#!/usr/bin/env python3
"""
IIB vs APIM response comparison tool.

Scans a folder of files named:
    <clientNumber_or_SWN>_<serviceNumber>_<IIB|APIM>.xml
    <clientNumber_or_SWN>_<serviceNumber>_<IIB|APIM>.json

Pairs up files that share the same <clientNumber_or_SWN>_<serviceNumber> key,
compares the IIB response against the APIM response, categorises differences,
and writes a single Markdown report.

Usage:
    python compare_report.py --input ./responses --output ./comparison_report.md

Only uses the Python standard library (xml.etree, json, re, pathlib) so it
will run anywhere without extra installs.
"""

import argparse
import html
import json
import os
import re
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict, namedtuple
from difflib import SequenceMatcher
from pathlib import Path

# --------------------------------------------------------------------------
# Data structures
# --------------------------------------------------------------------------

Issue = namedtuple(
    "Issue",
    ["key", "category", "subcategory", "path", "iib_value", "apim_value", "note"],
)

# Fixed display order for the report sections
CATEGORY_MISSING_IN_APIM = "Missing Values: present in IIB, missing in APIM"
CATEGORY_MISSING_IN_IIB = "Missing Values: present in APIM, missing in IIB"
CATEGORY_NAMESPACE = "Namespace & Schema Declaration Differences"
CATEGORY_PREFIX = "Namespace Prefix Naming Differences (same URI, different prefix used)"
CATEGORY_NS_SCOPE = "Namespace Declaration Scope Differences (same URI & prefix, declared on a different element)"
CATEGORY_ORDERING = "Element/Field Ordering Differences (data matches, order differs)"
CATEGORY_EMPTY = "Empty Elements/Tags (present but no value)"

CATEGORY_ORDER = [
    CATEGORY_NAMESPACE,
    CATEGORY_PREFIX,
    CATEGORY_NS_SCOPE,
    "Schema & Validation Errors",
    CATEGORY_ORDERING,
    CATEGORY_MISSING_IN_APIM,
    CATEGORY_MISSING_IN_IIB,
    CATEGORY_EMPTY,
    "SOAP Fault",
    "Data Integrity & Logic Issues",
    "Value Mismatch",
    "File / Pairing Issues",
]

# This report only covers pairs where a difference was found - not a full
# log of every service tested - so the title reflects that scope.
REPORT_TITLE = "IIB vs APIM Migration - Mismatch Analysis Report"

# --------------------------------------------------------------------------
# Helpers: filename parsing / pairing
# --------------------------------------------------------------------------

FILENAME_RE = re.compile(r"^(?P<key>.+)_(?P<source>IIB|APIM|AZURE)\.(?P<ext>xml|json)$", re.IGNORECASE)


def discover_pairs(folder: Path):
    """Group files in `folder` by <clientNumber_or_SWN>_<serviceNumber> key.

    Accepts IIB, APIM, or AZURE as the source token (AZURE is treated as the
    same "target" bucket as APIM, since some environments name their files
    that way). The literal label found in the filename is preserved in
    `target_labels` so the report can show "Azure" instead of a hardcoded
    "APIM" where relevant.
    """
    pairs = defaultdict(dict)
    target_labels = {}
    unmatched = []
    for f in sorted(folder.iterdir()):
        if not f.is_file():
            continue
        m = FILENAME_RE.match(f.name)
        if not m:
            unmatched.append(f.name)
            continue
        key = m.group("key")
        source_raw = m.group("source").upper()
        bucket = "IIB" if source_raw == "IIB" else "APIM"
        pairs[key][bucket] = f
        if bucket == "APIM":
            target_labels[key] = m.group("source")  # preserve original casing, e.g. "Azure"
    return pairs, unmatched, target_labels


def find_batch_dirs(root: Path):
    """
    Walk `root` recursively and return every directory (root itself included)
    that directly contains at least one file matching the <key>_<IIB|APIM|AZURE>.<xml|json>
    naming pattern. Each such directory is treated as one independent batch -
    its files are compared only against each other, not against files in
    sibling or parent/child folders.
    """
    batch_dirs = []
    for dirpath, dirnames, filenames in os.walk(root):
        if any(FILENAME_RE.match(f) for f in filenames):
            batch_dirs.append(Path(dirpath))
    return sorted(batch_dirs)


# --------------------------------------------------------------------------
# Helpers: XML flattening
# --------------------------------------------------------------------------

def strip_ns(tag: str) -> str:
    return tag.split("}", 1)[1] if "}" in tag else tag


def flatten_xml(elem, prefix):
    """
    Returns (leaves, order) for this element and all descendants.
      leaves: dict path -> text value (for leaf nodes) and path/@attr -> attr value
      order:  dict path -> list of immediate child tag names, in document order
    Repeated sibling tags get an index, e.g. Items/Item[0], Items/Item[1].
    """
    leaves = {}
    order = {}

    if elem.attrib:
        for k, v in elem.attrib.items():
            leaves[f"{prefix}/@{strip_ns(k)}"] = v

    children = list(elem)
    order[prefix] = [strip_ns(c.tag) for c in children]

    if not children:
        leaves[prefix] = (elem.text or "").strip()
        return leaves, order

    tag_counts = Counter(strip_ns(c.tag) for c in children)
    seen = defaultdict(int)
    for c in children:
        tag = strip_ns(c.tag)
        if tag_counts[tag] > 1:
            idx = seen[tag]
            seen[tag] += 1
            child_path = f"{prefix}/{tag}[{idx}]"
        else:
            child_path = f"{prefix}/{tag}"
        c_leaves, c_order = flatten_xml(c, child_path)
        leaves.update(c_leaves)
        order.update(c_order)

    return leaves, order


