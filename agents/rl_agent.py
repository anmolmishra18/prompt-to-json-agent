"""RL Agent with BHIV Core run() interface"""
from main import run_pipeline

class RLAgent:
    def run(self, input_data):
        """BHIV Core compatible run method"""
        spec = input_data.get("spec", {})
        iterations = input_data.get("iterations", 3)
        
        final_spec, history = run_pipeline(spec, iterations)
        
        return {
            "final_spec": final_spec,
            "history": history,
            "agent_type": "rl_agent"
        }