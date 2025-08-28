"""Feedback Agent with BHIV Core run() interface"""
from evaluator.feedback import suggest_fixes, apply_feedback

class FeedbackAgent:
    def run(self, input_data):
        """BHIV Core compatible run method"""
        spec = input_data.get("spec", {})
        score = input_data.get("score", 0)
        details = input_data.get("details", {})
        
        suggestions = suggest_fixes(spec, score, details)
        improved_spec = apply_feedback(spec, suggestions) if suggestions else spec
        
        return {
            "suggestions": suggestions,
            "improved_spec": improved_spec,
            "agent_type": "feedback"
        }