def detect_soap_fault_xml(root):
    """Look anywhere in the tree for a *Fault element and classify it."""
    for elem in root.iter():
        if strip_ns(elem.tag).lower() == "fault":
            code_text = ""
            for child in elem.iter():
                tag = strip_ns(child.tag).lower()
                if tag in ("faultcode", "value", "code"):
                    code_text = (child.text or "").strip()
                    if code_text:
                        break
            code_lower = code_text.lower()
            if "versionmismatch" in code_lower:
                return "VersionMismatch"
            if "mustunderstand" in code_lower:
                return "MustUnderstand"
            if "client" in code_lower or "sender" in code_lower:
                return "Client/Sender"
            if "server" in code_lower or "receiver" in code_lower:
                return "Server/Receiver"
            return f"Fault (unclassified: {code_text or 'no faultcode found'})"
    return None


def extract_namespaces(path: Path):
    """
    Returns a dict of {namespace URI -> set of prefixes used for it}, built
    from every xmlns / xmlns:prefix declaration in the document. This lets
    callers check both "is this schema URI present at all" (order-independent)
    and, separately, "is the same prefix alias used for it" (a cosmetic
    rename, not a schema change, but still worth surfacing separately).
    """
    uri_to_prefixes = defaultdict(set)
    for event, (prefix, uri) in ET.iterparse(str(path), events=("start-ns",)):
        uri_to_prefixes[uri].add(prefix)
    return dict(uri_to_prefixes)


def extract_namespace_scopes(path: Path):
    """
    Returns {(uri, prefix) -> tag name of the element that actually carries
    the xmlns declaration}, i.e. WHERE in the tree each namespace is
    declared - not just whether it's declared somewhere. iterparse fires
    "start-ns" events immediately before the "start" event of the element
    that declares them, so we can correlate the two.

    This catches things extract_namespaces can't: the same prefix bound to
    the same URI, but declared on a different element (e.g. IIB declares
    xmlns:NS2 directly on <NS2:header>, while APIM hoists the identical
    declaration up onto the parent element instead). Semantically null per
    XML namespace rules, but still a real, consistent serialization
    difference worth surfacing separately from a true prefix rename.
    Only the first occurrence of each (uri, prefix) pair is kept.
    """
    anchors = {}
    pending = []
    for event, value in ET.iterparse(str(path), events=("start-ns", "start")):
        if event == "start-ns":
            pending.append(value)  # (prefix, uri)
        else:
            tag = strip_ns(value.tag)
            for prefix, uri in pending:
                anchors.setdefault((uri, prefix), tag)
            pending = []
    return anchors


def load_xml(path: Path):
    tree = ET.parse(path)
    root = tree.getroot()
    root_path = strip_ns(root.tag)
    leaves, order = flatten_xml(root, root_path)
    fault = detect_soap_fault_xml(root)
    raw = path.read_text(encoding="utf-8", errors="replace")
    namespaces = extract_namespaces(path)
    ns_scopes = extract_namespace_scopes(path)
    return leaves, order, fault, raw, namespaces, ns_scopes


# --------------------------------------------------------------------------
# Helpers: JSON flattening
# --------------------------------------------------------------------------

def flatten_json(obj, prefix=""):
    leaves = {}
    order = {}
    if isinstance(obj, dict):
        order[prefix] = list(obj.keys())
        for k, v in obj.items():
            child_path = f"{prefix}/{k}" if prefix else k
            c_leaves, c_order = flatten_json(v, child_path)
            leaves.update(c_leaves)
            order.update(c_order)
    elif isinstance(obj, list):
        if not obj:
            leaves[prefix] = "[]"
        for i, v in enumerate(obj):
            child_path = f"{prefix}[{i}]"
            c_leaves, c_order = flatten_json(v, child_path)
            leaves.update(c_leaves)
            order.update(c_order)
    else:
        leaves[prefix] = "" if obj is None else obj
    return leaves, order


def detect_soap_fault_json(obj, prefix=""):
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k.lower() in ("fault", "error", "faultinfo"):
                code = None
                if isinstance(v, dict):
                    for kk, vv in v.items():
                        if kk.lower() in ("faultcode", "code", "errorcode"):
                            code = str(vv)
                            break
                code_lower = (code or "").lower()
                if "versionmismatch" in code_lower:
                    return "VersionMismatch"
                if "mustunderstand" in code_lower:
                    return "MustUnderstand"
                if "client" in code_lower or "sender" in code_lower:
                    return "Client/Sender"
                if "server" in code_lower or "receiver" in code_lower:
                    return "Server/Receiver"
                return f"Fault (unclassified: {code or 'no code found'})"
            result = detect_soap_fault_json(v, f"{prefix}/{k}")
            if result:
                return result
    return None


def load_json(path: Path):
    with open(path, "r", encoding="utf-8") as fh:
        obj = json.load(fh)
    leaves, order = flatten_json(obj)
    fault = detect_soap_fault_json(obj)
    raw = path.read_text(encoding="utf-8", errors="replace")
    return leaves, order, fault, raw, {}, {}  # no namespaces/scopes in JSON


def load_and_flatten(path: Path):
    ext = path.suffix.lower()
    if ext == ".xml":
        return load_xml(path)
    elif ext == ".json":
        return load_json(path)
    raise ValueError(f"Unsupported extension: {path}")


# --------------------------------------------------------------------------
# Comparison logic
# --------------------------------------------------------------------------

NUMERIC_KEYWORDS = ("balance", "amount", "price", "qty", "quantity", "total", "count", "value")


def infer_type(s: str) -> str:
    if s.lower() in ("true", "false"):
        return "boolean"
    try:
        int(s)
        return "integer"
    except ValueError:
        pass
    try:
        float(s)
        return "float"
    except ValueError:
        pass
    return "string"


