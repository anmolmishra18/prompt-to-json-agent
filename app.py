import streamlit as st
import json
from main import parse_prompt, run_pipeline

st.title("Prompt to JSON Agent")
st.write("Convert prompts into refined JSON specifications through RL feedback")

prompt = st.text_area("Enter your prompt:", 
                     value=st.session_state.get('prompt_text', ''),
                     height=100, 
                     placeholder="e.g., Build a chatbot for customer support. Priority: High")
iterations = st.number_input("Iterations", min_value=1, max_value=10, value=3)

if st.button("Run Agent"):
    if prompt.strip():
        try:
            with st.spinner("Processing..."):
                spec = parse_prompt(prompt)
                st.subheader("Parsed JSON")
                st.json(spec)
                
                final_spec, history = run_pipeline(spec, iterations)
                st.subheader("Final Spec")
                st.json(final_spec)
                
                if len(history) > 1:
                    initial_score = history[0]['score']
                    final_score = history[-1]['score']
                    st.metric("Score Improvement", f"{final_score}", f"{final_score - initial_score}")
                
                st.success("Reports saved in 'reports/', logs in 'logs/'")
        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.error("Please enter a prompt")

with st.sidebar:
    st.header("Examples")
    if st.button("Student System"):
        st.session_state.prompt_text = "Create a student management system with grades and attendance"
    if st.button("E-commerce API"):
        st.session_state.prompt_text = "Build an e-commerce API with products, orders, and payments"
    if st.button("Chatbot Support"):
        st.session_state.prompt_text = "Build a chatbot for customer support. Priority: High"
    
    st.markdown("**Usage Tips:**")
    st.markdown("• Use 'Priority: High/Medium/Low'")
    st.markdown("• Use 'Title: Your Title'")
    st.markdown("• Separate with periods or semicolons")