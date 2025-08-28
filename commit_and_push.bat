@echo off
echo Preparing to commit and push Prompt-to-JSON Agent...
echo.

echo Adding all files to git...
git add .

echo.
echo Committing changes...
git commit -m "Complete Task 3: Prompt-to-JSON Agent with RL Pipeline

- ✅ Day 1: Repo setup + folder structure + base pipeline (main.py)
- ✅ Day 2: Evaluator + report generator (criteria.py, feedback.py, report.py)  
- ✅ Day 3: Feedback loop + RL agent with iterative improvements
- ✅ Day 4: CLI + Streamlit app + comprehensive documentation

Features:
- Full CLI interface with --prompt and --sample options
- Streamlit web app for interactive use
- Comprehensive evaluation with scoring (0-100)
- Iterative feedback loop for spec refinement
- JSON and TXT report generation per iteration
- Daily values logging (honesty, discipline, gratitude, integrity)
- Windows compatibility with proper encoding handling
- Demo scripts and test suite included

All 4-day requirements completed with working agent pipeline."

echo.
echo Pushing to GitHub...
git push origin main

echo.
echo ✅ Successfully pushed to GitHub!
echo Check your repository at: https://github.com/your-username/prompt-to-json-agent
pause