def build_side_by_side_diff(left_raw: str, right_raw: str):
    """
    Line-based diff between two raw file contents. Returns (left_html, right_html)
    ready to drop inside <pre> tags: matching lines are shown as-is, differing
    lines are wrapped in <mark> (renders with a yellow highlight by default).
    """
    left_lines = left_raw.splitlines()
    right_lines = right_raw.splitlines()
    sm = SequenceMatcher(None, left_lines, right_lines, autojunk=False)

    left_out = []
    right_out = []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            for line in left_lines[i1:i2]:
                left_out.append(html.escape(line))
            for line in right_lines[j1:j2]:
                right_out.append(html.escape(line))
        else:
            for line in left_lines[i1:i2]:
                left_out.append(f"<mark>{html.escape(line)}</mark>")
            for line in right_lines[j1:j2]:
                right_out.append(f"<mark>{html.escape(line)}</mark>")

    return "\n".join(left_out), "\n".join(right_out)


def leaf_name(path: str) -> str:
    """
    Extract the field/tag name at the end of a path, for grouping issues by
    field rather than by full path. 'a/b/c[2]' -> 'c', 'a/b/@id' -> '@id'.
    """
    last = path.rsplit("/", 1)[-1]
    if last.startswith("@"):
        return last
    return re.sub(r"\[\d+\]$", "", last)


def business_logic_flag(path: str, s1: str, s2: str):
    """Very small set of heuristic business-rule checks. Customise for your domain."""
    lower_path = path.lower()
    if any(k in lower_path for k in NUMERIC_KEYWORDS):
        for label, s in (("IIB", s1), ("APIM", s2)):
            try:
                if float(s) < 0:
                    return f"Negative value in numeric field ({label} side) - possible business rule violation"
            except ValueError:
                pass
    return None


def compare_pair(key, files):
    """files: dict with optional 'IIB' and 'APIM' Path entries."""
    issues = []
    iib_path = files.get("IIB")
    apim_path = files.get("APIM")

    if iib_path is None:
        issues.append(Issue(key, "File / Pairing Issues", "Missing IIB file", "-", None, str(apim_path.name), ""))
        return issues, None, None
    if apim_path is None:
        issues.append(Issue(key, "File / Pairing Issues", "Missing APIM file", "-", str(iib_path.name), None, ""))
        return issues, None, None

    try:
        iib_leaves, iib_order, iib_fault, iib_raw, iib_ns, iib_ns_scopes = load_and_flatten(iib_path)
    except Exception as e:
        issues.append(Issue(key, "File / Pairing Issues", "IIB file failed to parse", str(iib_path.name), str(e), None, ""))
        return issues, None, None

    try:
        apim_leaves, apim_order, apim_fault, apim_raw, apim_ns, apim_ns_scopes = load_and_flatten(apim_path)
    except Exception as e:
        issues.append(Issue(key, "File / Pairing Issues", "APIM file failed to parse", str(apim_path.name), None, str(e), ""))
        return issues, iib_raw, None

    # ---- namespace / schema declaration comparison (XML only) ----
    # Order doesn't matter - we only care that the same set of namespace
    # URIs is declared on both sides. iib_ns/apim_ns are now {uri: {prefixes}}.
    if iib_path.suffix.lower() == ".xml" and apim_path.suffix.lower() == ".xml":
        iib_uris = set(iib_ns.keys())
        apim_uris = set(apim_ns.keys())
        missing_in_apim_ns = sorted(iib_uris - apim_uris)
        missing_in_iib_ns = sorted(apim_uris - iib_uris)
        if missing_in_apim_ns:
            issues.append(Issue(key, CATEGORY_NAMESPACE, "Namespace declared in IIB but missing in APIM",
                                 "(document namespaces)", ", ".join(missing_in_apim_ns), None, ""))
        if missing_in_iib_ns:
            issues.append(Issue(key, CATEGORY_NAMESPACE, "Namespace declared in APIM but missing in IIB",
                                 "(document namespaces)", None, ", ".join(missing_in_iib_ns), ""))

        # Separately: for namespace URIs present on BOTH sides, check whether the
        # actual prefix alias used differs (e.g. IIB's "out4" vs APIM's "hdr" for
        # the exact same URI). This is a cosmetic rename, not a schema change -
        # XML namespace rules mean these documents are equivalent - but it's
        # tracked as its own category since some downstream consumers or test
        # processes may still care about prefix consistency.
        for uri in sorted(iib_uris & apim_uris):
            iib_prefixes = iib_ns[uri]
            apim_prefixes = apim_ns[uri]
            if iib_prefixes != apim_prefixes:
                iib_disp = ", ".join(sorted(p if p else "(default)" for p in iib_prefixes))
                apim_disp = ", ".join(sorted(p if p else "(default)" for p in apim_prefixes))
                issues.append(Issue(key, CATEGORY_PREFIX, f"Prefix renamed for namespace `{uri}`",
                                     "(document namespaces)", iib_disp, apim_disp, ""))

        # Separately again: for (uri, prefix) pairs that match exactly on both
        # sides (no rename), check whether the namespace is actually declared
        # on a different element. Same URI, same prefix, but IIB declares it
        # directly on e.g. <header> while APIM hoists it up onto a parent
        # element instead - semantically null, but a real, consistent
        # serialization difference worth its own category.
        common_ns_keys = set(iib_ns_scopes.keys()) & set(apim_ns_scopes.keys())
        for uri, prefix in sorted(common_ns_keys):
            iib_anchor = iib_ns_scopes[(uri, prefix)]
            apim_anchor = apim_ns_scopes[(uri, prefix)]
            if iib_anchor != apim_anchor:
                prefix_disp = prefix or "(default)"
                issues.append(Issue(key, CATEGORY_NS_SCOPE,
                                     f"Namespace `{prefix_disp}` ({uri}) declared on a different element",
                                     "(document namespaces)",
                                     f"declared on <{iib_anchor}>", f"declared on <{apim_anchor}>", ""))

    all_paths = sorted(set(iib_leaves) | set(apim_leaves))
    for path in all_paths:
        in_iib = path in iib_leaves
        in_apim = path in apim_leaves
        is_attr = "/@" in path
        missing_label = "attribute" if is_attr else "tag"

        if in_iib and not in_apim:
            issues.append(Issue(key, CATEGORY_MISSING_IN_APIM, f"Missing {missing_label}: `{leaf_name(path)}`",
                                 path, iib_leaves[path], None, ""))
            continue
        if in_apim and not in_iib:
            issues.append(Issue(key, CATEGORY_MISSING_IN_IIB, f"Missing {missing_label}: `{leaf_name(path)}`",
                                 path, None, apim_leaves[path], ""))
            continue

        v1, v2 = iib_leaves[path], apim_leaves[path]
        s1 = "" if v1 is None else str(v1).strip()
        s2 = "" if v2 is None else str(v2).strip()

        if s1 == "" and s2 == "":
            continue
        if s1 == "" or s2 == "":
            issues.append(Issue(key, CATEGORY_EMPTY, f"Empty value: `{leaf_name(path)}`",
                                 path, v1, v2, ""))
            continue
        if s1 == s2:
            continue

        t1, t2 = infer_type(s1), infer_type(s2)
        if t1 != t2:
            issues.append(Issue(key, "Schema & Validation Errors", f"Data type mismatch: `{leaf_name(path)}`",
                                 path, v1, v2, f"IIB looks like {t1}, APIM looks like {t2}"))
            continue

        bl = business_logic_flag(path, s1, s2)
        if bl:
            issues.append(Issue(key, "Data Integrity & Logic Issues", f"{bl}: `{leaf_name(path)}`", path, v1, v2, ""))
            continue

        issues.append(Issue(key, "Value Mismatch", f"`{leaf_name(path)}` value differs", path, v1, v2, ""))

    # Element ordering check (mainly meaningful for XML; JSON object key order
    # is not semantically significant so this will rarely fire for JSON, but
    # array-of-object ordering differences will still show up as Value Mismatches above.)
    for path in sorted(set(iib_order) & set(apim_order)):
        seq1, seq2 = iib_order[path], apim_order[path]
        if seq1 != seq2 and sorted(seq1) == sorted(seq2) and seq1:
            parent_name = leaf_name(path) if path else path
            issues.append(Issue(key, CATEGORY_ORDERING, f"Order differs under `{parent_name}` (same elements & values present)",
                                 path, " -> ".join(seq1), " -> ".join(seq2), ""))

    if iib_fault:
        issues.append(Issue(key, "SOAP Fault", iib_fault, "(fault found in IIB response)", "FAULT", "OK", ""))
    if apim_fault:
        issues.append(Issue(key, "SOAP Fault", apim_fault, "(fault found in APIM response)", "OK", "FAULT", ""))

    return issues, iib_raw, apim_raw


