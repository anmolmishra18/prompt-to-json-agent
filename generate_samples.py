#!/usr/bin/env python3
"""
generate_samples.py
Takes at least 1 prompt from user, runs pipeline immediately,
and saves one merged output file per prompt in sample_outputs/.
"""
import os
import json
from main_agent import ensure_dirs, generate_spec_from_prompt, save_json
from evaluator_agent import evaluate_spec, save_evaluation
from data_scorer import score_spec
from rl_loop import run_episode

ROOT = os.path.dirname(os.path.abspath(__file__))
SAMPLES_FOLDER = os.path.join(ROOT, "sample_outputs")

def save_merged_output(prompt, spec, eval_result, score_result, rl_path, index):
    """Create one combined JSON file in sample_outputs/."""
    merged = {
        "prompt": prompt,
        "spec": spec,
        "evaluation": eval_result,
        "score": score_result,
        "rl_log_file": os.path.basename(rl_path)
    }
    os.makedirs(SAMPLES_FOLDER, exist_ok=True)
    merged_path = os.path.join(SAMPLES_FOLDER, f"sample_{index}.json")
    with open(merged_path, "w", encoding="utf-8") as f:
        json.dump(merged, f, indent=2)
    print(f"✅ Merged output saved to: {merged_path}")

def generate_for_prompt(prompt: str, index: int):
    """Run the pipeline for one prompt and save merged output."""
    print(f"\n=== Example {index}: {prompt} ===")
    # Generate spec
    spec = generate_spec_from_prompt(prompt, use_stub=True)
    spec_path = save_json(spec, "prompt_logs", f"spec_ex{index}")
    print("Spec saved to:", spec_path)

    # Evaluate
    eval_result = evaluate_spec(prompt, spec)
    eval_path = save_evaluation(eval_result, tag=f"eval_ex{index}")
    print("Evaluation saved to:", eval_path)

    # Score
    score_result = score_spec(prompt, spec)
    print("Score:", score_result)

    # RL improvement loop
    rl_path = run_episode(prompt, spec, max_steps=3)
    print("RL log saved to:", rl_path)

    # Save merged output
    save_merged_output(prompt, spec, eval_result, score_result, rl_path, index)

def main():
    ensure_dirs()
    os.makedirs(SAMPLES_FOLDER, exist_ok=True)

    print("Enter at least 1 prompt (type 'done' to finish).")
    index = 1
    while True:
        user_input = input(f"Prompt {index}: ").strip()
        if user_input.lower() == "done":
            if index == 1:
                print("⚠ You must enter at least one prompt before finishing.")
                continue
            else:
                break
        if user_input:
            generate_for_prompt(user_input, index)
            index += 1

    print(f"\n✅ Processed {index-1} prompts.")
    print(f"Outputs are in: {SAMPLES_FOLDER}")

if __name__ == "__main__":
    main()
