from transformers import pipeline
from extractor import extract_basic_fields
from schema import DesignSpec
from logger import log_prompt
import json
import os

# Load LLM pipeline
pipe = pipeline("text-generation", model="gpt2")

# Ensure output folder exists
os.makedirs("spec_outputs", exist_ok=True)

def main():
    print("\n🤖 Prompt-to-JSON AI Agent")
    prompt = input("🔸 Enter your design prompt: ")

    # Step 1: Extract structured fields
    extracted = extract_basic_fields(prompt)

    # Step 2: Validate with Pydantic v2
    try:
        spec = DesignSpec(**extracted)
        json_output = spec.model_dump_json(indent=4)
    except Exception as e:
        print("❌ Schema validation failed:", e)
        return

    # Step 3: Save JSON file
    file_id = extracted["type"].replace(" ", "_")
    filename = f"spec_outputs/{file_id}.json"
    with open(filename, "w") as f:
        f.write(json_output)

    # Step 4: Generate LLM response
    full_output = pipe(prompt, max_length=60)[0]["generated_text"]

    # Step 5: Clean LLM response
    if full_output.startswith(prompt):
        llm_generated_part = full_output[len(prompt):].strip()
    else:
        llm_generated_part = full_output.strip()

    if not llm_generated_part:
        llm_generated_part = full_output.strip()

    # Step 6: Log the result
    log_prompt(prompt, llm_generated_part)

    # Step 7: Display output
    print("\n✅ JSON Output:")
    print(json_output)
    print(f"\n📁 Saved to: {filename}")
    print("📝 Logged in: logs.json")

if __name__ == "__main__":
    main()