# --------------------------------------------------------------------------
# Report generation
# --------------------------------------------------------------------------

def anchor_id(key: str) -> str:
    return "detail-" + re.sub(r"[^A-Za-z0-9]+", "-", key).strip("-").lower()


def category_anchor_id(category: str) -> str:
    return "cat-" + re.sub(r"[^A-Za-z0-9]+", "-", category).strip("-").lower()


def fmt_val(v):
    if v is None:
        return "_(missing)_"
    s = str(v)
    if s == "":
        return "_(empty)_"
    return f"`{s}`"


def fmt_val_html(v):
    if v is None:
        return "<em>(missing)</em>"
    s = str(v)
    if s == "":
        return "<em>(empty)</em>"
    return f"<code>{html.escape(s)}</code>"


def compute_report_data(pairs, unmatched, target_labels=None):
    """Run all comparisons once and return a plain dict with everything
    both renderers (Markdown / HTML) need, so the two output formats can
    never drift out of sync with each other."""
    target_labels = target_labels or {}
    all_issues = []
    raw_by_key = {}

    for key in sorted(pairs.keys()):
        issues, iib_raw, apim_raw = compare_pair(key, pairs[key])
        all_issues.extend(issues)
        raw_by_key[key] = (iib_raw, apim_raw)

    keys_with_issues = sorted({i.key for i in all_issues})
    total_pairs = len(pairs)
    pairs_clean = total_pairs - len(keys_with_issues)

    missing_in_apim_keys = {i.key for i in all_issues if i.category == CATEGORY_MISSING_IN_APIM}
    missing_in_iib_keys = {i.key for i in all_issues if i.category == CATEGORY_MISSING_IN_IIB}
    missing_attr_count = sum(1 for i in all_issues if "/@" in i.path and i.category in (CATEGORY_MISSING_IN_APIM, CATEGORY_MISSING_IN_IIB))
    missing_tag_count = sum(1 for i in all_issues if "/@" not in i.path and i.category in (CATEGORY_MISSING_IN_APIM, CATEGORY_MISSING_IN_IIB))
    value_mismatch_count = sum(1 for i in all_issues if i.category == "Value Mismatch")
    namespace_issue_count = sum(1 for i in all_issues if i.category == CATEGORY_NAMESPACE)
    unique_subcategories = sorted({i.subcategory for i in all_issues})

    grouped = defaultdict(lambda: defaultdict(list))  # category -> subcategory -> [keys]
    for i in all_issues:
        if i.key not in grouped[i.category][i.subcategory]:
            grouped[i.category][i.subcategory].append(i.key)

    # Per-category stats, computed for EVERY tracked category (including ones
    # with zero findings) so the summary can show "0" instead of omitting them.
    category_stats = {}
    for cat in CATEGORY_ORDER:
        cat_issues = [i for i in all_issues if i.category == cat]
        category_stats[cat] = {
            "instances": len(cat_issues),
            "pairs": len({i.key for i in cat_issues}),
        }

    # Tag vs. attribute breakdown, specifically for the two missing-value categories.
    missing_breakdown = {}
    for cat in (CATEGORY_MISSING_IN_APIM, CATEGORY_MISSING_IN_IIB):
        cat_issues = [i for i in all_issues if i.category == cat]
        missing_breakdown[cat] = {
            "tags": sum(1 for i in cat_issues if "/@" not in i.path),
            "attrs": sum(1 for i in cat_issues if "/@" in i.path),
        }

    categories_with_findings = sum(1 for cat in CATEGORY_ORDER if category_stats[cat]["instances"] > 0)

    return {
        "pairs": pairs,
        "unmatched": unmatched,
        "target_labels": target_labels,
        "all_issues": all_issues,
        "raw_by_key": raw_by_key,
        "keys_with_issues": keys_with_issues,
        "total_pairs": total_pairs,
        "pairs_clean": pairs_clean,
        "missing_in_apim_keys": missing_in_apim_keys,
        "missing_in_iib_keys": missing_in_iib_keys,
        "missing_attr_count": missing_attr_count,
        "missing_tag_count": missing_tag_count,
        "value_mismatch_count": value_mismatch_count,
        "namespace_issue_count": namespace_issue_count,
        "unique_subcategories": unique_subcategories,
        "grouped": grouped,
        "category_stats": category_stats,
        "missing_breakdown": missing_breakdown,
        "total_categories_tracked": len(CATEGORY_ORDER),
        "categories_with_findings": categories_with_findings,
    }


