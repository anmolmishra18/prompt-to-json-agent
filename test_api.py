"""Test script for FastAPI endpoints"""
import json
from api import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_generate():
    response = client.post("/generate", json={"prompt": "Create a student portal"})
    print("Generate endpoint test:")
    print(json.dumps(response.json(), indent=2))
    return response.status_code == 200

if __name__ == "__main__":
    success = test_generate()
    print(f"Test passed: {success}")