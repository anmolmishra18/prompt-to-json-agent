import jsonschema
from jsonschema import validate, ValidationError

# Simple JSON schema used for validation and scoring
SCHEMA = {
    "type": "object",
    "properties": {
        "title": {"type": "string"},
        "description": {"type": "string"},
        "owner": {"type": "string"},
        "priority": {"type": "string", "enum": ["low", "medium", "high"]},
        "requirements": {
            "type": "array",
            "items": {"type": "string"}
        }
    },
    "required": ["title", "description"]
}

def validate_spec(spec):
    """
    Validate against SCHEMA.
    Returns (is_valid: bool, errors: list[str])
    """
    try:
        validate(instance=spec, schema=SCHEMA)
        return True, []
    except ValidationError as e:
        return False, [str(e.message)]

def score_spec(spec):
    """
    Produce a simple 0-100 score based on presence of fields and simple heuristics.
    Priority changes strictness:
      - High → stricter (needs long description, ≥3 requirements, owner required)
      - Medium → normal rules
      - Low → more forgiving
    """
    score = 0
    valid, errors = validate_spec(spec)
    if valid:
        score += 40

    # description length
    desc = spec.get("description", "")
    if len(desc) >= 50:
        score += 20
    elif len(desc) >= 20:
        score += 10

    # owner present
    if spec.get("owner"):
        score += 10

    # priority present
    priority = spec.get("priority", "medium")
    if priority in ("low", "medium", "high"):
        score += 10

    # requirements
    reqs = spec.get("requirements") or []
    if isinstance(reqs, list) and len(reqs) >= 3:
        score += 20
    elif isinstance(reqs, list) and len(reqs) >= 1:
        score += 5

    # 🔥 Priority-based adjustments
    if priority == "high":
        if len(desc) < 30:
            score -= 10
        if len(reqs) < 3:
            score -= 10
        if not spec.get("owner"):
            score -= 5
    elif priority == "low":
        score += 5  # lenient

    # clamp score
    return min(100, max(0, score)), {"valid": valid, "errors": errors, "priority": priority}
