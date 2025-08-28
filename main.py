import os
import sys
import json
import argparse
from datetime import datetime

from evaluator.criteria import score_spec
from evaluator.feedback import suggest_fixes, apply_feedback
from evaluator.report import generate_report


def ensure_dir(path: str):
    if not os.path.exists(path):
        os.makedirs(path)


def timestamp():
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def load_sample(path: str):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def parse_prompt(prompt: str):
    """
    Parse a structured 'Title:..., Description:..., Owner:..., Requirements:...' prompt
    or treat free text as description.
    """
    spec = {"priority": "medium"}  # default priority
    lowered = prompt.lower()
    if "title:" in lowered or "description:" in lowered or "owner:" in lowered or "requirements:" in lowered:
        for part in prompt.split(";"):
            if ":" in part:
                key, val = part.split(":", 1)
                spec[key.strip().lower()] = val.strip()
    else:
        # Free text fallback
        spec["description"] = prompt
        spec["title"] = prompt[:30]
        spec["requirements"] = ["basic validation", "report generation"]

    # normalize requirements
    if isinstance(spec.get("requirements"), str):
        spec["requirements"] = [r.strip() for r in spec["requirements"].split(",")]

    return spec


def run_pipeline(spec: dict, iterations: int, outdir_reports="reports", outdir_logs="logs"):
    """
    Run the evaluator + feedback loop for a number of iterations.
    Saves reports and logs.
    Returns (final_spec, history).
    """
    ensure_dir(outdir_reports)
    ensure_dir(outdir_logs)

    history = []

    print("\n[INFO] Initial Parsed JSON")
    print(json.dumps(spec, indent=4))

    for i in range(1, iterations + 1):
        score, details = score_spec(spec)
        suggestions = suggest_fixes(spec, score, details)

        history.append({
            "iteration": i,
            "score": score,
            "details": details,
            "spec": spec,
            "suggestions": suggestions
        })

        # Save reports
        generate_report(spec, score, details, outdir_reports, iteration=i)

        if not suggestions:
            break

        spec = apply_feedback(spec, suggestions)

    # Save feedback log
    logpath = os.path.join(outdir_logs, f"feedback_log_{timestamp()}.json")
    with open(logpath, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=4)

    print(f"\n[SUCCESS] Reports saved in '{outdir_reports}/', logs saved in '{logpath}'")

    print("\n[SUCCESS] Final Spec after Feedback Loop")
    print(json.dumps(spec, indent=4))

    # 🔹 Return both spec and history
    return spec, history


def append_daily_log(honesty: str, discipline: str, gratitude: str, integrity: str = None, outdir: str = "reports"):
    """
    Append a daily values log entry into /reports/daily_log.txt.
    """
    ensure_dir(outdir)
    log_path = os.path.join(outdir, "daily_log.txt")
    ts = timestamp()

    with open(log_path, "a", encoding="utf-8") as f:
        f.write(f"=== {ts} ===\n")
        if integrity:
            f.write(f"Integrity: {integrity}\n")
        f.write(f"Honesty: {honesty}\n")
        f.write(f"Discipline: {discipline}\n")
        f.write(f"Gratitude: {gratitude}\n\n")

    print(f"Daily log updated -> {log_path}")


def refine_spec(spec: dict, iterations: int = 3):
    """
    Simple wrapper for app.py (Streamlit UI).
    Runs the feedback loop and returns the refined spec.
    """
    final_spec, _ = run_pipeline(spec, iterations)
    return final_spec


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--prompt", type=str, help="Structured or free-text prompt")
    parser.add_argument("--sample", type=str, help="Path to a sample JSON file")
    parser.add_argument("--iterations", type=int, default=3, help="Number of refinement iterations")
    args = parser.parse_args()

    if not args.prompt and not args.sample:
        print("[ERROR] Please provide either --prompt or --sample")
        sys.exit(1)

    if args.sample:
        try:
            spec = load_sample(args.sample)
        except Exception as e:
            print(f"[ERROR] Failed to load sample {args.sample}: {e}")
            sys.exit(1)
    else:
        spec = parse_prompt(args.prompt)

    final_spec, history = run_pipeline(spec, args.iterations)

    # === Values Log ===
    append_daily_log(
        honesty="Today I tested the full Task 3 pipeline, integrated evaluator + feedback, and verified reports/logs.",
        discipline="Kept code structured in evaluator/, wrote clean commit messages, and updated Read.md.",
        gratitude="Grateful for having completed all Task 3 steps with working CLI + UI + reports.",
        integrity="Submitted the work honestly without skipping compulsory steps."
    )


if __name__ == "__main__":
    main()
