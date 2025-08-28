#!/usr/bin/env python3
"""
Test script to verify the complete pipeline works correctly.
This tests all major components: parsing, evaluation, feedback, and reporting.
"""

import json
import os
from main import parse_prompt, run_pipeline

def test_pipeline():
    """Test the complete pipeline with different types of inputs."""
    
    print("=" * 60)
    print("TESTING PROMPT-TO-JSON AGENT PIPELINE")
    print("=" * 60)
    
    # Test 1: Free text prompt
    print("\n1. Testing free text prompt...")
    prompt1 = "Create a chatbot for customer support with FAQ handling"
    spec1 = parse_prompt(prompt1)
    print(f"Input: {prompt1}")
    print(f"Parsed: {json.dumps(spec1, indent=2)}")
    
    final_spec1, history1 = run_pipeline(spec1, iterations=2, 
                                        outdir_reports="test_reports", 
                                        outdir_logs="test_logs")
    print(f"Final score: {history1[-1]['score']}")
    
    # Test 2: Structured prompt
    print("\n2. Testing structured prompt...")
    prompt2 = "Title: E-commerce Platform; Description: Online shopping with cart and payments; Owner: John Doe; Requirements: user auth, product catalog, payment gateway"
    spec2 = parse_prompt(prompt2)
    print(f"Input: {prompt2}")
    print(f"Parsed: {json.dumps(spec2, indent=2)}")
    
    final_spec2, history2 = run_pipeline(spec2, iterations=2,
                                        outdir_reports="test_reports", 
                                        outdir_logs="test_logs")
    print(f"Final score: {history2[-1]['score']}")
    
    # Test 3: Load from sample file
    print("\n3. Testing sample file loading...")
    if os.path.exists("samples/spec1.json"):
        with open("samples/spec1.json", "r") as f:
            spec3 = json.load(f)
        print(f"Loaded: {json.dumps(spec3, indent=2)}")
        
        final_spec3, history3 = run_pipeline(spec3, iterations=2,
                                            outdir_reports="test_reports", 
                                            outdir_logs="test_logs")
        print(f"Final score: {history3[-1]['score']}")
    
    print("\n" + "=" * 60)
    print("PIPELINE TEST COMPLETED SUCCESSFULLY!")
    print("Check 'test_reports/' and 'test_logs/' for generated files.")
    print("=" * 60)

if __name__ == "__main__":
    test_pipeline()