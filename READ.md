# Prompt-to-JSON AI Agent

This project takes **user prompts** and turns them into a structured JSON specification.  
It also evaluates the spec for issues, scores it, and runs a simple reinforcement learning (RL) loop to try to improve it.

---

## 📌 1. Project Overview

The system has **3 main agents**:

1. **Main Agent** (`main_agent.py`)  
   - Reads a user prompt
   - Generates a **specification JSON** from it (currently rule-based stub)
   - Saves the spec in `prompt_logs/`
   - Passes the spec to the Evaluator Agent
   - Passes the spec to the Data Scorer
   - Runs the RL loop (optional)
   - Saves all outputs to respective folders

2. **Evaluator Agent** (`evaluator_agent.py`)  
   - Checks the generated spec for:
     - Missing dimensions
     - Unknown materials
     - Type mismatch (prompt says "library" but spec says "mechanical")
   - Returns feedback & a list of detected issues
   - Saves evaluation results in `evaluations/`

3. **RL Loop** (`rl_loop.py`)  
   - Receives a prompt and a spec
   - Evaluates and scores it
   - If score/reward is bad:
     - Applies simple **fixes** (e.g., add missing dimensions, replace unknown materials)
     - Re-evaluates
     - Repeats until:
       - Reward is good, or
       - Max steps are reached
   - Saves the RL run log in `rl_logs/`

---

## 🔄 2. Agent Flow

### **Main Agent Flow** (`main_agent.py`)
User Prompt → Generate Spec → Save Spec → Evaluate Spec → Save Evaluation → Score Spec → [Optional] Run RL Loop → Save RL Log

- **Generate Spec**: The current version uses a stub function (`generate_spec_from_prompt`) that recognizes certain keywords (e.g., "library", "building", "mechanical") and fills in JSON fields.
- **Save Spec**: Stored in `prompt_logs/` with timestamp.
- **Evaluate Spec**: Uses `evaluate_spec` to detect issues and suggest improvements.
- **Score Spec**: Uses `score_spec` to give a 0–10 score based on completeness, realism, type match, and formatting.
- **RL Loop**: Optionally (`--simulate`) runs improvement attempts.

---

## 🧠 3. Evaluator Flow (`evaluator_agent.py`)

1. Check **type-specific requirements**:
   - If building → Must have dimensions (`length`, `width`, `height`).
2. Check **materials**:
   - Flag unknown materials not in the allowed list.
3. Check **prompt vs type match**:
   - Example: If prompt says "library" but type is `"mechanical"`, it's an issue.
4. Return:
   - `critic_feedback` (human-readable)
   - `raw_issues` (list of detected problems)
   - `spec_summary` (summary of type, materials, dimensions)

---

## 🤖 4. RL Loop Logic (`rl_loop.py`)

1. Start with the generated spec.
2. **Evaluate** and **Score** it.
3. If reward is **good**:
   - Stop immediately.
4. If reward is **bad**:
   - Apply a simple **fix**:
     - Add missing dimensions.
     - Replace unknown materials with known ones.
   - Re-run evaluation and scoring.
5. Repeat until:
   - Reward is good, or
   - Maximum number of steps reached.
6. Save the **entire episode log** (all steps, changes, and rewards) in `rl_logs/`.

---

## 🧪 5. Running Test Prompts

### **A) Single Prompt**
```bash
# Basic run
python main_agent.py --prompt "Design a small 2-floor eco-friendly library"

# Run with RL improvement loop
python main_agent.py --prompt "Design a small 2-floor eco-friendly library" --simulate