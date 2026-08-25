"""
Helpers for enriching Allure reports on APIM vs IIB comparison failures:
classification of the failure(s) and a side-by-side HTML diff.
"""
import difflib
import html
import json
import re


# --------------------------------------------------------------------------
# Failure classification
# --------------------------------------------------------------------------
_CLASSIFICATION_PATTERNS = [
    ("Missing Field", re.compile(r"\bmissing\b", re.I)),
    ("Extra/Unexpected Field", re.compile(r"\b(extra|unexpected|added)\b", re.I)),
    ("Namespace Difference", re.compile(r"\bnamespace\b", re.I)),
    ("Type Mismatch", re.compile(r"\btype\b", re.I)),
    ("Ordering Difference", re.compile(r"\border(ing)?\b", re.I)),
]


def classify_differences(diff_text: str) -> str:
    """Best-effort classification based on keywords in the diff report text.
    If response_comparator exposes structured diff objects, this should be
    swapped to read those directly for more accurate classification.
    """
    if not diff_text or not diff_text.strip():
        return "Differences detected but no details were returned by the comparator."

    counts = {}
    for line in diff_text.splitlines():
        line = line.strip()
        if not line:
            continue
        matched_label = None
        for label, pattern in _CLASSIFICATION_PATTERNS:
            if pattern.search(line):
                matched_label = label
                break
        label = matched_label or "Value Mismatch"
        counts[label] = counts.get(label, 0) + 1

    lines = ["Failure classification summary:"]
    for label, count in sorted(counts.items(), key=lambda x: -x[1]):
        lines.append(f"  - {label}: {count} occurrence(s)")
    return "\n".join(lines)


# --------------------------------------------------------------------------
# Side-by-side HTML diff
# --------------------------------------------------------------------------
def _pretty(text: str) -> str:
    """Pretty-print JSON if possible; otherwise return as-is (XML/plain)."""
    try:
        return json.dumps(json.loads(text), indent=2, sort_keys=True)
    except (ValueError, TypeError):
        return text


def build_side_by_side_html(iib_text: str, apim_text: str) -> str:
    iib_lines = _pretty(iib_text).splitlines()
    apim_lines = _pretty(apim_text).splitlines()

    matcher = difflib.SequenceMatcher(None, iib_lines, apim_lines)
    rows = []
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == "equal":
            for a, b in zip(iib_lines[i1:i2], apim_lines[j1:j2]):
                rows.append((a, b, False))
        else:
            span = max(i2 - i1, j2 - j1)
            a_slice = iib_lines[i1:i2] + [""] * (span - (i2 - i1))
            b_slice = apim_lines[j1:j2] + [""] * (span - (j2 - j1))
            for a, b in zip(a_slice, b_slice):
                rows.append((a, b, True))

    row_html = []
    for a, b, is_diff in rows:
        style = ' style="background-color:#ffdada;"' if is_diff else ""
        row_html.append(
            f"<tr{style}><td>{html.escape(a)}</td><td>{html.escape(b)}</td></tr>"
        )

    return f"""<html><head><style>
        table {{ border-collapse: collapse; width: 100%; font-family: monospace; font-size: 12px; }}
        td, th {{ border: 1px solid #ccc; padding: 4px 8px; vertical-align: top; white-space: pre-wrap; }}
        th {{ background-color: #f0f0f0; text-align: left; position: sticky; top: 0; }}
    </style></head><body>
    <table>
        <tr><th>IIB Response</th><th>APIM Response</th></tr>
        {''.join(row_html)}
    </table>
    </body></html>"""