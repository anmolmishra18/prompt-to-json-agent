@echo off
echo Setting up Prompt-to-JSON Agent...
echo.

echo Creating virtual environment...
python -m venv venv

echo.
echo Activating virtual environment...
call venv\Scripts\activate

echo.
echo Installing dependencies...
pip install -r requirements.txt

echo.
echo ✅ Setup complete!
echo.
echo To run the agent:
echo   CLI: python main.py --prompt "Your prompt here"
echo   Web: streamlit run app.py
echo   Demo: python run_demo.py
echo.
pause