from pathlib import Path
from jinja2 import Environment, FileSystemLoader
from tools.test_result_coverage.extractor import ReportSummary, TestRecord


def _build_payload(records: list[TestRecord], summary: ReportSummary) -> dict:
    """Build up the JSON payload used in the HTML page

    Args:
        records: Extracted test records
        summary: summary metrics

    Returns:
        Dictionary information of records, summary, and meta data
    """
    return {
        "records": [record.serialize() for record in records],
        "summary": {
            "passed": summary.passed,
            "failed": summary.failed,
            "skipped": summary.skipped,
            "total": summary.total,
            "collected": summary.collected,
        },
        "meta": {"created": summary.created, "duration": summary.duration, "exitcode": summary.exitcode},
    }


def render_html(
    records: list[TestRecord], summary: ReportSummary, output_path: Path, templates_dir: Path | None = None
) -> Path:
    """Render the self-contained results page

    Args:
        records: Extracted test records
        summary: Report-wide summary metrics
        output_path: Target path for the HTML page
        templates_dir: Path of the template directory

    Returns:
        The path of the written HTML file.
    """
    if templates_dir is None:
        templates_dir = Path(__file__).parent / "templates"

    env = Environment(loader=FileSystemLoader(str(templates_dir)), autoescape=True)
    template = env.get_template("results.html")
    payload = _build_payload(records, summary)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(template.render(payload=payload), encoding="utf-8")
    return output_path
