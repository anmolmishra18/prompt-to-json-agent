"""Start FastAPI server"""
import uvicorn

if __name__ == "__main__":
    print("Starting FastAPI server on http://localhost:8000")
    print("API endpoints:")
    print("- POST /generate - Convert prompt to JSON")
    print("- POST /evaluate - Evaluate JSON spec") 
    print("- POST /iterate - Run RL loop")
    
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)