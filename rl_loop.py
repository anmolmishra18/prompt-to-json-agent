#!/usr/bin/env python3
"""
rl_loop.py
Simple RL-like fixer:
  - Evaluate + Score
  - If not good: fix missing dims / replace unknown materials
  - Log each step (evaluation + fix diff). Log never empty.
Creates rl_logs/rl_*.json
"""
import json
import os
from copy import deepcopy
from datetime import datetime

from evaluator_agent import evaluate_spec
from data_scorer import score_spec

ROOT = os.path.dirname(os.path.abspath(__file__))
RL_DIR = os.path.join(ROOT, "rl_logs")
os.makedirs(RL_DIR, exist_ok=True)

def _ts():
    return datetime.now().strftime("%Y%m%d_%H%M%S")

def _save_rl_log(obj):
    path = os.path.join(RL_DIR, f"rl_{_ts()}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2)
    return path

def _shallow_diff(before: dict, after: dict) -> dict:
    diff = {}
    keys = set(before.keys()) | set(after.keys())
    for k in keys:
        if before.get(k) != after.get(k):
            diff[k] = {"before": before.get(k), "after": after.get(k)}
    return diff

def _attempt_fix(spec: dict) -> dict:
    s = deepcopy(spec)

    # Fix materials
    known = {"bamboo","wood","steel","concrete","glass","brick","aluminum","recycled_wood","low-e_glass","low-e glass"}
    if s.get("materials"):
        s["materials"] = [
            (m if str(m).lower() in known else ("steel" if s.get("type") != "building" else "wood"))
            for m in s["materials"]
        ]

    # Fix dimensions for buildings
    if s.get("type") == "building":
        dims = s.get("dimensions_m")
        per_floor = (dims or {}).get("per_floor") if isinstance(dims, dict) else None
        if not per_floor or not all(k in per_floor for k in ("length","width","height")):
            s["dimensions_m"] = {
                "per_floor": {"length": 10.0, "width": 8.0, "height": 3.0},
                "total_height": 3.0 * s.get("floors", 1)
            }

    return s

def run_episode(prompt: str, spec: dict, max_steps: int = 3) -> str:
    print(">>> RL LOOP START for prompt:", prompt)  # DEBUG

    logs = []
    current = deepcopy(spec)

    for step in range(1, max_steps + 1):
        # Evaluate + Score
        eval_res = evaluate_spec(prompt, current)
        score_res = score_spec(prompt, current)
        critic_text = eval_res.get("critic_feedback", "").lower()
        reward = 1 if (score_res["spec_score"] >= 7.0 and "no major issues" in critic_text) else -1

        # Always log the evaluation step
        logs.append({
            "step": step,
            "spec_snapshot": deepcopy(current),
            "evaluation": eval_res,
            "score": score_res,
            "reward": reward,
            "timestamp": datetime.now().isoformat()
        })

        if reward == 1:
            break

        # Apply fix and log diff
        before = deepcopy(current)
        current = _attempt_fix(current)
        diff = _shallow_diff(before, current)
        logs.append({
            "step": step,
            "fix_applied_diff": diff,
            "timestamp": datetime.now().isoformat()
        })

    if not logs:  # safety net; should never happen now
        logs.append({"step": 0, "note": "No steps recorded — forcing non-empty log"})

    rl_path = _save_rl_log({"prompt": prompt, "episode": logs})
    return rl_path
