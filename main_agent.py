#!/usr/bin/env python3
"""
main_agent.py
Pipeline:
  prompt -> generate spec (intentionally flawed) -> evaluate -> score -> optional RL -> merged output
Creates:
  - prompt_logs/spec_*.json
  - evaluations/eval_*.json
  - rl_logs/rl_*.json (if --simulate)
  - sample_outputs/single_*.json (merged: spec + eval + score + RL content)
"""
import argparse
import json
import os
from datetime import datetime
import random

from evaluator_agent import evaluate_spec, save_evaluation
from data_scorer import score_spec
from rl_loop import run_episode

ROOT = os.path.dirname(os.path.abspath(__file__))

def _ts():  # timestamp string
    return datetime.now().strftime("%Y%m%d_%H%M%S")

def _ensure_dirs():
    for d in ("prompt_logs", "evaluations", "rl_logs", "sample_outputs"):
        os.makedirs(os.path.join(ROOT, d), exist_ok=True)

def _save_json(obj, folder, prefix):
    path = os.path.join(ROOT, folder, f"{prefix}_{_ts()}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2)
    return path

# ---------- Spec Generator (guarantees at least one flaw) ----------
def generate_spec_from_prompt(prompt: str) -> dict:
    """
    Stubbed generator that ALWAYS injects at least one flaw so the RL loop has work.
    Flaws: missing/incomplete dimensions (for buildings), or unknown materials.
    """
    lower = prompt.lower()
    spec = {
        "prompt": prompt,
        "generated_by": "stub_generator",
        "created_at": datetime.now().isoformat(),
    }

    is_building_prompt = any(w in lower for w in ["library", "building", "house", "office", "school", "museum", "center"])
    if is_building_prompt:
        spec["type"] = "building"
        spec["floors"] = 2 if any(k in lower for k in ["2-floor", "2 floor", "two-floor", "two floor", "2"]) else 1

        # Guarantee at least one flaw:
        # (a) 50%: remove dimensions entirely; (b) otherwise: add incomplete dimensions
        if random.random() < 0.5:
            # No dimensions at all (flaw)
            pass
        else:
            spec["dimensions_m"] = {"per_floor": {"length": 12.0}}  # incomplete (flaw)

        # Always include one unknown material (flaw)
        spec["materials"] = ["bamboo", "unobtainium"]

        # Basic content
        spec["rooms"] = [
            {"name": "reading_hall", "area_m2": 50},
            {"name": "stacks", "area_m2": 20}
        ]
    else:
        spec["type"] = "mechanical"
        spec["parts"] = [
            {"name": "base", "material": "steel", "dimensions_mm": {"l": 200, "w": 100, "h": 20}},
            {"name": "shaft", "material": "adamantium", "dimensions_mm": {"l": 150, "dia": 20}}  # unknown material (flaw)
        ]
        spec["materials"] = ["steel", "adamantium"]  # unknown material (flaw)

    spec["notes"] = "Machine-generated with intentional flaws so RL loop can demonstrate fixes."
    return spec

def _merge_and_save(prompt, spec, eval_result, score_result, rl_path=None, prefix="single"):
    merged = {"prompt": prompt, "spec": spec, "evaluation": eval_result, "score": score_result}
    if rl_path:
        try:
            with open(rl_path, "r", encoding="utf-8") as f:
                merged["rl_log"] = json.load(f)
        except Exception as e:
            merged["rl_log"] = {"error": f"Could not load RL log: {e}", "path": rl_path}

    out_path = os.path.join(ROOT, "sample_outputs", f"{prefix}_{_ts()}.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(merged, f, indent=2)
    return out_path

def main():
    _ensure_dirs()
    parser = argparse.ArgumentParser(description="Prompt -> Spec -> Evaluate -> Score -> (optional RL) -> Merge")
    parser.add_argument("--prompt", type=str, help="Prompt text (wrap in quotes)")
    parser.add_argument("--simulate", action="store_true", help="Run RL improvement loop")
    args = parser.parse_args()

    prompt = args.prompt.strip() if args.prompt else input("Enter your prompt: ").strip()
    if not prompt:
        print("No prompt provided. Exiting.")
        return

    # Generate flawed spec
    spec = generate_spec_from_prompt(prompt)
    spec_path = _save_json(spec, "prompt_logs", "spec")
    print("Spec saved to:", spec_path)

    # Evaluate + Score
    eval_result = evaluate_spec(prompt, spec)
    eval_path = save_evaluation(eval_result, tag="eval")
    print("Evaluation saved to:", eval_path)

    score_result = score_spec(prompt, spec)
    print("Score:", score_result)

    # Optional RL loop
    rl_path = None
    if args.simulate:
        print("DEBUG: RL loop starting for prompt:", prompt)
        rl_path = run_episode(prompt, spec, max_steps=3)
        print("DEBUG: RL loop finished:", rl_path)

    merged_path = _merge_and_save(prompt, spec, eval_result, score_result, rl_path, prefix="single")
    print("Merged output saved to:", merged_path)

if __name__ == "__main__":
    main()
