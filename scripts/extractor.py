import os
import json
import re
from copy import deepcopy
from prompt_builder import save_agent_spec
from task_tracker import create_task

BASE_SCHEMA = {
    "account_id": "",
    "company_name": "",
    "business_hours": {
        "days": [],
        "start": "",
        "end": "",
        "timezone": ""
    },
    "office_address": "",
    "services_supported": [],
    "emergency_definition": [],
    "emergency_routing_rules": {
        "primary": "",
        "secondary": "",
        "fallback": ""
    },
    "non_emergency_routing_rules": "",
    "call_transfer_rules": {
        "timeout_seconds": "",
        "retry_policy": "",
        "fail_message": ""
    },
    "integration_constraints": [],
    "after_hours_flow_summary": "",
    "office_hours_flow_summary": "",
    "questions_or_unknowns": [],
    "notes": ""
}


def extract_from_text(text, account_id):
    memo = deepcopy(BASE_SCHEMA)
    memo["account_id"] = account_id

    text_lower = text.lower()

    # Company name extraction
    company_match = re.search(
        r"(?:company name is|our company name is)\s+(.+?)[\.\n]",
        text_lower
    )
    if company_match:
        memo["company_name"] = company_match.group(1).strip()
    else:
        memo["questions_or_unknowns"].append("Company name not found")

    # Business hours extraction
    hours_match = re.search(
        r"open\s+from\s+(\d+\s*[ap]m)\s+to\s+(\d+\s*[ap]m)",
        text_lower
    )
    if hours_match:
        memo["business_hours"]["start"] = hours_match.group(1).strip()
        memo["business_hours"]["end"] = hours_match.group(2).strip()
    else:
        memo["questions_or_unknowns"].append("Business hours not clearly defined")

    # Emergency detection
    if "sprinkler leak" in text_lower:
        memo["emergency_definition"].append("sprinkler leak")

    return memo


def save_memo(memo):
    folder = os.path.abspath(f"../outputs/accounts/{memo['account_id']}/v1")
    os.makedirs(folder, exist_ok=True)

    with open(os.path.join(folder, "memo.json"), "w") as f:
        json.dump(memo, f, indent=4)


if __name__ == "__main__":
    demo_folder = os.path.abspath("../dataset/demo")

    # Safety check
    if not os.path.exists(demo_folder):
        print("Demo folder not found. Please check dataset/demo path.")
        exit()

    for filename in os.listdir(demo_folder):
        if filename.endswith(".txt"):

            account_id = filename.replace(".txt", "").upper()
            account_folder = os.path.abspath(f"../outputs/accounts/{account_id}/v1")

            # --------------------------
            # Idempotency Check
            # --------------------------
            if os.path.isdir(account_folder):
                print(f"{account_id} v1 already exists. Skipping.")
                continue

            file_path = os.path.join(demo_folder, filename)

            with open(file_path, "r") as f:
                text = f.read()

            memo = extract_from_text(text, account_id)
            save_memo(memo)
            save_agent_spec(memo, version="v1")
            create_task(account_id, "v1")

            print(f"{account_id} v1 created successfully.")