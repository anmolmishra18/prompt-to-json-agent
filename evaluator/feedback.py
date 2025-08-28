from copy import deepcopy

def suggest_fixes(spec, score, details):
    suggestions = []
    
    if score >= 95:
        return suggestions
    
    if "title" not in spec or len(spec.get("title", "")) < 5:
        suggestions.append({
            "field": "title",
            "action": "add",
            "value": "Untitled Project"
        })
    
    if "description" not in spec or len(spec.get("description", "")) < 20:
        suggestions.append({
            "field": "description", 
            "action": "expand",
            "value": spec.get("description", "") + " - Enhanced with more details"
        })
    
    reqs = spec.get("requirements", [])
    if not reqs or len(reqs) < 2:
        suggestions.append({
            "field": "requirements",
            "action": "add", 
            "value": ["validation", "reporting"]
        })
    
    if "owner" not in spec:
        suggestions.append({
            "field": "owner",
            "action": "add",
            "value": "Unknown"
        })
    
    if "priority" not in spec:
        suggestions.append({
            "field": "priority",
            "action": "add",
            "value": "medium"
        })
    
    return suggestions

def apply_feedback(spec, suggestions):
    new_spec = deepcopy(spec)
    
    for s in suggestions:
        field, action, value = s["field"], s["action"], s["value"]
        
        if action == "add":
            if isinstance(value, list):
                existing = new_spec.get(field, [])
                if not isinstance(existing, list):
                    existing = []
                new_spec[field] = list(set(existing + value))
            else:
                new_spec[field] = value
        elif action == "expand":
            new_spec[field] = value
        elif action == "replace":
            new_spec[field] = value
    
    return new_spec