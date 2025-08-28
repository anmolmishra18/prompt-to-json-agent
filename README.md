# 🤖 Prompt-to-JSON Agent

A reinforcement learning agent that converts free-text or structured prompts into **refined JSON specifications** through an iterative evaluation and feedback loop.

## 🚀 Features

- **Prompt to JSON Conversion**: Accepts structured input (`Title: ...; Description: ...; Owner: ...; Requirements: ...`) or free text
- **Iterative Refinement**: Uses evaluation + feedback loop to improve specs over multiple iterations
- **Comprehensive Reporting**: Generates JSON and TXT reports for each iteration
- **Feedback Logging**: Maintains detailed logs of all improvements and iterations
- **Dual Interface**: Command Line Interface (CLI) and Streamlit web app
- **Values Tracking**: Daily logs for honesty, discipline, gratitude, and integrity

## 🛠 Installation

```bash
git clone https://github.com/your-username/prompt-to-json-agent.git
cd prompt-to-json-agent
python -m venv venv
source venv/bin/activate   # On Linux/Mac
venv\\Scripts\\activate      # On Windows
pip install -r requirements.txt
```

## 💻 Usage

### 1. CLI Mode

**Run with structured prompt:**
```bash
python main.py --prompt "Title: Student Portal; Description: Manage courses and grades; Owner: Anmol; Requirements: login, dashboard, reports" --iterations 3
```

**Run with free-text prompt:**
```bash
python main.py --prompt "Create a student management system for tracking grades and attendance" --iterations 3
```

**Run with sample JSON file:**
```bash
python main.py --sample samples/spec1.json --iterations 2
```

### 2. Streamlit Web App

Launch the web interface:
```bash
streamlit run app.py
```

Enter your prompt and choose the number of feedback iterations. The app will show:
- The parsed JSON spec
- The final refined spec after iterations
- Links to generated reports and logs

## 📂 Project Structure

```
prompt-to-json-agent/
│
├── main.py              # CLI entrypoint + pipeline orchestration
├── app.py               # Streamlit web interface
├── evaluator/
│   ├── criteria.py      # JSON schema validation & scoring
│   ├── feedback.py      # Feedback generation & application
│   └── report.py        # Report generation (JSON + TXT)
│
├── samples/             # Sample JSON specifications
│   ├── spec1.json
│   └── spec2.json
│
├── reports/             # Generated reports + daily_log.txt
├── logs/                # Feedback history logs
├── requirements.txt     # Python dependencies
└── README.md           # This documentation
```

## 🔄 How It Works

1. **Input Processing**: Parses structured or free-text prompts into initial JSON spec
2. **Evaluation**: Scores the spec (0-100) based on completeness and quality
3. **Feedback Generation**: Identifies missing or inadequate fields
4. **Spec Refinement**: Applies suggested improvements
5. **Iteration**: Repeats steps 2-4 for specified number of iterations
6. **Reporting**: Generates comprehensive reports and logs

## 📊 Evaluation Criteria

The agent evaluates specs based on:
- **Schema Validation**: Adherence to required JSON structure
- **Completeness**: Presence of title, description, owner, priority, requirements
- **Quality**: Description length, requirement count, priority-based adjustments
- **Priority Handling**: Stricter evaluation for high-priority specs

## 🧭 Daily Values Tracking

Each CLI run appends a reflection entry to `/reports/daily_log.txt`:

```
=== 20250828_112335 ===
Integrity: Submitted work honestly without skipping steps
Honesty: Tested full pipeline and verified all components work
Discipline: Maintained clean code structure and documentation
Gratitude: Grateful for completing all Task 3 requirements
```

## 🎯 Task 3 Completion Status

✅ **Day 1**: Repo setup + folder structure + base pipeline  
✅ **Day 2**: Evaluator + report generator implemented  
✅ **Day 3**: Feedback loop + RL agent working  
✅ **Day 4**: CLI + Streamlit app + documentation complete  

## 🤝 Contributing

This project follows the core values of:
- **Honesty**: Transparent reporting of what works vs. what's blocked
- **Discipline**: Regular commits and structured development
- **Gratitude**: Acknowledging contributions and learning
- **Integrity**: Honest evaluation and authentic progress tracking

## 📝 License

MIT License - see LICENSE file for details

## 👥 Acknowledgments

- Thanks to Olivia and Saad for evaluation logic contributions
- Grateful for open-source libraries: FastAPI, Streamlit, jsonschema
- AWS Q Developer for development assistance