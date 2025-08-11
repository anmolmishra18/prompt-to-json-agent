# main_agent.py
from transformers import pipeline
import json

# Load stub LLM for main agent
generator_llm = pipeline("text-generation", model="TinyLlama/TinyLlama-1.1B-Chat-v1.0")

def generate_spec(prompt: str) -> dict:
    gen_prompt = f"Generate a JSON spec for: {prompt}. Include dimensions, materials, layout."
    response = generator_llm(gen_prompt, max_new_tokens=200, do_sample=True)[0]['generated_text']
    # Mock parse to JSON (in real, use better parsing)
    try:
        # Attempt to extract JSON from response
        json_start = response.find('{')
        json_end = response.rfind('}') + 1
        spec_str = response[json_start:json_end]
        spec = json.loads(spec_str)
    except:
        spec = {"dimensions": "unknown", "materials": "unknown", "layout": "unknown"}  # Fallback
    return spec

# Example
if __name__ == "__main__":
    prompt = "design a small 2-floor eco-friendly library"
    print(generate_spec(prompt))