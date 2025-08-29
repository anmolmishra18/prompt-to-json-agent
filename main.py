import os
import json
import argparse
from datetime import datetime
from evaluator.criteria import score_spec
from evaluator.feedback import suggest_fixes, apply_feedback
from evaluator.report import generate_report

def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def timestamp():
    return datetime.now().strftime("%Y%m%d_%H%M%S")

def parse_prompt(prompt):
    import re
    spec = {}
    
    # Look for Priority: value pattern
    priority_match = re.search(r'priority:\s*(\w+)', prompt, re.IGNORECASE)
    if priority_match:
        spec["priority"] = priority_match.group(1).lower()
        prompt = re.sub(r'priority:\s*\w+\.?', '', prompt, flags=re.IGNORECASE).strip()
    else:
        spec["priority"] = "medium"
    
    # Look for Title: value pattern
    title_match = re.search(r'title:\s*([^;.]+)', prompt, re.IGNORECASE)
    if title_match:
        spec["title"] = title_match.group(1).strip()
        prompt = re.sub(r'title:\s*[^;.]+[;.]?', '', prompt, flags=re.IGNORECASE).strip()
    else:
        spec["title"] = prompt[:30].strip()
    
    # Use remaining text as description
    spec["description"] = prompt.strip()
    spec["requirements"] = ["basic validation", "report generation"]
    
    return spec

def run_pipeline(spec, iterations):
    ensure_dir("reports")
    ensure_dir("logs")
    
    history = []
    print("\nInitial JSON:")
    print(json.dumps(spec, indent=2))
    
    for i in range(1, iterations + 1):
        score, details = score_spec(spec)
        suggestions = suggest_fixes(spec, score, details)
        
        history.append({
            "iteration": i,
            "score": score,
            "spec": spec.copy(),
            "suggestions": suggestions
        })
        
        generate_report(spec, score, details, "reports", iteration=i)
        
        if not suggestions:
            break
            
        spec = apply_feedback(spec, suggestions)
    
    # Save feedback log
    logpath = os.path.join("logs", f"feedback_log_{timestamp()}.json")
    with open(logpath, "w") as f:
        json.dump(history, f, indent=2)
    
    print(f"\nFinal JSON:")
    print(json.dumps(spec, indent=2))
    print(f"Reports saved in 'reports/', logs in '{logpath}'")
    
    return spec, history

def append_daily_log(honesty, discipline, gratitude, integrity=None):
    ensure_dir("reports")
    log_path = os.path.join("reports", "daily_log.txt")
    ts = timestamp()
    
    with open(log_path, "a") as f:
        f.write(f"=== {ts} ===\n")
        if integrity:
            f.write(f"Integrity: {integrity}\n")
        f.write(f"Honesty: {honesty}\n")
        f.write(f"Discipline: {discipline}\n")
        f.write(f"Gratitude: {gratitude}\n\n")

def main():
    parser = argparse.ArgumentParser(description="Prompt-to-JSON Agent with RL feedback")
    parser.add_argument("--prompt", type=str, help="Prompt text to convert to JSON")
    parser.add_argument("--sample", type=str, help="Sample JSON file path to process")
    parser.add_argument("--iterations", type=int, default=3, help="Number of RL iterations (1-10)")
    args = parser.parse_args()
    
    try:
        if args.sample:
            if not os.path.exists(args.sample):
                print(f"Error: File '{args.sample}' not found")
                return
            with open(args.sample, "r") as f:
                spec = json.load(f)
        elif args.prompt:
            spec = parse_prompt(args.prompt)
        else:
            print("Error: Provide --prompt 'text' or --sample path/to/file.json")
            print("Examples:")
            print("  python main.py --prompt 'Create a student management system'")
            print("  python main.py --sample samples/spec1.json --iterations 2")
            return
        
        if args.iterations < 1 or args.iterations > 10:
            print("Error: Iterations must be between 1-10")
            return
            
        final_spec, history = run_pipeline(spec, args.iterations)
        
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in file - {e}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()