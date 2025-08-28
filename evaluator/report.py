"""
report.py – Generate JSON and TXT evaluation reports
"""

import os
import json
from datetime import datetime


def ensure_dir(path: str):
    if not os.path.exists(path):
        os.makedirs(path)


def timestamp():
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def generate_report(spec: dict, score: int, details: dict, outdir: str, iteration: int = None):
    """
    Generate both JSON and TXT reports for a given iteration.

    Args:
        spec: Current JSON spec
        score: Numeric evaluator score
        details: Dict with evaluator details
        outdir: Directory to save reports
        iteration: Iteration number (optional, default None)
    """
    ensure_dir(outdir)
    ts = timestamp()

    # File base name (different if iteration is provided)
    if iteration is not None:
        base = f"report_iter{iteration}_{ts}"
    else:
        base = f"report_final_{ts}"

    report_json = os.path.join(outdir, base + ".json")
    report_txt = os.path.join(outdir, base + ".txt")

    # Save JSON report
    with open(report_json, "w", encoding="utf-8") as f:
        json.dump({
            "spec": spec,
            "score": score,
            "details": details,
            "iteration": iteration
        }, f, indent=4)

    # Save TXT report
    with open(report_txt, "w", encoding="utf-8") as f:
        f.write(f"=== Report {'Iteration ' + str(iteration) if iteration else 'Final'} ===\n")
        f.write(f"Score: {score}\n\n")
        f.write("Details:\n")
        f.write(json.dumps(details, indent=4))
        f.write("\n\nSpec:\n")
        f.write(json.dumps(spec, indent=4))

    return report_json, report_txt
