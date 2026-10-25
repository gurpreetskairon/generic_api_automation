import logging
import shutil
from pathlib import Path
from tools.test_result_coverage.extractor import parse_report
from tools.test_result_coverage.renderer import render_html

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

ROOT = Path(__file__).resolve().parents[2]

INPUT_FILE = ROOT / "report.json"
OUTPUT_FILE = ROOT / "coverage-report/results_coverage.html"
OUT_FOLDER = ROOT / "coverage-report"
PNG_FILE = ROOT / "tools/test_result_coverage/coverage.png"
CSS_FILE = ROOT / "tools/test_result_coverage/templates/results_style.css"


def main() -> None:
    logger.info(f"Parsing report from {INPUT_FILE}")
    records, summary = parse_report(INPUT_FILE)
    logger.info(f"Extracted {len(records)} test records (passed={summary.passed}, failed={summary.failed})")

    logger.info("Generating a HTML report")
    written = render_html(records, summary, OUTPUT_FILE)
    logger.info(f"Report generated at location: {written}")

    shutil.copy2(PNG_FILE, OUT_FOLDER)
    logger.info("The png file is copied")

    shutil.copy2(CSS_FILE, OUT_FOLDER)
    logger.info("The css style file is copied")


if __name__ == "__main__":
    main()
