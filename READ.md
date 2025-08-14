# Prompt-to-JSON AI Agent

This project takes **user prompts** and turns them into a structured JSON specification.  
It also evaluates the spec for issues, scores it, and runs a simple reinforcement learning (RL) loop to improve it.

---

## 📌 1. Project Overview

The system has **three main components**:

1. **Main Agent** (`main_agent.py`)  
   - Reads a user prompt (interactive input or `--prompt` flag)
   - Generates a **specification JSON** from it (currently rule-based)
   - Saves the spec in `prompt_logs/`
   - Passes the spec to the Evaluator Agent
   - Passes the spec to the Data Scorer
   - Runs the RL loop (now runs automatically in this version)
   - Saves all outputs to respective folders

2. **Evaluator Agent** (`evaluator_agent.py`)  
   - Checks the generated spec for:
     - Missing dimensions
     - Unknown or unrealistic materials
     - Type mismatch (e.g., prompt says "library" but spec says "mechanical")
   - Returns feedback and a list of detected issues
   - Saves evaluation results in `evaluations/`

3. **RL Loop** (`rl_loop.py`)  
   - Receives a prompt and a spec
   - Evaluates and scores it
   - If score/reward is low:
     - Applies simple **fixes** (e.g., add missing dimensions, replace unknown materials)
     - Re-evaluates
     - Repeats until:
       - Reward is good, or
       - Max steps reached
   - Saves the RL run log in `rl_logs/`

---

## 🔄 2. Agent Flow

### **Main Agent Flow** (`main_agent.py`)
User Prompt
↓
Generate Spec
↓
Save Spec → Evaluate → Save Evaluation → Score
↓
Run RL Loop
↓
Save RL Log → Merge & Save Final Output

yaml
Copy
Edit

- **Generate Spec**: Uses `generate_spec_from_prompt()` which detects keywords like `"library"`, `"building"`, `"mechanical"` and fills JSON fields accordingly.
- **Save Spec**: Stored in `prompt_logs/` with a timestamp.
- **Evaluate**: `evaluate_spec()` detects problems and gives improvement suggestions.
- **Score**: `score_spec()` assigns a 0–10 score based on completeness, realism, type match, and formatting.
- **RL Loop**: Iteratively improves the spec until it meets the quality threshold.

---

## 🧠 3. Evaluator Flow (`evaluator_agent.py`)

1. **Type Checks**:
   - If type is `"building"` → must have `length`, `width`, and `height`.
2. **Material Checks**:
   - Flags any material not in the allowed list.
3. **Prompt vs Type Match**:
   - Ensures prompt type matches spec type.
4. **Return Values**:
   - `critic_feedback` → human-readable comments
   - `raw_issues` → list of issues found
   - `spec_summary` → quick summary of type, materials, and dimensions

---

## 🤖 4. RL Loop Logic (`rl_loop.py`)

1. Start with the generated spec.
2. Evaluate and score it.
3. If score ≥ threshold **and** no major issues → stop.
4. If not:
   - Apply a **fix**:
     - Add missing dimensions (defaults: length=10, width=10, height=3)
     - Replace unknown materials with `"wood"`
   - Re-run evaluation and scoring.
5. Repeat until:
   - Score is acceptable, or
   - Maximum steps reached (default: 3)
6. Save **all steps, scores, and fixes** to `rl_logs/`.

---

## 🧪 5. Running Test Prompts

### **A) Single Prompt**
```bash
# Standard run (RL loop)
python main_agent.py --prompt "Design a small 2-floor eco-friendly library" --simulate
