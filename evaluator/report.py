import os
import json
from datetime import datetime

def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def timestamp():
    return datetime.now().strftime("%Y%m%d_%H%M%S")

def generate_report(spec, score, details, outdir, iteration=None):
    ensure_dir(outdir)
    ts = timestamp()
    
    if iteration is not None:
        base = f"report_iter{iteration}_{ts}"
    else:
        base = f"report_final_{ts}"
    
    report_json = os.path.join(outdir, base + ".json")
    report_txt = os.path.join(outdir, base + ".txt")
    
    # JSON report
    with open(report_json, "w") as f:
        json.dump({
            "spec": spec,
            "score": score,
            "details": details,
            "iteration": iteration
        }, f, indent=2)
    
    # TXT report
    with open(report_txt, "w") as f:
        f.write(f"=== Report {'Iteration ' + str(iteration) if iteration else 'Final'} ===\n")
        f.write(f"Score: {score}\n\n")
        f.write("Details:\n")
        f.write(json.dumps(details, indent=2))
        f.write("\n\nSpec:\n")
        f.write(json.dumps(spec, indent=2))
    
    return report_json, report_txt