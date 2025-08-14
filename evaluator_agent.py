#!/usr/bin/env python3
"""
evaluator_agent.py
Rule-based evaluator that flags:
 - missing/incomplete building dimensions
 - unknown materials
 - prompt/type mismatch
Returns an evaluation dict. Saving is handled via save_evaluation().
"""
import json
import os
from datetime import datetime

ROOT = os.path.dirname(os.path.abspath(__file__))

def _ts():
    return datetime.now().strftime("%Y%m%d_%H%M%S")

def save_evaluation(eval_obj, tag="eval"):
    folder = os.path.join(ROOT, "evaluations")
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, f"{tag}_{_ts()}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(eval_obj, f, indent=2)
    return path

def evaluate_spec(prompt: str, spec: dict) -> dict:
    issues = []
    prompt_low = prompt.lower()

    # Dimensions check for buildings
    if spec.get("type") == "building":
        dims = spec.get("dimensions_m")
        per_floor = (dims or {}).get("per_floor") if isinstance(dims, dict) else None
        if not per_floor or not all(k in per_floor for k in ("length", "width", "height")):
            issues.append("Incomplete or missing per-floor dimensions (length/width/height).")

    # Materials check
    known_materials = {
        "bamboo","wood","steel","concrete","glass","brick","aluminum","recycled_wood","low-e_glass","low-e glass","low-e_glass","low-e_glass".lower()
    }
    mats = spec.get("materials", [])
    unknown = [m for m in mats if str(m).lower() not in known_materials]
    if unknown:
        issues.append(f"Unrecognized or unusual materials: {unknown}")

    # Prompt/type match
    building_prompt = any(w in prompt_low for w in ["library", "building", "house", "office", "school", "museum", "center"])
    if building_prompt and spec.get("type") != "building":
        issues.append("Prompt suggests a building but spec type is not 'building'.")
    if (not building_prompt) and spec.get("type") == "building":
        issues.append("Prompt does not suggest a building, but spec type is 'building'.")

    feedback = "No major issues found." if not issues else " | ".join(issues)

    return {
        "prompt": prompt,
        "spec_summary": {
            "type": spec.get("type"),
            "has_dimensions": bool(spec.get("dimensions_m")),
            "materials": mats
        },
        "critic_feedback": feedback,
        "raw_issues": issues,
        "timestamp": datetime.now().isoformat()
    }
