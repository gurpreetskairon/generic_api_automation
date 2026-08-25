"""
response_comparator.py

Compares two API response bodies (XML or JSON) - e.g. resp_a.text and resp_b.text
from IIB vs APIM calls - and reports differences in three categories:

    1. Namespace differences   (XML only - prefix/URI declarations, element/attr namespaces)
    2. Schema differences      (structural - missing/extra elements/keys, occurrence
                                 counts, array lengths, type mismatches)
    3. Value differences       (same structural location, different value)

Works for both XML and JSON automatically (format is auto-detected, or can be
forced with format_hint="xml"/"json").

Two entry points are provided:

    compare_responses(text_a, text_b, ...)
        Compares two full raw response bodies (strings). Use this for the
        overall APIM vs IIB response comparison.

    compare_values(actual, expected, ...) / values_match(actual, expected)
        Compares a single extracted value (e.g. from a JSONPath/XPath query
        against a response) with an expected value from a test case file.
        Accepts either raw strings (JSON/XML text) OR already-parsed values
        (dict/list from query_json, xml.etree.ElementTree.Element from
        query_xml, or plain scalars) on either side, auto-detects the
        format from whichever side looks structured, and reuses the same
        namespace/schema/value diffing logic as compare_responses.

Ignoring fields
----------------
Both entry points accept an `ignore_fields` argument: a list/set of field or
element names to exclude from comparison, matched by name at ANY depth in
the document (e.g. ["id", "createdAt"] will skip a top-level "id" key as
well as a nested "meta.id" key). This is meant for volatile fields that are
expected to legitimately differ between calls (server-generated ids,
timestamps, request-correlation ids, etc).

Pass the single value "ALL" (case-insensitive) anywhere in ignore_fields to
skip the comparison entirely - the resulting report will have no
differences and report.skipped will be True.

    from response_comparator import compare_responses, parse_ignore_fields

    ignore_fields = parse_ignore_fields(testcase_row.get("VALIDATE_DATA_TO_IGNORE"))

    report = compare_responses(
        resp_apim.text(), resp_iib.text(),
        label_a="APIM", label_b="IIB",
        ignore_fields=ignore_fields,
    )
    assert not report.has_differences(), report.to_text()

Basic usage
-----------
    from response_comparator import compare_responses

    report = compare_responses(
        resp_iib.text,
        resp_apim.text,
        label_a="IIB",
        label_b="APIM",
    )

    print(report.to_text())

    if report.has_differences():
        # e.g. fail the pytest-bdd step, attach report.to_text() to Allure, etc.
        ...

    # machine-readable form, e.g. for building an Allure attachment or a
    # consolidated per-contract mismatch summary
    report.to_dict()

Single-value usage
-------------------
    from response_comparator import compare_values, values_match

    report = compare_values(actual_value, expected_value, label_a="Actual", label_b="Expected")
    assert not report.has_differences(), report.to_text()

    # or simply:
    assert values_match(actual_value, expected_value)
"""

from __future__ import annotations

import ast
import json
import re
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List, Optional, Set, Tuple, Union

IgnoreFields = Optional[Iterable[str]]

_IGNORE_ALL_SENTINEL = "ALL"


# ---------------------------------------------------------------------------
# Report data structures
# ---------------------------------------------------------------------------

@dataclass
class Difference:
    path: str
    detail: str
    left: Any = None
    right: Any = None

    def to_text(self) -> str:
        lines = [f"  - {self.path}: {self.detail}"]
        if self.left is not None or self.right is not None:
            lines.append(f"      A: {self.left!r}")
            lines.append(f"      B: {self.right!r}")
        return "\n".join(lines)


