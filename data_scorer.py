#!/usr/bin/env python3
"""
data_scorer.py
Score generated spec on:
 - completeness (dimensions present)
 - material realism
 - type match (prompt vs spec)
 - formatting (basic)
Returns combined score 0-10 and breakdown.
"""
import json
from typing import Dict

KNOWN_MATERIALS = {"bamboo", "wood", "steel", "concrete", "glass", "brick", "aluminum", "recycled_wood", "low-e_glass", "low-E_glass"}

def has_dimensions(spec: Dict) -> bool:
    if spec.get("type") == "building":
        dims = spec.get("dimensions_m")
        return bool(dims and "per_floor" in dims)
    if spec.get("type") == "mechanical":
        return bool(spec.get("parts"))
    return False

def material_realism_score(spec: Dict) -> float:
    mats = spec.get("materials", [])
    if not mats:
        return 0.0
    known = sum(1 for m in mats if m.lower() in KNOWN_MATERIALS)
    return known / len(mats)  # 0..1

def type_match_score(prompt: str, spec: Dict) -> float:
    pl = prompt.lower()
    is_building_prompt = any(w in pl for w in ["library", "building", "house", "school"])
    if is_building_prompt and spec.get("type") == "building":
        return 1.0
    if not is_building_prompt and spec.get("type") != "building":
        return 1.0
    return 0.0

def format_score(spec: Dict) -> float:
    # crude heuristic: presence of keys
    keys = set(spec.keys())
    base_expected = {"prompt", "type", "materials"}
    present = len(base_expected.intersection(keys))
    return present / len(base_expected)  # 0..1

def score_spec(prompt: str, spec: Dict) -> Dict:
    completeness = 1.0 if has_dimensions(spec) else 0.0
    material_score = material_realism_score(spec)
    tmatch = type_match_score(prompt, spec)
    fmt = format_score(spec)
    # weights -> map to 0..10
    score = (completeness * 4.0) + (material_score * 3.0) + (tmatch * 2.0) + (fmt * 1.0)
    # clamp
    score = max(0.0, min(10.0, score))
    return {
        "spec_score": round(score, 2),
        "breakdown": {
            "completeness": completeness,
            "material_realism": round(material_score, 2),
            "type_match": tmatch,
            "format_score": round(fmt, 2)
        }
    }

if __name__ == "__main__":
    # example quick test
    from main_agent import generate_spec_from_prompt
    p = "Design a small 2-floor eco-friendly library"
    s = generate_spec_from_prompt(p)
    print(json.dumps(score_spec(p, s), indent=2))
