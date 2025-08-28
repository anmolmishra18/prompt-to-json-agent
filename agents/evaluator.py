"""Evaluator Agent with BHIV Core run() interface"""
from evaluator.criteria import score_spec

class EvaluatorAgent:
    def run(self, input_data):
        """BHIV Core compatible run method"""
        spec = input_data.get("spec", {})
        score, details = score_spec(spec)
        return {"score": score, "details": details, "agent_type": "evaluator"}