@dataclass
class ComparisonReport:
    format: str  # "xml", "json", or "scalar"
    label_a: str = "A"
    label_b: str = "B"
    namespace_diffs: List[Difference] = field(default_factory=list)
    schema_diffs: List[Difference] = field(default_factory=list)
    value_diffs: List[Difference] = field(default_factory=list)
    parse_error: Optional[str] = None
    skipped: bool = False
    skip_reason: Optional[str] = None

    def has_differences(self) -> bool:
        if self.skipped:
            return False
        return bool(
            self.namespace_diffs or self.schema_diffs or self.value_diffs or self.parse_error
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "format": self.format,
            "label_a": self.label_a,
            "label_b": self.label_b,
            "parse_error": self.parse_error,
            "skipped": self.skipped,
            "skip_reason": self.skip_reason,
            "namespace_differences": [d.__dict__ for d in self.namespace_diffs],
            "schema_differences": [d.__dict__ for d in self.schema_diffs],
            "value_differences": [d.__dict__ for d in self.value_diffs],
        }

    def to_text(self) -> str:
        if self.skipped:
            return f"SKIPPED: {self.skip_reason}" if self.skip_reason else "SKIPPED"

        if self.parse_error:
            return f"PARSE ERROR: {self.parse_error}"

        lines = [
            f"Comparison report ({self.format.upper()}): {self.label_a} vs {self.label_b}",
            "=" * 60,
        ]

        def section(title: str, diffs: List[Difference]) -> None:
            lines.append(f"\n{title} ({len(diffs)})")
            if not diffs:
                lines.append("  none")
            for d in diffs:
                lines.append(d.to_text())

        section("NAMESPACE DIFFERENCES", self.namespace_diffs)
        section("SCHEMA DIFFERENCES", self.schema_diffs)
        section("VALUE DIFFERENCES", self.value_diffs)

        if not self.has_differences():
            lines.append("\nNo differences found.")
        return "\n".join(lines)


# ---------------------------------------------------------------------------
# Ignore-fields helpers
# ---------------------------------------------------------------------------

def _normalize_ignore_fields(ignore_fields: IgnoreFields) -> Set[str]:
    if not ignore_fields:
        return set()
    return {str(f).strip() for f in ignore_fields if str(f).strip()}


def _is_ignore_all(ignore_fields: Set[str]) -> bool:
    return any(f.upper() == _IGNORE_ALL_SENTINEL for f in ignore_fields)


def parse_ignore_fields(raw_value: Any) -> List[str]:
    """Parse a VALIDATE_DATA_TO_IGNORE-style cell into a list of field names.

    Accepts, and returns [] for, None / NaN / blank. Accepts an already-parsed
    list/tuple/set as-is. For strings, tries in order:
      1. JSON array, e.g.  '["id", "createdAt"]'
      2. Python-literal list (handles single-quoted CSV exports),
         e.g.  "['id', 'createdAt']"
      3. Plain comma-separated text, e.g.  "id, createdAt"  or  "ALL"
    """
    if raw_value is None:
        return []
    if isinstance(raw_value, float):  # pandas NaN for a blank cell
        return []
    if isinstance(raw_value, (list, tuple, set)):
        return [str(v).strip() for v in raw_value if str(v).strip()]

    text = str(raw_value).strip()
    if not text:
        return []

    if text.startswith("["):
        try:
            return [str(v).strip() for v in json.loads(text)]
        except (json.JSONDecodeError, TypeError):
            pass
        try:
            parsed = ast.literal_eval(text)
            if isinstance(parsed, (list, tuple, set)):
                return [str(v).strip() for v in parsed]
        except (ValueError, SyntaxError):
            pass

    return [part.strip() for part in text.split(",") if part.strip()]


# ---------------------------------------------------------------------------
# Entry point: full response body comparison
# ---------------------------------------------------------------------------

def compare_responses(
    text_a: str,
    text_b: str,
    label_a: str = "A",
    label_b: str = "B",
    format_hint: Optional[str] = None,
    ignore_fields: IgnoreFields = None,
) -> ComparisonReport:
    """Compare two response bodies and return a ComparisonReport.

    format_hint: "xml" or "json" to force parsing mode; otherwise auto-detected
    from text_a's leading character.

    ignore_fields: field/element names to skip wherever they occur in the
    document, regardless of nesting depth (e.g. ["id", "createdAt"]). Pass
    "ALL" as one of the entries to skip the comparison entirely.
    """
    ignore_set = _normalize_ignore_fields(ignore_fields)
    fmt = format_hint or _detect_format(text_a)
    report = ComparisonReport(format=fmt, label_a=label_a, label_b=label_b)

    if _is_ignore_all(ignore_set):
        report.skipped = True
        report.skip_reason = "ignore_fields contains 'ALL' - comparison skipped"
        return report

    if fmt == "json":
        _compare_json(text_a, text_b, report, ignore_set)
    else:
        _compare_xml(text_a, text_b, report, ignore_set)

    return report


