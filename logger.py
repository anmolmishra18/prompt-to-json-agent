import json
import datetime

def log_prompt(prompt, output):
    log = {
        "prompt": prompt,
        "output": output,
        "timestamp": datetime.datetime.now().isoformat()
    }
    with open("logs.json", "a") as f:
        json.dump(log, f)
        f.write("\n")

def get_last_prompts(n=5):
    with open("logs.json") as f:
        lines = f.readlines()
    return lines[-n:]
