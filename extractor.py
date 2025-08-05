# extractor.py

def extract_basic_fields(prompt: str) -> dict:
    fields = {
        "type": "unknown",
        "material": [],
        "color": None,
        "dimensions": None,
        "purpose": None
    }

    prompt_lower = prompt.lower()

    # Detect object type
    if "building" in prompt_lower:
        fields["type"] = "building"
    elif "gearbox" in prompt_lower:
        fields["type"] = "gearbox"
    elif "throne" in prompt_lower:
        fields["type"] = "throne"

    # Detect material
    materials = ["glass", "steel", "concrete", "wood", "carbon fiber", "brick"]
    for mat in materials:
        if mat in prompt_lower:
            fields["material"].append(mat)

    # Detect color
    colors = ["red", "blue", "green", "black", "white"]
    for color in colors:
        if color in prompt_lower:
            fields["color"] = color

    # Detect purpose
    if "fantasy game" in prompt_lower:
        fields["purpose"] = "fantasy game"
    elif "automotive" in prompt_lower:
        fields["purpose"] = "automotive"

    return fields


if __name__ == "__main__":
    prompts = [
        "Design a 2-floor building using glass and concrete.",
        "Create a red gearbox with steel gears.",
        "Model a medieval throne for a fantasy game."
    ]

    for i, prompt in enumerate(prompts):
        result = extract_basic_fields(prompt)
        print(f"\nPrompt {i+1}: {prompt}")
        print("Extracted:", result)
