"""
feedback.py – Suggest and apply improvements to JSON specs
"""

from copy import deepcopy


def suggest_fixes(spec: dict, score: int, details: dict):
    """
    Suggest improvements based on the evaluator's score and details.

    Args:
        spec: Current JSON spec (dict)
        score: Numeric score from evaluator (0-100)
        details: Dict with field-level evaluation details

    Returns:
        list of suggestion dicts
    """
    suggestions = []

    # If already very good, no changes needed
    if score >= 95:
        return suggestions

    # If title missing or too short
    if "title" not in spec or len(spec.get("title", "")) < 5:
        suggestions.append({
            "field": "title",
            "action": "add",
            "value": "Untitled Project"
        })

    # If description is missing or too short
    if "description" not in spec or len(spec.get("description", "")) < 20:
        suggestions.append({
            "field": "description",
            "action": "expand",
            "value": spec.get("description", "") +
                     "\n\nPlease add more details about goal, input and expected output."
        })

    # If requirements missing or too few
    reqs = spec.get("requirements", [])
    if not reqs or len(reqs) < 2:
        suggestions.append({
            "field": "requirements",
            "action": "add",
            "value": ["basic validation", "report generation"]
        })

    # If owner missing
    if "owner" not in spec or not spec.get("owner"):
        suggestions.append({
            "field": "owner",
            "action": "add",
            "value": "Unknown"
        })

    # If priority missing
    if "priority" not in spec or not spec.get("priority"):
        suggestions.append({
            "field": "priority",
            "action": "add",
            "value": "medium"
        })

    return suggestions


def apply_feedback(spec: dict, suggestions: list):
    """
    Apply feedback suggestions to the spec.

    Args:
        spec: Current JSON spec
        suggestions: list of suggestion dicts

    Returns:
        Updated spec
    """
    new_spec = deepcopy(spec)

    for s in suggestions:
        field, action, value = s["field"], s["action"], s["value"]

        if action == "add":
            if isinstance(value, list):
                # merge lists
                existing = new_spec.get(field, [])
                if not isinstance(existing, list):
                    existing = []
                new_spec[field] = list(set(existing + value))
            else:
                new_spec[field] = value

        elif action == "expand":
            if field in new_spec and isinstance(new_spec[field], str):
                new_spec[field] += "\n" + value
            else:
                new_spec[field] = value

        elif action == "replace":
            new_spec[field] = value

    return new_spec
