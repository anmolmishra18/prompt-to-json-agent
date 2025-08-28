# 🤖 Prompt → JSON Agent

A small agent that converts free-text or structured prompts into **refined JSON specifications**.  
The agent runs an **evaluation + feedback loop** that improves the spec over multiple iterations.  
Reports and feedback logs are saved automatically.

---

## 🚀 Features

- **Prompt to JSON**:  
  Accepts either structured input (`Title: …; Description: …; Owner: …; Requirements: …`) or free text.  

- **Feedback Iterations**:  
  Each iteration runs the evaluator + feedback module to improve the spec until it is complete.  

- **Reports & Logs**:  
  - JSON and TXT reports are saved in `/reports/`.  
  - Feedback history is logged in `/logs/`.  
  - A daily values log (`honesty`, `discipline`, `gratitude`, `integrity`) is appended in `/reports/daily_log.txt`.  

- **Dual Interface**:  
  - Command Line Interface (CLI) via `main.py`.  
  - Streamlit web app via `app.py`.  

---

## 🛠 Installation

Clone the repository and install dependencies:

```bash
git clone https://github.com/your-username/prompt-to-json-agent.git
cd prompt-to-json-agent
python -m venv venv
source venv/bin/activate   # On Linux/Mac
venv\Scripts\activate      # On Windows
pip install -r requirements.txt
💻 Usage
1. CLI Mode
Run with a structured prompt:

bash
Copy code
python main.py --prompt "Title: Student Portal; Description: Manage courses and grades; Owner: Anmol; Requirements: login, dashboard, reports" --iterations 3
Run with a free-text prompt:

bash
Copy code
python main.py --prompt "Make a chatbot for exam queries" --iterations 3
Run with a sample JSON file:

bash
Copy code
python main.py --sample spec1.json --iterations 2
✅ After each run:

Reports are saved in /reports/.

Feedback logs are saved in /logs/.

The final refined spec is printed to the console.

2. Streamlit App
Launch the web interface:

bash
Copy code
streamlit run app.py
Enter your prompt and choose the number of feedback iterations.
You will see:

The parsed JSON spec.

The final refined spec.

Access to logs and reports.

📂 Project Structure
bash
Copy code
prompt-to-json-agent/
│
├── app.py              # Streamlit UI
├── main.py             # CLI entrypoint + pipeline
├── evaluator/
│   ├── criteria.py     # Scoring & evaluation
│   ├── feedback.py     # Feedback generation & application
│   └── report.py       # Report generation (per iteration + final)
│
├── reports/            # Generated reports + daily_log.txt
├── logs/               # Feedback history logs
├── spec1.json          # Sample spec
├── spec2.json          # Sample spec
├── requirements.txt    # Python dependencies
└── Read.md             # Documentation (this file)
🧭 Daily Values Log
Each CLI run appends a reflection entry to /reports/daily_log.txt:

pgsql
Copy code
=== 20250827_141530 ===
Integrity: Submitted the work honestly without skipping compulsory steps.
Honesty: Today I tested the pipeline and verified reports/logs.
Discipline: Kept code structured and updated Read.md.
Gratitude: Grateful for having completed all Task 3 steps.
This ensures honesty, discipline, gratitude, and integrity are recorded daily.

