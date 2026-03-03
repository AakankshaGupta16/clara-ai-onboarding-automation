import os
import json
from copy import deepcopy


def merge_memos(old_memo, new_data):
    updated_memo = deepcopy(old_memo)
    changes = []

    for key, value in new_data.items():

        # Skip empty values
        if not value:
            continue

        # ----------------------------
        # Handle nested dictionaries
        # ----------------------------
        if isinstance(value, dict) and key in old_memo:
            for sub_key, sub_value in value.items():
                if sub_value and old_memo[key].get(sub_key) != sub_value:
                    changes.append({
                        "field": f"{key}.{sub_key}",
                        "old": old_memo[key].get(sub_key),
                        "new": sub_value
                    })
                    updated_memo[key][sub_key] = sub_value

        # ----------------------------
        # Handle normal fields
        # ----------------------------
        elif old_memo.get(key) != value:
            changes.append({
                "field": key,
                "old": old_memo.get(key),
                "new": value
            })
            updated_memo[key] = value

    return updated_memo, changes


def save_v2(account_id, updated_memo, changes):
    folder = f"../outputs/accounts/{account_id}/v2"
    os.makedirs(folder, exist_ok=True)

    # Save updated memo
    with open(f"{folder}/memo.json", "w") as f:
        json.dump(updated_memo, f, indent=4)

    # Save changelog
    with open(f"../outputs/accounts/{account_id}/changes.json", "w") as f:
        json.dump({
            "version_from": "v1",
            "version_to": "v2",
            "changes": changes
        }, f, indent=4)