def write_markdown_report(data, out_path: Path, raw_snippet_limit=4000):
    pairs = data["pairs"]
    unmatched = data["unmatched"]
    target_labels = data["target_labels"]
    all_issues = data["all_issues"]
    raw_by_key = data["raw_by_key"]
    grouped = data["grouped"]
    category_stats = data["category_stats"]
    missing_breakdown = data["missing_breakdown"]

    lines = []
    lines.append(f"# {REPORT_TITLE}")
    lines.append("")
    lines.append("_This report only lists service contracts where at least one difference was found between "
                 "IIB and APIM/Azure - it is not a full log of every contract tested._")
    lines.append("")

    # ==================== Summary (collapsible) ====================
    lines.append("<details open>")
    lines.append('<summary><strong style="font-size:1.4em;">Summary</strong></summary>')
    lines.append("")
    lines.append('<a id="summary"></a>')
    lines.append("")
    lines.append("**Overview**")
    lines.append("")
    lines.append(f"- Total Mismatched Service Contracts Analysed: **{len(data['keys_with_issues'])}**")
    lines.append(f"- Total Individual Issue Instances: **{len(all_issues)}**")
    lines.append(f"- Issue Categories With Findings: **{data['categories_with_findings']} of {data['total_categories_tracked']}** tracked categories")
    lines.append(f"- Unique Specific Issue Types Found (one per field/tag, e.g. `description` value differs): **{len(data['unique_subcategories'])}**")
    if unmatched:
        lines.append(f"- Files That Didn't Match The Naming Pattern (ignored): **{len(unmatched)}**")
    lines.append("")
    lines.append("**Issues by category** — every tracked category is listed below; a category shows as a link "
                  "only when it has findings, otherwise its counts show as 0.")
    lines.append("")
    lines.append("| Category | Instances | Service Contracts Affected |")
    lines.append("|---|---|---|")
    for cat in CATEGORY_ORDER:
        stats = category_stats[cat]
        if stats["instances"] > 0:
            name_cell = f"[{cat}](#{category_anchor_id(cat)})"
        else:
            name_cell = cat
        extra = ""
        if cat in missing_breakdown and stats["instances"] > 0:
            b = missing_breakdown[cat]
            extra = f" ({b['tags']} tag(s), {b['attrs']} attribute(s))"
        lines.append(f"| {name_cell}{extra} | {stats['instances']} | {stats['pairs']} |")
    lines.append("")
    lines.append("</details>")
    lines.append("")

    # ==================== Issues by Category (collapsible) ====================
    lines.append("<details>")
    lines.append('<summary><strong style="font-size:1.4em;">Issues by Category</strong></summary>')
    lines.append("")
    lines.append('<a id="issues-by-category"></a>')
    lines.append("")
    for category in CATEGORY_ORDER:
        if category not in grouped:
            continue
        lines.append("<details open>")
        lines.append(f'<summary><strong style="font-size:1.15em;">{category}</strong></summary>')
        lines.append("")
        lines.append(f'<a id="{category_anchor_id(category)}"></a>')
        lines.append("")
        for subcat in sorted(grouped[category].keys()):
            keys = grouped[category][subcat]
            lines.append(f"**{subcat}** ({len(keys)} case(s))")
            lines.append("")
            links = ", ".join(f"[{k}](#{anchor_id(k)})" for k in sorted(keys))
            lines.append(links)
            lines.append("")
        lines.append("</details>")
        lines.append("")

    if unmatched:
        lines.append("<details>")
        lines.append('<summary><strong style="font-size:1.15em;">Files ignored (naming pattern mismatch)</strong></summary>')
        lines.append("")
        for fname in unmatched:
            lines.append(f"- `{fname}`")
        lines.append("")
        lines.append("</details>")
        lines.append("")
    lines.append("</details>")
    lines.append("")

    # ==================== Detailed Comparisons (collapsible, closed per-pair) ====================
    lines.append("<details>")
    lines.append('<summary><strong style="font-size:1.4em;">Detailed Comparisons</strong></summary>')
    lines.append("")
    lines.append('<a id="detailed-comparisons"></a>')
    lines.append("")
    for key in sorted(pairs.keys()):
        key_issues = [i for i in all_issues if i.key == key]
        if not key_issues:
            continue  # only show pairs that actually had issues; change this to show all pairs if you want a full log
        lines.append("<details>")
        lines.append(f'<summary><strong style="font-size:1.15em;">{key}</strong></summary>')
        lines.append("")
        lines.append(f'<a id="{anchor_id(key)}"></a>')
        lines.append("")
        lines.append(f"{len(key_issues)} issue(s) found. [Back to category list](#issues-by-category)")
        lines.append("")
        lines.append("| Path | IIB Value | APIM Value | Category | Detail |")
        lines.append("|---|---|---|---|---|")
        for i in key_issues:
            iib_disp = fmt_val(i.iib_value)
            apim_disp = fmt_val(i.apim_value)
            if str(i.iib_value) != str(i.apim_value):
                iib_disp = f"**{iib_disp}**"
                apim_disp = f"**{apim_disp}**"
            lines.append(f"| `{i.path}` | {iib_disp} | {apim_disp} | {i.subcategory} | {i.note} |")
        lines.append("")

        iib_raw, apim_raw = raw_by_key.get(key, (None, None))
        if iib_raw is not None and apim_raw is not None:
            iib_html, apim_html = build_side_by_side_diff(
                iib_raw[:raw_snippet_limit], apim_raw[:raw_snippet_limit]
            )
            lines.append("<details>")  # closed by default - this is the bulky part
            lines.append("<summary>Side-by-side raw response (differing lines highlighted) — click to expand</summary>")
            lines.append("")
            lines.append("<table>")
            lines.append(f'<tr><th align="left" width="50%">IIB</th><th align="left" width="50%">{target_labels.get(key, "APIM")}</th></tr>')
            lines.append("<tr>")
            lines.append(f'<td valign="top"><pre>{iib_html}</pre></td>')
            lines.append(f'<td valign="top"><pre>{apim_html}</pre></td>')
            lines.append("</tr>")
            lines.append("</table>")
            lines.append("")
            lines.append("</details>")
            lines.append("")
        elif iib_raw is not None:
            lines.append("<details><summary>Raw IIB response (no APIM response available to compare)</summary>")
            lines.append("")
            lines.append("```")
            lines.append(iib_raw[:raw_snippet_limit])
            lines.append("```")
            lines.append("</details>")
            lines.append("")
        elif apim_raw is not None:
            lines.append("<details><summary>Raw APIM response (no IIB response available to compare)</summary>")
            lines.append("")
            lines.append("```")
            lines.append(apim_raw[:raw_snippet_limit])
            lines.append("```")
            lines.append("</details>")
            lines.append("")

        lines.append("</details>")  # close key-level details
        lines.append("")

    lines.append("</details>")  # close Detailed Comparisons container
    lines.append("")
    lines.append(AUTO_EXPAND_SCRIPT)
    lines.append("")

    out_path.write_text("\n".join(lines), encoding="utf-8")


