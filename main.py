# main.py

from transformers import pipeline
from schema import DesignSpec
from logger import log_prompt
import os
import json

# ✅ Ensure output directory exists
os.makedirs("spec_outputs", exist_ok=True)

# ✅ Sample prompts to run through the system
prompts = [
    "Design a robotic arm for factory use using aluminum.",
    "Create a red gearbox with steel gears.",
    "Model a medieval throne for a fantasy game.",
    "Create a stealth drone for surveillance using carbon fiber.",
    "Design a waterproof smartwatch using titanium."
]

# ✅ Text generation pipeline (offline model)
pipe = pipeline("text-generation", model="distilgpt2")

# ✅ Naive extractor (manual pattern matching — replace with real parser later)
def extract_spec(text):
    spec = {}
    text = text.lower()

    # Type
    for t in ["arm", "gearbox", "throne", "drone", "watch", "smartwatch"]:
        if t in text:
            spec["type"] = t
            break

    # Material
    materials = []
    for m in ["aluminum", "steel", "wood", "carbon fiber", "titanium"]:
        if m in text:
            materials.append(m)
    if materials:
        spec["material"] = materials

    # Color
    for c in ["red", "blue", "black", "silver"]:
        if c in text:
            spec["color"] = c
            break

    # Purpose
    for p in ["factory", "automotive", "fantasy", "surveillance", "waterproof"]:
        if p in text:
            spec["purpose"] = p + " use" if p == "factory" else p
            break

    return spec

# ✅ Main processing loop
for idx, prompt in enumerate(prompts, 1):
    print(f"\n🔵 Prompt {idx}: {prompt}")
    response = pipe(prompt, max_length=100)[0]["generated_text"]
    print(f"🟢 Response: {response}")

    # 🔁 Log prompt + output
    log_prompt(prompt, response)

    # 🧠 Extract structured data
    extracted = extract_spec(response)
    print(f"🧩 Extracted: {extracted}")

    try:
        # ✅ Validate structure
        spec = DesignSpec(**extracted)
        filename = f"spec_outputs/spec_{idx}.json"
        with open(filename, "w") as f:
            f.write(spec.json(indent=4))
        print(f"✅ Saved structured spec to {filename}")
    except Exception as e:
        print(f"❌ Validation failed: {e}")
