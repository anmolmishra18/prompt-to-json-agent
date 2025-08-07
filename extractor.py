def extract_basic_fields(prompt: str) -> dict:
    prompt = prompt.lower()
    fields = {
        "type": "unknown",
        "material": [],
        "dimensions": None,
        "extras": None
    }

    if "building" in prompt or "house" in prompt:
        fields["type"] = "building"
    elif "gearbox" in prompt:
        fields["type"] = "gearbox"
    elif "throne" in prompt:
        fields["type"] = "throne"
    elif "drone" in prompt:
        fields["type"] = "drone"
    elif "robotic arm" in prompt or "robotic hand" in prompt:
        fields["type"] = "robotic arm"
    elif "scene" in prompt:
        fields["type"] = "scene"

    materials = ["steel", "glass", "wood", "carbon fiber", "aluminum", "brick"]
    for mat in materials:
        if mat in prompt:
            fields["material"].append(mat)

    return fields