def _detect_format(text: str) -> str:
    stripped = text.lstrip()
    if stripped.startswith("<"):
        return "xml"
    if stripped.startswith("{") or stripped.startswith("["):
        return "json"
    try:
        json.loads(text)
        return "json"
    except (ValueError, TypeError):
        return "xml"


# ---------------------------------------------------------------------------
# Entry point: single extracted value comparison
# ---------------------------------------------------------------------------

def compare_values(
    actual: Any,
    expected: Any,
    label_a: str = "Actual",
    label_b: str = "Expected",
    ignore_fields: IgnoreFields = None,
) -> ComparisonReport:
    """Compare a single extracted value against an expected value.

    Either side can be:
      - an already-parsed JSON value (dict / list / str / number / bool / None)
      - a JSON string
      - an xml.etree.ElementTree.Element
      - an XML string
      - a plain scalar string

    Format is auto-detected (preferring the expected side, since that's the
    "shape" the test case author intended), then compared using the same
    namespace/schema/value diffing logic as compare_responses.

    ignore_fields: see compare_responses() docstring - useful when the
    queried value is itself an object/element containing volatile
    sub-fields. "ALL" skips the comparison entirely.
    """
    ignore_set = _normalize_ignore_fields(ignore_fields)
    fmt = _detect_value_format(expected)
    if fmt == "scalar":
        # fall back to whichever side does look structured, if any
        fmt = _detect_value_format(actual)

    report = ComparisonReport(format=fmt, label_a=label_a, label_b=label_b)

    if _is_ignore_all(ignore_set):
        report.skipped = True
        report.skip_reason = "ignore_fields contains 'ALL' - comparison skipped"
        return report

    if fmt == "json":
        try:
            obj_a = _to_json_obj(actual)
        except (json.JSONDecodeError, TypeError) as exc:
            report.parse_error = f"{label_a} is not valid JSON: {exc}"
            return report
        try:
            obj_b = _to_json_obj(expected)
        except (json.JSONDecodeError, TypeError) as exc:
            report.parse_error = f"{label_b} is not valid JSON: {exc}"
            return report
        _walk_json(obj_a, obj_b, "$", report, ignore_set)

    elif fmt == "xml":
        try:
            elem_a = _to_xml_element(actual)
        except ET.ParseError as exc:
            report.parse_error = f"{label_a} is not valid XML: {exc}"
            return report
        try:
            elem_b = _to_xml_element(expected)
        except ET.ParseError as exc:
            report.parse_error = f"{label_b} is not valid XML: {exc}"
            return report
        _, root_local = _split_tag(elem_b.tag)
        _compare_elements(elem_a, elem_b, f"/{root_local}", report, ignore_set)

    else:
        str_a = "" if actual is None else str(actual).strip()
        str_b = "" if expected is None else str(expected).strip()
        if str_a != str_b:
            report.value_diffs.append(Difference("$", "value differs", str_a, str_b))

    return report


def values_match(actual: Any, expected: Any, ignore_fields: IgnoreFields = None) -> bool:
    """Convenience boolean wrapper around compare_values()."""
    return not compare_values(actual, expected, ignore_fields=ignore_fields).has_differences()


def _detect_value_format(value: Any) -> str:
    if isinstance(value, (dict, list)):
        return "json"
    if isinstance(value, ET.Element):
        return "xml"
    if isinstance(value, str):
        stripped = value.strip()
        if stripped.startswith("<"):
            return "xml"
        if stripped.startswith("{") or stripped.startswith("["):
            return "json"
    return "scalar"


def _to_json_obj(value: Any) -> Any:
    if isinstance(value, (dict, list)):
        return value
    if isinstance(value, str):
        return json.loads(value)
    return value  # numbers, bool, None pass through as-is


def _to_xml_element(value: Any) -> ET.Element:
    if isinstance(value, ET.Element):
        return value
    if isinstance(value, str):
        return ET.fromstring(value.strip())
    raise ET.ParseError(f"cannot parse XML from value of type {type(value).__name__}")


# ---------------------------------------------------------------------------
# JSON comparison
# ---------------------------------------------------------------------------

def _compare_json(
    text_a: str,
    text_b: str,
    report: ComparisonReport,
    ignore_fields: Set[str] = frozenset(),
) -> None:
    try:
        obj_a = json.loads(text_a)
    except json.JSONDecodeError as exc:
        report.parse_error = f"{report.label_a} is not valid JSON: {exc}"
        return
    try:
        obj_b = json.loads(text_b)
    except json.JSONDecodeError as exc:
        report.parse_error = f"{report.label_b} is not valid JSON: {exc}"
        return

    _walk_json(obj_a, obj_b, "$", report, ignore_fields)


