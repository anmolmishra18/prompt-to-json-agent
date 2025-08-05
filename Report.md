Prompt-to-JSON Agent

> Convert natural language design prompts into clean, structured JSON using a lightweight AI agent.

Project Purpose:

This project simulates a lightweight design assistant powered by a local LLM (`distilgpt2`).  
It accepts natural language prompts, generates design descriptions, then parses and validates them into a **structured JSON format using `Pydantic`.

Use cases include:
- AI-assisted design tools
- Generative input extraction
- Low-latency prompt logging and response storage

Setup Instructions:

1. Clone the Repo:

bash
git clone https://github.com/anmolmishra18/prompt-to-json-agent.git
cd prompt-to-json-agent

2. Create a Virtual Environment:

bash
python -m venv venv

3. Activate the Environment:

On Windows:

bash
venv\Scripts\activate

Install Dependencies:

Install all libraries from `requirements.txt`:

bash
pip install -r requirements.txt

Or install manually if needed:

bash
pip install transformers torch pydantic

How to Run

Run the full pipeline:

bash
python main.py

This script will:
 Accept prompts
 Generate LLM responses
 Extract structured data (type, material, color, purpose)
 Validate via Pydantic schema
 Save to `spec_outputs/spec_*.json`
 Log all interactions in `logs.json`

Sample Input & Output:

Prompt:

Design a robotic arm for factory use using aluminum.

LLM Output:

The robotic arm is constructed with high-grade aluminum to endure factory conditions.

Parsed Output (JSON):

json
{
  "type": "robotic arm",
  "material": ["aluminum"],
  "color": null,
  "purpose": "factory use"
}

Project Structure:

prompt-to-json-agent/
├── main.py             # Full pipeline script
├── logger.py           # Logs prompt/output with timestamps
├── schema.py           # Pydantic schema for design specs
├── logs.json           # All logged interactions
├── spec_outputs/       # Contains validated JSON outputs
├── venv/               # Python virtual environment
├── report.md           # Final report
└── requirements.txt    # Python dependencies

Author:

Name: Anmol Mishra
Email: [anmolmishra307680@gmail.com](mailto:anmolmishra307680@gmail.com)
GitHub: [@anmolmishra18](https://github.com/anmolmishra18)