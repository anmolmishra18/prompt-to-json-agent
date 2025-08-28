"""Prompt Agent with BHIV Core run() interface"""
from main import parse_prompt

class PromptAgent:
    def run(self, input_data):
        """BHIV Core compatible run method"""
        prompt = input_data.get("prompt", "")
        spec = parse_prompt(prompt)
        return {"spec": spec, "agent_type": "prompt_agent"}