def _json_type_name(value: Any) -> str:
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "boolean"
    if isinstance(value, (int, float)):
        return "number"
    if isinstance(value, str):
        return "string"
    if isinstance(value, list):
        return "array"
    if isinstance(value, dict):
        return "object"
    return type(value).__name__


def _walk_json(
    a: Any,
    b: Any,
    path: str,
    report: ComparisonReport,
    ignore_fields: Set[str] = frozenset(),
) -> None:
    type_a, type_b = _json_type_name(a), _json_type_name(b)

    if type_a != type_b:
        report.schema_diffs.append(
            Difference(path, f"type mismatch ({type_a} vs {type_b})", a, b)
        )
        return

    if type_a == "object":
        keys_a, keys_b = set(a.keys()), set(b.keys())
        for key in sorted(keys_a - keys_b):
            if key in ignore_fields:
                continue
            report.schema_diffs.append(
                Difference(f"{path}.{key}", f"present only in {report.label_a}", a[key], None)
            )
        for key in sorted(keys_b - keys_a):
            if key in ignore_fields:
                continue
            report.schema_diffs.append(
                Difference(f"{path}.{key}", f"present only in {report.label_b}", None, b[key])
            )
        for key in sorted(keys_a & keys_b):
            if key in ignore_fields:
                continue
            _walk_json(a[key], b[key], f"{path}.{key}", report, ignore_fields)

    elif type_a == "array":
        if len(a) != len(b):
            report.schema_diffs.append(
                Difference(path, f"array length differs ({len(a)} vs {len(b)})", len(a), len(b))
            )
        for i in range(min(len(a), len(b))):
            _walk_json(a[i], b[i], f"{path}[{i}]", report, ignore_fields)

    else:
        if a != b:
            report.value_diffs.append(Difference(path, "value differs", a, b))


# ---------------------------------------------------------------------------
# XML comparison
# ---------------------------------------------------------------------------

_NS_DECL_RE = re.compile(r'xmlns(:(?P<prefix>[\w.\-]+))?\s*=\s*"(?P<uri>[^"]*)"')


def _extract_namespace_declarations(text: str) -> Dict[str, str]:
    """Returns {prefix_or_'(default)': uri} for every xmlns declaration in the raw text."""
    decls: Dict[str, str] = {}
    for m in _NS_DECL_RE.finditer(text):
        prefix = m.group("prefix") or "(default)"
        decls[prefix] = m.group("uri")
    return decls


def _compare_namespace_declarations(text_a: str, text_b: str, report: ComparisonReport) -> None:
    ns_a = _extract_namespace_declarations(text_a)
    ns_b = _extract_namespace_declarations(text_b)

    for prefix in sorted(set(ns_a) - set(ns_b)):
        report.namespace_diffs.append(
            Difference(f"xmlns:{prefix}", f"declared only in {report.label_a}", ns_a[prefix], None)
        )
    for prefix in sorted(set(ns_b) - set(ns_a)):
        report.namespace_diffs.append(
            Difference(f"xmlns:{prefix}", f"declared only in {report.label_b}", None, ns_b[prefix])
        )
    for prefix in sorted(set(ns_a) & set(ns_b)):
        if ns_a[prefix] != ns_b[prefix]:
            report.namespace_diffs.append(
                Difference(f"xmlns:{prefix}", "prefix bound to a different URI", ns_a[prefix], ns_b[prefix])
            )


def _split_tag(tag: str) -> Tuple[str, str]:
    """'{uri}local' -> (uri, local); 'local' -> ('', local)."""
    if tag.startswith("{"):
        uri, local = tag[1:].split("}", 1)
        return uri, local
    return "", tag


def _build_children_index(element: ET.Element) -> Dict[str, List[ET.Element]]:
    idx: Dict[str, List[ET.Element]] = {}
    for child in element:
        _, local = _split_tag(child.tag)
        idx.setdefault(local, []).append(child)
    return idx


