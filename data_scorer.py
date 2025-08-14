#!/usr/bin/env python3
"""
data_scorer.py
Computes a 0–10 score from:
 - completeness (dimensions for building / parts for mechanical)
 - material realism
 - type match (prompt vs spec)
 - minimal format completeness
"""
from typing import Dict

KNOWN_MATERIALS = {
    "bamboo","wood","steel","concrete","glass","brick","aluminum","recycled_wood","low-e_glass","low-e glass"
}

def has_dimensions(spec: Dict) -> bool:
    if spec.get("type") == "building":
        dims = spec.get("dimensions_m")
        per_floor = (dims or {}).get("per_floor") if isinstance(dims, dict) else None
        return bool(per_floor and all(k in per_floor for k in ("length","width","height")))
    if spec.get("type") == "mechanical":
        return bool(spec.get("parts"))
    return False

def material_realism_score(spec: Dict) -> float:
    mats = spec.get("materials", [])
    if not mats:
        return 0.0
    known = sum(1 for m in mats if str(m).lower() in KNOWN_MATERIALS)
    return known / max(1, len(mats))

def type_match_score(prompt: str, spec: Dict) -> float:
    pl = prompt.lower()
    building_prompt = any(w in pl for w in ["library","building","house","office","school","museum","center"])
    if (building_prompt and spec.get("type") == "building") or (not building_prompt and spec.get("type") != "building"):
        return 1.0
    return 0.0

def format_score(spec: Dict) -> float:
    base_expected = {"prompt","type","materials"}
    return len(base_expected.intersection(set(spec.keys()))) / len(base_expected)

def score_spec(prompt: str, spec: Dict) -> Dict:
    completeness = 1.0 if has_dimensions(spec) else 0.0
    material_score = material_realism_score(spec)
    tmatch = type_match_score(prompt, spec)
    fmt = format_score(spec)
    score = (completeness * 4.0) + (material_score * 3.0) + (tmatch * 2.0) + (fmt * 1.0)
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
