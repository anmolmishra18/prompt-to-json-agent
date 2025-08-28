import streamlit as st
from main import parse_prompt, refine_spec, run_pipeline

st.set_page_config(page_title="Prompt to JSON Agent", layout="wide")
st.title("Prompt to JSON Agent (Demo)")

prompt = st.text_area(
    "Enter your prompt text:",
    placeholder="Example: Make a call to ambulance it is urgent",
    height=150
)

iterations = st.number_input("Feedback iterations", min_value=1, max_value=10, value=3)

if st.button("Run Agent"):
    if not prompt.strip():
        st.error("Please enter a prompt first.")
    else:
        spec = parse_prompt(prompt)
        st.subheader("Parsed JSON")
        st.json(spec)

        final_spec, logs = run_pipeline(spec, iterations=iterations)
        st.subheader("Final Spec after Feedback Loop")
        st.json(final_spec)

        st.success(f"Reports saved in 'reports/', logs saved in 'logs/'")
