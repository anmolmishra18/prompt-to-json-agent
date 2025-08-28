from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict, Any, Optional
from main import parse_prompt, run_pipeline

app = FastAPI(title="Prompt-to-JSON Agent API")

class PromptRequest(BaseModel):
    prompt: str

class EvaluateRequest(BaseModel):
    spec: Dict[str, Any]

class IterateRequest(BaseModel):
    spec: Dict[str, Any]
    iterations: Optional[int] = 3

@app.post("/generate")
async def generate_json(request: PromptRequest):
    """Convert prompt to JSON spec"""
    spec = parse_prompt(request.prompt)
    return {"spec": spec}

@app.post("/evaluate")
async def evaluate_spec(request: EvaluateRequest):
    """Evaluate JSON spec"""
    from evaluator.criteria import score_spec
    score, details = score_spec(request.spec)
    return {"score": score, "details": details}

@app.post("/iterate")
async def iterate_spec(request: IterateRequest):
    """Run RL loop on spec"""
    final_spec, history = run_pipeline(request.spec, request.iterations)
    return {"before": request.spec, "after": final_spec, "history": history}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)