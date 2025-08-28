#!/usr/bin/env python3
"""
Demo script showcasing the Prompt-to-JSON Agent capabilities.
This script demonstrates all major features with example inputs.
"""

import json
import os
from main import parse_prompt, run_pipeline

def demo_examples():
    """Run demo with various example prompts."""
    
    print("=" * 70)
    print("PROMPT-TO-JSON AGENT DEMO")
    print("=" * 70)
    
    examples = [
        {
            "name": "Free Text Prompt",
            "input": "Build a mobile app for food delivery with GPS tracking",
            "iterations": 2
        },
        {
            "name": "Structured Prompt", 
            "input": "Title: Library Management; Description: Digital library system with book search and borrowing; Owner: Sarah Johnson; Priority: high; Requirements: user registration, book catalog, due date tracking, fine calculation",
            "iterations": 3
        },
        {
            "name": "Emergency System",
            "input": "Create an emergency response system for hospitals with real-time alerts",
            "iterations": 2
        }
    ]
    
    for i, example in enumerate(examples, 1):
        print(f"\n{'-' * 50}")
        print(f"DEMO {i}: {example['name']}")
        print(f"{'-' * 50}")
        print(f"Input: {example['input']}")
        
        # Parse and run pipeline
        spec = parse_prompt(example['input'])
        print(f"\nInitial JSON:")
        print(json.dumps(spec, indent=2))
        
        final_spec, history = run_pipeline(
            spec, 
            iterations=example['iterations'],
            outdir_reports=f"demo_reports",
            outdir_logs=f"demo_logs"
        )
        
        print(f"\nFinal Score: {history[-1]['score']}/100")
        print(f"Improvements Made: {len(history)} iterations")
        
        # Show key improvements
        if len(history) > 1:
            initial_score = history[0]['score']
            final_score = history[-1]['score']
            improvement = final_score - initial_score
            print(f"Score Improvement: +{improvement} points")
    
    print(f"\n{'=' * 70}")
    print("[SUCCESS] DEMO COMPLETED!")
    print("[INFO] Check 'demo_reports/' and 'demo_logs/' for detailed results")
    print("[INFO] Run 'streamlit run app.py' for interactive web interface")
    print("[INFO] Use 'python main.py --help' for CLI options")
    print("=" * 70)

if __name__ == "__main__":
    demo_examples()