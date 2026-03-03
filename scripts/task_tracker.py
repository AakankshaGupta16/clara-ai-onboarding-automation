import os
import json

def create_task(account_id, version):
    os.makedirs("../tasks", exist_ok=True)

    task_file = "../tasks/tasks.json"

    task_entry = {
        "account_id": account_id,
        "version": version,
        "status": "Agent Generated"
    }

    if os.path.exists(task_file):
        with open(task_file, "r") as f:
            tasks = json.load(f)
    else:
        tasks = []

    tasks.append(task_entry)

    with open(task_file, "w") as f:
        json.dump(tasks, f, indent=4)

    print(f"Task created for {account_id} ({version})")