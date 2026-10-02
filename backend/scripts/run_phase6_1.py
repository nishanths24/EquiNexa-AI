import sys
import subprocess

def run_phase6_1():
    print("=== PHASE 6.1: DYNAMIC TARGET SENSITIVITY ===")
    
    experiments = [
        "EXP-6-HGB-TH-0",
        "EXP-6-HGB-TH-1",
        "EXP-6-HGB-TH-2",
        "EXP-6-HGB-TH-3"
    ]
    
    for exp_id in experiments:
        path = f"backend/app/ai/research/configs/{exp_id}.json"
        print(f"Running {exp_id}...")
        subprocess.run([sys.executable, "backend/scripts/run_experiment.py", "--config", path])

if __name__ == "__main__":
    run_phase6_1()
