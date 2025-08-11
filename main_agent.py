#!/usr/bin/env python3
"""
main_agent.py
Orchestrator:
 - generates a spec JSON from a prompt (stub or real model)
 - saves to prompt_logs/
 - calls evaluator_agent.evaluate_spec(...)
 - calls data_scorer.score_spec(...)
 - logs RL step via rl_loop (single step or simulate)
"""
import os
import sys
import json
import argparse
from datetime import datetime
import random

# Ensure module imports work when running scripts from different CWDs
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from evaluator_agent import evaluate_spec, save_evaluation  # local module
from data_scorer import score_spec
from rl_loop import run_episode

ROOT = os.path.dirname(os.path.abspath(__file__))

def ensure_dirs():
    for d in ("prompt_logs", "evaluations", "rl_logs", "sample_outputs"):
        path = os.path.join(ROOT, d)
        os.makedirs(path, exist_ok=True)

def timestamp():
    return datetime.now().strftime("%Y%m%d_%H%M%S")

def generate_spec_from_prompt(prompt: str, use_stub=True):
    """
    Simple stubbed spec generator. Replace with LLM call if desired.
    """
    lower = prompt.lower()
    spec = {
        "prompt": prompt,
        "generated_by": "stub_generator",
        "created_at": datetime.now().isoformat(),
    }

    # simple type detection
    if any(w in lower for w in ["library", "building", "house", "office", "school"]):
        spec["type"] = "building"
        # floors detection
        if "2-floor" in lower or "2 floor" in lower or "two-floor" in lower:
            floors = 2
        else:
            floors = 1 if "single" in lower or "one-floor" in lower else 2 if "two" in lower else 1
        spec["floors"] = floors
        # dimensions (stubbed) per floor
        spec["dimensions_m"] = {
            "per_floor": {
                "length": 12.0,
                "width": 8.0,
                "height": 3.0
            },
            "total_height": floors * 3.0
        }
        # room list for a library
        spec["rooms"] = [
            {"name": "reading_hall", "area_m2": 50},
            {"name": "stacks", "area_m2": 20},
            {"name": "toilet", "area_m2": 6},
            {"name": "staircase", "area_m2": 8}
        ]
        # materials
        if "eco" in lower or "eco-friendly" in lower or "sustainable" in lower:
            spec["materials"] = ["bamboo", "recycled_wood", "low-E_glass"]
        else:
            spec["materials"] = ["concrete", "brick", "glass"]
    else:
        # fallback mechanical spec
        spec["type"] = "mechanical"
        spec["parts"] = [
            {"name": "base", "material": "steel", "dimensions_mm": {"l": 200, "w": 100, "h": 20}},
            {"name": "shaft", "material": "steel", "dimensions_mm": {"l": 150, "dia": 20}}
        ]
        spec["materials"] = ["steel", "aluminum"]

    # add some metadata
    spec["notes"] = "This spec is machine-generated stub. Replace generator with LLM for richer outputs."
    return spec

def save_json(obj, folder, prefix):
    fn = f"{prefix}_{timestamp()}.json"
    path = os.path.join(ROOT, folder, fn)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2)
    return path

def main():
    ensure_dirs()
    parser = argparse.ArgumentParser(description="Prompt -> Spec orchestrator")
    parser.add_argument("--prompt", type=str, help="Prompt text (wrap in quotes)")
    parser.add_argument("--prompt_file", type=str, help="Read prompt from a file")
    parser.add_argument("--simulate", action="store_true", help="Run RL episode (attempt fixes) after generation")
    args = parser.parse_args()

    if not args.prompt and not args.prompt_file:
        print("Provide --prompt or --prompt_file")
        return

    if args.prompt_file:
        with open(args.prompt_file, "r", encoding="utf-8") as f:
            prompt = f.read().strip()
    else:
        prompt = args.prompt.strip()

    print("Prompt:", prompt)
    spec = generate_spec_from_prompt(prompt, use_stub=True)
    spec_path = save_json(spec, "prompt_logs", "spec")
    print("Spec generated and saved to:", spec_path)

    # Evaluate
    eval_result = evaluate_spec(prompt, spec)  # returns dict with 'critic_feedback' etc.
    eval_path = save_evaluation(eval_result, tag="eval")
    print("Evaluation saved to:", eval_path)

    # Score
    score_result = score_spec(prompt, spec)
    print("Spec scoring result:", score_result)

    # RL step / simulation
    if args.simulate:
        rl_log_path = run_episode(prompt, spec, max_steps=3)
        print("RL episode logged to:", rl_log_path)
    else:
        # Write a single RL log entry summarizing this attempt
        # simple reward rule: reward = 1 if no "issues" in eval
        reward = 1 if "no major issues" in eval_result.get("critic_feedback", "").lower() else -1
        rl_entry = {
            "prompt": prompt,
            "spec_path": spec_path,
            "eval_path": eval_path,
            "score": score_result,
            "critic_feedback": eval_result.get("critic_feedback"),
            "reward": reward,
            "timestamp": datetime.now().isoformat()
        }
        rl_path = save_json(rl_entry, "rl_logs", "rl")
        print("RL log (single step) saved to:", rl_path)
        print("Final reward:", reward)

if __name__ == "__main__":
    main()
