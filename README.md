# Prompt-to-JSON Agent

A reinforcement learning agent that converts prompts into refined JSON specifications through iterative evaluation and feedback.

## Installation

```bash
git clone https://github.com/your-username/prompt-to-json-agent.git
cd prompt-to-json-agent
pip install -r requirements.txt
```

## Usage

### CLI
```bash
python main.py --prompt "Create a student management system" --iterations 3
python main.py --sample samples/spec1.json --iterations 2
```

### Web App
```bash
streamlit run app.py
```

## Project Structure

```
prompt-to-json-agent/
├── main.py              # CLI entrypoint + pipeline
├── app.py               # Streamlit web interface
├── evaluator/
│   ├── criteria.py      # Schema validation & scoring
│   ├── feedback.py      # Feedback generation & application
│   └── report.py        # Report generation
├── samples/             # Sample JSON specifications
├── reports/             # Generated reports + daily_log.txt
├── logs/                # Feedback history logs
└── requirements.txt     # Dependencies
```

## How It Works

1. **Input Processing**: Parses prompts into initial JSON spec
2. **Evaluation**: Scores spec (0-100) based on completeness
3. **Feedback Generation**: Identifies missing fields
4. **Spec Refinement**: Applies improvements
5. **Iteration**: Repeats for specified iterations
6. **Reporting**: Generates JSON and TXT reports

## Acknowledgments

- Thanks to Olivia and Saad for evaluation logic contributions
- Grateful for open-source libraries: jsonschema, streamlit