#!/usr/bin/env python3
"""
evaluator_agent.py
Simple evaluator/critic agent (stub). It inspects the spec and returns a critique.
Replace the stub with a real LLM call as needed.
"""
import os
import sys
import json
from datetime import datetime

# ensure imports when run from different cwd
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(os.path.abspath(__file__))

def timestamp():
    return datetime.now().strftime("%Y%m%d_%H%M%S")

def save_evaluation(eval_obj, tag="eval"):
    folder = os.path.join(ROOT, "evaluations")
    os.makedirs(folder, exist_ok=True)
    fn = f"{tag}_{timestamp()}.json"
    path = os.path.join(folder, fn)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(eval_obj, f, indent=2)
    return path

def evaluate_spec(prompt: str, spec: dict) -> dict:
    """
    Very simple rule-based evaluator that returns critic feedback.
    """
    issues = []
    # Check dimensions for buildings
    if spec.get("type") == "building":
        dims = spec.get("dimensions_m")
        if not dims or not isinstance(dims, dict):
            issues.append("Missing dimensions for building.")
        else:
            per_floor = dims.get("per_floor")
            if not per_floor or not all(k in per_floor for k in ("length", "width", "height")):
                issues.append("Incomplete per-floor dimensions (length/width/height).")

    # Check materials against a small known set
    known_materials = {"bamboo", "wood", "steel", "concrete", "glass", "brick", "aluminum", "recycled_wood", "low-e_glass", "low-E_glass"}
    materials = spec.get("materials", [])
    if materials:
        unknown = [m for m in materials if m.lower() not in known_materials]
        if unknown:
            issues.append(f"Unrecognized or unusual materials: {unknown}")

    # Type / prompt mismatch
    prompt_low = prompt.lower()
    if any(w in prompt_low for w in ["library", "building", "house"]) and spec.get("type") != "building":
        issues.append("Prompt suggests a building but spec type is not 'building'.")

    # Content clarity checks
    if len(issues) == 0:
        feedback = "No major issues found."
    else:
        feedback = " | ".join(issues)

    eval_obj = {
        "prompt": prompt,
        "spec_summary": {
            "type": spec.get("type"),
            "has_dimensions": bool(spec.get("dimensions_m")),
            "materials": spec.get("materials", [])
        },
        "critic_feedback": feedback,
        "raw_issues": issues,
        "timestamp": datetime.now().isoformat()
    }
    # Save evaluation file
    save_evaluation(eval_obj)
    return eval_obj

if __name__ == "__main__":
    # quick local test
    sample_prompt = "Design a small eco-friendly 2-floor library"
    from main_agent import generate_spec_from_prompt
    s = generate_spec_from_prompt(sample_prompt)
    r = evaluate_spec(sample_prompt, s)
    print(json.dumps(r, indent=2))
