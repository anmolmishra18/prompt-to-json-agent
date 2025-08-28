import streamlit as st
from main import parse_prompt, run_pipeline

st.title("Prompt to JSON Agent")

prompt = st.text_area("Enter your prompt:", height=100)
iterations = st.number_input("Iterations", min_value=1, max_value=10, value=3)

if st.button("Run Agent"):
    if prompt.strip():
        spec = parse_prompt(prompt)
        st.subheader("Parsed JSON")
        st.json(spec)
        
        final_spec, history = run_pipeline(spec, iterations)
        st.subheader("Final Spec")
        st.json(final_spec)
        
        st.success("Reports saved in 'reports/', logs in 'logs/'")
    else:
        st.error("Please enter a prompt")