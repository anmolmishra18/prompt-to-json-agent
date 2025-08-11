#!/usr/bin/env python3
"""
rl_loop.py
Simple RL simulation:
 - run_episode(prompt, spec, max_steps)
 - on each negative reward step, apply simple fixes (add missing dims / replace unknown materials)
 - log each step to rl_logs/
"""
import os
import sys
import json
from datetime import datetime

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from evaluator_agent import evaluate_spec, save_evaluation
from data_scorer import score_spec

ROOT = os.path.dirname(os.path.abspath(__file__))

def timestamp():
    return datetime.now().strftime("%Y%m%d_%H%M%S")

def save_rl_log(obj, tag="rl_episode"):
    folder = os.path.join(ROOT, "rl_logs")
    os.makedirs(folder, exist_ok=True)
    fn = f"{tag}_{timestamp()}.json"
    path = os.path.join(folder, fn)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2)
    return path

def attempt_fix(spec: dict) -> dict:
    # Simple deterministic repairs:
    s = dict(spec)  # shallow copy
    if s.get("type") == "building":
        dims = s.get("dimensions_m")
        if not dims:
            s["dimensions_m"] = {"per_floor": {"length": 10.0, "width": 8.0, "height": 3.0}, "total_height": 3.0}
        else:
            per_floor = dims.get("per_floor") or {}
            if not all(k in per_floor for k in ("length", "width", "height")):
                per_floor.setdefault("length", 10.0)
                per_floor.setdefault("width", 8.0)
                per_floor.setdefault("height", 3.0)
                s["dimensions_m"]["per_floor"] = per_floor
                s["dimensions_m"]["total_height"] = per_floor["height"] * s.get("floors", 1)
    # materials fixes: replace unknowns with common known materials
    mats = s.get("materials", [])
    if mats:
        known = {"bamboo", "wood", "steel", "concrete", "glass", "brick", "aluminum", "recycled_wood"}
        new_mats = []
        for m in mats:
            if m.lower() not in known:
                # replace with a plausible choice
                new_mats.append("steel" if s.get("type") == "mechanical" else "wood")
            else:
                new_mats.append(m)
        s["materials"] = new_mats
    return s

def run_episode(prompt: str, spec: dict, max_steps: int = 3) -> str:
    logs = []
    current_spec = dict(spec)
    for step in range(1, max_steps + 1):
        eval_res = evaluate_spec(prompt, current_spec)
        score_res = score_spec(prompt, current_spec)
        reward = 1 if score_res["spec_score"] >= 7.0 and "no major issues" in eval_res.get("critic_feedback", "").lower() else -1
        logs.append({
            "step": step,
            "spec": current_spec,
            "eval": eval_res,
            "score": score_res,
            "reward": reward,
            "timestamp": datetime.now().isoformat()
        })
        if reward == 1:
            break
        # attempt a fix
        current_spec = attempt_fix(current_spec)

    rl_path = save_rl_log({"prompt": prompt, "episode": logs})
    return rl_path

if __name__ == "__main__":
    # quick run
    from main_agent import generate_spec_from_prompt
    p = "Design a small 2-floor eco-friendly library"
    s = generate_spec_from_prompt(p)
    path = run_episode(p, s, max_steps=3)
    print("RL log saved at:", path)
