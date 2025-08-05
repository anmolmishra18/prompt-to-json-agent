# logger.py

import json
import datetime
import os

# ✅ Path to the log file
LOG_FILE = "logs.json"

# ✅ Function to log a new prompt and output with timestamp
def log_prompt(prompt: str, output: str):
    log_entry = {
        "prompt": prompt,
        "output": output,
        "timestamp": datetime.datetime.now().isoformat()
    }

    with open(LOG_FILE, "a", encoding="utf-8") as f:
        json.dump(log_entry, f)
        f.write("\n")

    print("✅ Logged entry with timestamp.")

# ✅ Function to fetch the last N logged prompts
def get_last_prompts(n=5):
    try:
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            lines = f.readlines()
            recent_logs = lines[-n:]
            return [json.loads(line.strip()) for line in recent_logs]
    except FileNotFoundError:
        print("⚠️ No log file found.")
        return []
    except json.JSONDecodeError as e:
        print(f"❌ JSON decode error: {e}")
        return []

# ✅ Test block (optional)
if __name__ == "__main__":
    # Sample test usage
    sample_prompt = "Create a stealth drone for surveillance using carbon fiber."
    sample_output = "type: drone, material: carbon fiber, purpose: surveillance"

    log_prompt(sample_prompt, sample_output)

    print("\n🔁 Last 3 logged prompts:")
    logs = get_last_prompts(3)
    for i, entry in enumerate(logs, 1):
        print(f"\nLog {i}:")
        print(f"Prompt   : {entry['prompt']}")
        print(f"Output   : {entry['output']}")
        print(f"Timestamp: {entry['timestamp']}")