HTML_STYLE = """
:root {
  color-scheme: light;
  --border: #d0d7de;
  --bg-alt: #f6f8fa;
  --text-muted: #57606a;
  --accent: #0969da;
}
* { box-sizing: border-box; }
body {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
  max-width: 1200px;
  margin: 0 auto;
  padding: 32px 24px 80px;
  color: #1f2328;
  line-height: 1.5;
}
h1 { border-bottom: 2px solid var(--border); padding-bottom: 8px; }
h2 { border-bottom: 1px solid var(--border); padding-bottom: 6px; margin-top: 40px; }
h3 { margin-top: 32px; }
a { color: var(--accent); text-decoration: none; }
a:hover { text-decoration: underline; }
ul { margin-top: 4px; }
.summary-list { list-style: none; padding-left: 0; }
.summary-list li {
  padding: 6px 10px;
  border-bottom: 1px solid var(--border);
}
.summary-list li strong { color: var(--accent); }
.subcat-block { margin-bottom: 18px; }
.key-links { margin-top: 6px; line-height: 1.8; }
.key-links a { white-space: nowrap; }
.subcat-title {
  font-weight: 600;
  background: var(--bg-alt);
  padding: 6px 10px;
  border-radius: 6px;
  display: inline-block;
}
table { border-collapse: collapse; width: 100%; margin: 12px 0; }
table.issues-table th, table.issues-table td {
  border: 1px solid var(--border);
  padding: 6px 10px;
  vertical-align: top;
  font-size: 14px;
}
table.issues-table th { background: var(--bg-alt); text-align: left; }
table.diff-table td { border: 1px solid var(--border); vertical-align: top; width: 50%; }
table.diff-table th { border: 1px solid var(--border); background: var(--bg-alt); padding: 8px; }
table.diff-table pre {
  margin: 0;
  padding: 10px;
  white-space: pre-wrap;
  word-break: break-word;
  font-size: 12.5px;
  max-height: 600px;
  overflow-y: auto;
}
mark { background: #fff2a8; padding: 0 1px; }
code { background: var(--bg-alt); padding: 1px 5px; border-radius: 4px; font-size: 90%; }
.pill {
  display: inline-block; background: var(--bg-alt); border: 1px solid var(--border);
  border-radius: 999px; padding: 2px 10px; font-size: 12px; color: var(--text-muted);
}
.toc-cat { margin-top: 6px; }
.back-to-top { font-size: 12px; }
details { margin: 10px 0; }
details > summary { cursor: pointer; font-weight: 600; list-style: none; }
details > summary::-webkit-details-marker { display: none; }
details > summary::before { content: "▶ "; font-size: 0.75em; color: var(--text-muted); }
details[open] > summary::before { content: "▼ "; }
details details {
  margin-left: 18px;
  padding-left: 14px;
  border-left: 2px solid var(--border);
}
h4 { margin-bottom: 4px; }
"""

