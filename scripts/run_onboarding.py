import os
import json
from extractor import extract_from_text
from merge_engine import merge_memos, save_v2
from prompt_builder import save_agent_spec
from task_tracker import create_task

def process_onboarding():
    onboarding_folder = "../dataset/onboarding"

    # -------------------------
    # Safety Check
    # -------------------------
    if not os.path.exists(onboarding_folder):
        print("Onboarding folder not found. Please check dataset/onboarding path.")
        return

    for filename in os.listdir(onboarding_folder):
        if filename.endswith(".txt"):

            account_id = filename.replace(".txt", "").upper()

            v1_path = f"../outputs/accounts/{account_id}/v1/memo.json"
            v2_folder = f"../outputs/accounts/{account_id}/v2"

            # -------------------------
            # Ensure v1 exists
            # -------------------------
            if not os.path.exists(v1_path):
                print(f"{account_id} has no v1 memo. Skipping onboarding.")
                continue

            # -------------------------
            # Idempotency Check
            # -------------------------
            if os.path.exists(v2_folder):
                print(f"{account_id} v2 already exists. Skipping.")
                continue

            file_path = os.path.join(onboarding_folder, filename)

            with open(file_path, "r") as f:
                text = f.read()

            # Extract new data from onboarding
            new_data = extract_from_text(text, account_id)

            # Load existing v1 memo
            with open(v1_path, "r") as f:
                old_memo = json.load(f)

            # Merge updates
            updated_memo, changes = merge_memos(old_memo, new_data)

            # Save v2 + changelog
            save_v2(account_id, updated_memo, changes)

            # Regenerate agent spec
            save_agent_spec(updated_memo, version="v2")
            create_task(account_id, "v2")

            print(f"{account_id} v2 created successfully.")


if __name__ == "__main__":
    process_onboarding()