def _compare_attributes(
    attrs_a: Dict[str, str],
    attrs_b: Dict[str, str],
    path: str,
    report: ComparisonReport,
    ignore_fields: Set[str] = frozenset(),
) -> None:
    def split_attr(name: str) -> Tuple[str, str]:
        return _split_tag(name) if name.startswith("{") else ("", name)

    norm_a = {split_attr(k)[1]: (split_attr(k)[0], v) for k, v in attrs_a.items()}
    norm_b = {split_attr(k)[1]: (split_attr(k)[0], v) for k, v in attrs_b.items()}

    for name in sorted(set(norm_a) - set(norm_b)):
        if name in ignore_fields:
            continue
        report.schema_diffs.append(
            Difference(f"{path}/@{name}", f"attribute present only in {report.label_a}", norm_a[name][1], None)
        )
    for name in sorted(set(norm_b) - set(norm_a)):
        if name in ignore_fields:
            continue
        report.schema_diffs.append(
            Difference(f"{path}/@{name}", f"attribute present only in {report.label_b}", None, norm_b[name][1])
        )
    for name in sorted(set(norm_a) & set(norm_b)):
        if name in ignore_fields:
            continue
        uri_a, val_a = norm_a[name]
        uri_b, val_b = norm_b[name]
        if uri_a != uri_b:
            report.namespace_diffs.append(
                Difference(f"{path}/@{name}", "attribute namespace differs", uri_a or "(none)", uri_b or "(none)")
            )
        if val_a != val_b:
            report.value_diffs.append(Difference(f"{path}/@{name}", "attribute value differs", val_a, val_b))


def _compare_elements(
    elem_a: ET.Element,
    elem_b: ET.Element,
    path: str,
    report: ComparisonReport,
    ignore_fields: Set[str] = frozenset(),
) -> None:
    uri_a, _ = _split_tag(elem_a.tag)
    uri_b, _ = _split_tag(elem_b.tag)

    if uri_a != uri_b:
        report.namespace_diffs.append(
            Difference(path, "element uses a different namespace URI", uri_a or "(none)", uri_b or "(none)")
        )

    _compare_attributes(elem_a.attrib, elem_b.attrib, path, report, ignore_fields)

    text_a = (elem_a.text or "").strip()
    text_b = (elem_b.text or "").strip()
    if text_a != text_b:
        report.value_diffs.append(Difference(path, "element text differs", text_a, text_b))

    children_a = _build_children_index(elem_a)
    children_b = _build_children_index(elem_b)

    for local in sorted(set(children_a) - set(children_b)):
        if local in ignore_fields:
            continue
        report.schema_diffs.append(
            Difference(
                f"{path}/{local}",
                f"element present only in {report.label_a}",
                f"{len(children_a[local])} occurrence(s)",
                None,
            )
        )
    for local in sorted(set(children_b) - set(children_a)):
        if local in ignore_fields:
            continue
        report.schema_diffs.append(
            Difference(
                f"{path}/{local}",
                f"element present only in {report.label_b}",
                None,
                f"{len(children_b[local])} occurrence(s)",
            )
        )

    for local in sorted(set(children_a) & set(children_b)):
        if local in ignore_fields:
            continue
        list_a, list_b = children_a[local], children_b[local]
        if len(list_a) != len(list_b):
            report.schema_diffs.append(
                Difference(
                    f"{path}/{local}",
                    f"occurrence count differs ({len(list_a)} vs {len(list_b)})",
                    len(list_a),
                    len(list_b),
                )
            )
        for i in range(min(len(list_a), len(list_b))):
            suffix = f"[{i}]" if len(list_a) > 1 or len(list_b) > 1 else ""
            _compare_elements(list_a[i], list_b[i], f"{path}/{local}{suffix}", report, ignore_fields)


def _compare_xml(
    text_a: str,
    text_b: str,
    report: ComparisonReport,
    ignore_fields: Set[str] = frozenset(),
) -> None:
    _compare_namespace_declarations(text_a, text_b, report)

    try:
        root_a = ET.fromstring(text_a)
    except ET.ParseError as exc:
        report.parse_error = f"{report.label_a} is not valid XML: {exc}"
        return
    try:
        root_b = ET.fromstring(text_b)
    except ET.ParseError as exc:
        report.parse_error = f"{report.label_b} is not valid XML: {exc}"
        return

    _, root_local_a = _split_tag(root_a.tag)
    _compare_elements(root_a, root_b, f"/{root_local_a}", report, ignore_fields)
