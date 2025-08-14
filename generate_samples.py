#!/usr/bin/env python3
"""
generate_samples.py
Batch runner for at least 1 prompt.
Creates one merged JSON per prompt in sample_outputs/ with full RL content embedded.
"""
import json
import os
from datetime import datetime

from main_agent import generate_spec_from_prompt
from evaluator_agent import evaluate_spec, save_evaluation
from data_scorer import score_spec
from rl_loop import run_episode

ROOT = os.path.dirname(os.path.abspath(__file__))
SAMPLES_DIR = os.path.join(ROOT, "sample_outputs")
for d in ("prompt_logs", "evaluations", "rl_logs", "sample_outputs"):
    os.makedirs(os.path.join(ROOT, d), exist_ok=True)

def _save_json(obj, folder, prefix):
    path = os.path.join(ROOT, folder, f"{prefix}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2)
    return path

def _merge_and_save(prompt, spec, eval_result, score_result, rl_path, index):
    try:
        with open(rl_path, "r", encoding="utf-8") as f:
            rl_content = json.load(f)
    except Exception as e:
        rl_content = {"error": f"Could not load RL log: {e}", "path": rl_path}

    merged = {
        "prompt": prompt,
        "spec": spec,
        "evaluation": eval_result,
        "score": score_result,
        "rl_log": rl_content
    }
    out_path = os.path.join(SAMPLES_DIR, f"sample_{index}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(merged, f, indent=2)
    print(f"✅ Merged output saved to: {out_path}")

def main():
    print("Enter prompts (type 'done' when finished). Minimum 1 prompt.")
    idx = 1
    while True:
        p = input(f"Prompt {idx}: ").strip()
        if p.lower() == "done":
            if idx == 1:
                print("⚠ Please enter at least one prompt before finishing.")
                continue
            break
        if not p:
            print("⚠ Empty prompt ignored.")
            continue

        spec = generate_spec_from_prompt(p)
        spec_path = _save_json(spec, "prompt_logs", f"spec_ex{idx}")
        print("Spec saved to:", spec_path)

        eval_result = evaluate_spec(p, spec)
        eval_path = save_evaluation(eval_result, tag=f"eval_ex{idx}")
        print("Evaluation saved to:", eval_path)

        score_result = score_spec(p, spec)
        print("Score:", score_result)

        rl_path = run_episode(p, spec, max_steps=3)
        print("RL log saved to:", rl_path)

        _merge_and_save(p, spec, eval_result, score_result, rl_path, idx)
        idx += 1

    print(f"\n✅ Done. Created {idx-1} merged files in: {SAMPLES_DIR}")

if __name__ == "__main__":
    main()
