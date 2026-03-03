import subprocess
import os

def run_script(script_name):
    print(f"\nRunning {script_name}...\n")
    result = subprocess.run(["python", script_name])
    if result.returncode != 0:
        print(f"{script_name} failed.")
    else:
        print(f"{script_name} completed successfully.")

if __name__ == "__main__":
    run_script("extractor.py")
    run_script("run_onboarding.py")