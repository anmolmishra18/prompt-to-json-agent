#!/usr/bin/env python3
"""
Demo script showing the complete Prompt-to-JSON Agent workflow
"""
import json
from main import parse_prompt, run_pipeline

def demo():
    print("=== Prompt-to-JSON Agent Demo ===\n")
    
    # Demo 1: Simple prompt
    print("1. Simple Prompt Processing:")
    prompt1 = "Create a student management system"
    spec1 = parse_prompt(prompt1)
    print(f"Input: {prompt1}")
    print(f"Output: {json.dumps(spec1, indent=2)}\n")
    
    # Demo 2: Complex prompt with key:value pairs
    print("2. Complex Prompt with Key-Value Pairs:")
    prompt2 = "title: E-commerce Platform; description: Online shopping with cart and payments; priority: high"
    spec2 = parse_prompt(prompt2)
    print(f"Input: {prompt2}")
    print(f"Output: {json.dumps(spec2, indent=2)}\n")
    
    # Demo 3: RL improvement cycle
    print("3. RL Improvement Cycle (2 iterations):")
    final_spec, history = run_pipeline(spec1, 2)
    
    print("Score progression:")
    for i, h in enumerate(history):
        print(f"  Iteration {h['iteration']}: Score {h['score']}")
    
    print(f"\nFinal improved spec:")
    print(json.dumps(final_spec, indent=2))
    
    print("\n=== Demo Complete ===")
    print("Check /reports/ for detailed reports")
    print("Check /logs/ for feedback history")

if __name__ == "__main__":
    demo()