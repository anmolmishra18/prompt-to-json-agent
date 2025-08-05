# fix_logs.py

import json
import datetime

LOG_FILE = "logs.json"
updated_logs = []

try:
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()
        for idx, line in enumerate(lines, 1):
            line = line.strip()
            if not line:
                continue
            try:
                entry = json.loads(line)
                if "timestamp" not in entry:
                    entry["timestamp"] = datetime.datetime.now().isoformat()
                updated_logs.append(entry)
            except json.JSONDecodeError as e:
                print(f"⚠️ Skipping malformed line {idx}: {e}")
except FileNotFoundError:
    print("❌ logs.json not found.")
    exit()

# ✅ Rewrite the updated logs back to file
with open(LOG_FILE, "w", encoding="utf-8") as f:
    for entry in updated_logs:
        json.dump(entry, f)
        f.write("\n")

print(f"✅ Updated {len(updated_logs)} log entries with missing timestamps.")
