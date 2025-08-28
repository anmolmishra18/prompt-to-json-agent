import jsonschema
from jsonschema import validate, ValidationError

SCHEMA = {
    "type": "object",
    "properties": {
        "title": {"type": "string"},
        "description": {"type": "string"},
        "owner": {"type": "string"},
        "priority": {"type": "string", "enum": ["low", "medium", "high"]},
        "requirements": {"type": "array", "items": {"type": "string"}}
    },
    "required": ["title", "description"]
}

def validate_spec(spec):
    try:
        validate(instance=spec, schema=SCHEMA)
        return True, []
    except ValidationError as e:
        return False, [str(e.message)]

def score_spec(spec):
    score = 0
    valid, errors = validate_spec(spec)
    
    if valid:
        score += 40
    
    desc = spec.get("description", "")
    if len(desc) >= 50:
        score += 20
    elif len(desc) >= 20:
        score += 10
    
    if spec.get("owner"):
        score += 10
    
    if spec.get("priority") in ["low", "medium", "high"]:
        score += 10
    
    reqs = spec.get("requirements", [])
    if isinstance(reqs, list) and len(reqs) >= 3:
        score += 20
    elif isinstance(reqs, list) and len(reqs) >= 1:
        score += 5
    
    return min(100, max(0, score)), {"valid": valid, "errors": errors}