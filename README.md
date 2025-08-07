# 🤖 Prompt-to-JSON AI Agent

A Python-based AI agent that converts **natural language design prompts** into **structured JSON specifications**.  
This is ideal for turning vague human instructions into usable machine-readable formats — useful in CAD, manufacturing, and automation design systems.

---

## 🎯 Project Purpose

The goal of this agent is to:
- Understand user prompts like “create a red gearbox using steel gears”
- Extract structured fields such as `type`, `material`, etc.
- Validate them using a schema (`Pydantic`)
- Save them as `.json` files
- Optionally generate LLM-based design text using `GPT2` or `distilgpt2`

---

## ⚙️ Setup Steps

### ✅ 1. Clone the project
```bash
git clone https://github.com/YOUR_USERNAME/prompt-to-json-agent.git
cd prompt-to-json-agent
✅ 2. Set up Python virtual environment
Windows:
bash
Copy
Edit
python -m venv venv
venv\Scripts\activate
macOS/Linux:
bash
Copy
Edit
python3 -m venv venv
source venv/bin/activate
✅ 3. Install dependencies
bash
Copy
Edit
pip install -r requirements.txt
This will install:

transformers for text generation

pydantic for JSON validation

torch and accelerate for running the model efficiently

▶️ How to Run It
Inside the activated environment, run:

bash
Copy
Edit
python main.py
You will be prompted to enter a design prompt:

css
Copy
Edit
🤖 Prompt-to-JSON AI Agent
🔸 Enter your design prompt:
Type something like:

sql
Copy
Edit
Create a red gearbox using steel gears.
📤 Sample Output
✅ JSON Output:
json
Copy
Edit
{
    "type": "gearbox",
    "material": ["steel"],
    "dimensions": null,
    "extras": null
}
✅ File Saved:
spec_outputs/gearbox.json

✅ Prompt Logged in:
logs.json (with timestamp + LLM response)