# Best-effort fallback: some markdown viewers / embedded webviews don't
# implement the native browser behaviour of auto-opening ancestor <details>
# elements when you navigate to an anchor inside them. This script forces
# that behaviour explicitly. It's a harmless no-op wherever <script> tags
# get stripped (many markdown renderers strip them for security) - in that
# case you fall back to native browser support only, same as before.
AUTO_EXPAND_SCRIPT = """<script>
(function () {
  function openDetailsForHash() {
    var id = decodeURIComponent(location.hash.substring(1));
    if (!id) return;
    var el = document.getElementById(id);
    if (!el) return;
    var node = el;
    while (node) {
      if (node.tagName === "DETAILS") { node.open = true; }
      node = node.parentElement;
    }
  }
  window.addEventListener("hashchange", openDetailsForHash);
  window.addEventListener("load", openDetailsForHash);
  document.addEventListener("DOMContentLoaded", openDetailsForHash);
})();
</script>"""


def write_html_report(data, out_path: Path, raw_snippet_limit=4000):
    pairs = data["pairs"]
    unmatched = data["unmatched"]
    target_labels = data["target_labels"]
    all_issues = data["all_issues"]
    raw_by_key = data["raw_by_key"]
    grouped = data["grouped"]
    category_stats = data["category_stats"]
    missing_breakdown = data["missing_breakdown"]

    parts = []
    parts.append("<!DOCTYPE html>")
    parts.append('<html lang="en"><head><meta charset="UTF-8">')
    parts.append('<meta name="viewport" content="width=device-width, initial-scale=1">')
    parts.append(f"<title>{html.escape(REPORT_TITLE)}</title>")
    parts.append(f"<style>{HTML_STYLE}</style>")
    parts.append("</head><body>")

    parts.append(f"<h1>{html.escape(REPORT_TITLE)}</h1>")
    parts.append("<p><em>This report only lists service contracts where at least one difference was found "
                  "between IIB and APIM/Azure - it is not a full log of every contract tested.</em></p>")

    # ==================== Summary (collapsible) ====================
    parts.append("<details open>")
    parts.append('<summary><strong style="font-size:1.4em;">Summary</strong></summary>')
    parts.append('<a id="summary"></a>')

    parts.append("<h4>Overview</h4>")
    parts.append('<ul class="summary-list">')
    overview_rows = [
        ("Total Mismatched Service Contracts Analysed", len(data["keys_with_issues"])),
        ("Total Individual Issue Instances", len(all_issues)),
        ("Issue Categories With Findings", f'{data["categories_with_findings"]} of {data["total_categories_tracked"]} tracked categories'),
        ("Unique Specific Issue Types Found (one per field/tag)", len(data["unique_subcategories"])),
    ]
    if unmatched:
        overview_rows.append(("Files That Didn't Match The Naming Pattern (ignored)", len(unmatched)))
    for label, val in overview_rows:
        parts.append(f"<li>{html.escape(label)}: <strong>{val}</strong></li>")
    parts.append("</ul>")

    parts.append("<h4>Issues by category</h4>")
    parts.append("<p>Every tracked category is listed below; a category name is a link only when it has findings, otherwise its counts show as 0.</p>")
    parts.append('<table class="issues-table">')
    parts.append("<tr><th>Category</th><th>Instances</th><th>Service Contracts Affected</th></tr>")
    for cat in CATEGORY_ORDER:
        stats = category_stats[cat]
        if stats["instances"] > 0:
            name_cell = f'<a href="#{category_anchor_id(cat)}">{html.escape(cat)}</a>'
        else:
            name_cell = html.escape(cat)
        if cat in missing_breakdown and stats["instances"] > 0:
            b = missing_breakdown[cat]
            name_cell += f' <span class="pill">{b["tags"]} tag(s), {b["attrs"]} attribute(s)</span>'
        parts.append(f"<tr><td>{name_cell}</td><td>{stats['instances']}</td><td>{stats['pairs']}</td></tr>")
    parts.append("</table>")
    parts.append("</details>")

    # ==================== Issues by Category (collapsible) ====================
    parts.append("<details>")
    parts.append('<summary><strong style="font-size:1.4em;">Issues by Category</strong></summary>')
    parts.append('<a id="issues-by-category"></a>')
    for category in CATEGORY_ORDER:
        if category not in grouped:
            continue
        parts.append("<details open>")
        parts.append(f'<summary><strong style="font-size:1.15em;">{html.escape(category)}</strong></summary>')
        parts.append(f'<a id="{category_anchor_id(category)}"></a>')
        for subcat in sorted(grouped[category].keys()):
            keys = grouped[category][subcat]
            parts.append('<div class="subcat-block">')
            parts.append(f'<div class="subcat-title">{html.escape(subcat)} <span class="pill">{len(keys)} case(s)</span></div>')
            links = ", ".join(f'<a href="#{anchor_id(k)}">{html.escape(k)}</a>' for k in sorted(keys))
            parts.append(f'<div class="key-links">{links}</div>')
            parts.append("</div>")
        parts.append("</details>")

    if unmatched:
        parts.append("<details>")
        parts.append('<summary><strong style="font-size:1.15em;">Files ignored (naming pattern mismatch)</strong></summary>')
        parts.append("<ul>")
        for fname in unmatched:
            parts.append(f"<li><code>{html.escape(fname)}</code></li>")
        parts.append("</ul>")
        parts.append("</details>")
    parts.append("</details>")

    # ==================== Detailed Comparisons (collapsible per-pair) ====================
    parts.append("<details>")
    parts.append('<summary><strong style="font-size:1.4em;">Detailed Comparisons</strong></summary>')
    parts.append('<a id="detailed-comparisons"></a>')
    for key in sorted(pairs.keys()):
        key_issues = [i for i in all_issues if i.key == key]
        if not key_issues:
            continue
        parts.append("<details>")
        parts.append(f'<summary><strong style="font-size:1.15em;">{html.escape(key)}</strong></summary>')
        parts.append(f'<a id="{anchor_id(key)}"></a>')
        parts.append(f'<p>{len(key_issues)} issue(s) found. <a class="back-to-top" href="#issues-by-category">[back to category list]</a></p>')

        parts.append('<table class="issues-table">')
        parts.append("<tr><th>Path</th><th>IIB Value</th><th>APIM Value</th><th>Category</th><th>Detail</th></tr>")
        for i in key_issues:
            iib_disp = fmt_val_html(i.iib_value)
            apim_disp = fmt_val_html(i.apim_value)
            if str(i.iib_value) != str(i.apim_value):
                iib_disp = f"<mark>{iib_disp}</mark>"
                apim_disp = f"<mark>{apim_disp}</mark>"
            parts.append(
                f"<tr><td><code>{html.escape(i.path)}</code></td><td>{iib_disp}</td>"
                f"<td>{apim_disp}</td><td>{html.escape(i.subcategory)}</td><td>{html.escape(i.note)}</td></tr>"
            )
        parts.append("</table>")

        iib_raw, apim_raw = raw_by_key.get(key, (None, None))
        if iib_raw is not None and apim_raw is not None:
            iib_diff_html, apim_diff_html = build_side_by_side_diff(
                iib_raw[:raw_snippet_limit], apim_raw[:raw_snippet_limit]
            )
            parts.append("<details>")  # closed by default - this is the bulky part
            parts.append("<summary>Side-by-side raw response (differing lines highlighted) — click to expand</summary>")
            parts.append('<table class="diff-table">')
            parts.append(f'<tr><th>IIB</th><th>{html.escape(target_labels.get(key, "APIM"))}</th></tr>')
            parts.append(f"<tr><td><pre>{iib_diff_html}</pre></td><td><pre>{apim_diff_html}</pre></td></tr>")
            parts.append("</table>")
            parts.append("</details>")
        elif iib_raw is not None:
            parts.append("<details><summary>Raw IIB response (no APIM response available to compare)</summary>")
            parts.append(f"<pre>{html.escape(iib_raw[:raw_snippet_limit])}</pre>")
            parts.append("</details>")
        elif apim_raw is not None:
            parts.append(f'<details><summary>Raw {html.escape(target_labels.get(key, "APIM"))} response (no IIB response available to compare)</summary>')
            parts.append(f"<pre>{html.escape(apim_raw[:raw_snippet_limit])}</pre>")
            parts.append("</details>")

        parts.append("</details>")  # close key-level details

    parts.append("</details>")  # close Detailed Comparisons container

    parts.append(AUTO_EXPAND_SCRIPT)
    parts.append("</body></html>")

    out_path.write_text("\n".join(parts), encoding="utf-8")


# --------------------------------------------------------------------------
# Entry point
# --------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Compare IIB vs APIM response files and produce Markdown + HTML reports. "
                    "Supports an --input folder containing subfolders of response files: each "
                    "subfolder that contains matching files is compared independently, and the "
                    "same folder structure is recreated under --output, with each report named "
                    "after the folder it came from."
    )
    parser.add_argument("--input", required=True,
                         help="Folder containing the response files. May contain subfolders - "
                              "each subfolder with matching files is treated as its own batch.")
    parser.add_argument("--output", required=True,
                         help="Output directory. The input folder's structure is recreated here, "
                              "with <foldername>_comparison_report.md/.html written into each "
                              "corresponding subfolder.")
    args = parser.parse_args()

    in_root = Path(args.input)
    out_root = Path(args.output)

    if not in_root.is_dir():
        print(f"Input path is not a folder: {in_root}")
        return

    batch_dirs = find_batch_dirs(in_root)
    if not batch_dirs:
        print(f"No files matching <key>_<IIB|APIM|AZURE>.<xml|json> found under {in_root}")
        return

    if out_root.exists() and not out_root.is_dir():
        print(f"--output path '{out_root}' already exists and is a FILE, not a folder.\n"
              f"This tool needs to create '{out_root}' as a directory to write reports into.\n"
              f"Delete or rename that file, or choose a different --output path, then try again.")
        return

    out_root.mkdir(parents=True, exist_ok=True)
    reports_written = 0

    for batch_dir in batch_dirs:
        rel = batch_dir.relative_to(in_root)
        out_dir = out_root if str(rel) == "." else out_root / rel
        out_dir.mkdir(parents=True, exist_ok=True)

        # Name the report after the folder that directly contains its files
        # (resolve() so this also works sensibly if --input was "." or similar).
        folder_name = batch_dir.resolve().name or "root"

        pairs, unmatched, target_labels = discover_pairs(batch_dir)
        if not pairs:
            continue

        data = compute_report_data(pairs, unmatched, target_labels)
        md_path = out_dir / f"{folder_name}_comparison_report.md"
        html_path = out_dir / f"{folder_name}_comparison_report.html"
        # write_markdown_report(data, md_path)
        write_html_report(data, html_path)
        reports_written += 1

        complete_pairs = sum(1 for files in pairs.values() if len(files) == 2)
        single_sided = len(pairs) - complete_pairs
        mismatched = len(data["keys_with_issues"])
        clean = len(pairs) - mismatched  # includes single-sided keys, which always register as an issue, so
                                          # "clean" here really means complete pairs with zero differences

        display_rel = "." if str(rel) == "." else str(rel)
        print(f"[{display_rel}] {len(pairs)} keys found "
              f"({complete_pairs} complete pairs, {single_sided} single-sided/missing-file), "
              f"{len(unmatched)} files ignored (naming pattern), "
              f"{mismatched} with mismatches, {clean} with zero differences "
              f"-> {md_path.relative_to(out_root)}, {html_path.relative_to(out_root)}")

        if len(pairs) > 0 and mismatched == 0:
            print(f"    WARNING: every key in this folder shows zero differences. If you expected "
                  f"mismatches here, double-check that IIB and APIM/Azure files are actually being "
                  f"paired correctly (see the {len(pairs)} keys found above) rather than genuinely matching.")

    print(f"\nDone. Generated reports for {reports_written} folder(s) under {out_root}")


if __name__ == "__main__":
    main()
