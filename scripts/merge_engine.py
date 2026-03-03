import os
import json
from copy import deepcopy
from datetime import datetime


def merge_memos(old_memo, new_data):
    updated_memo = deepcopy(old_memo)
    changes = []

    for key, value in new_data.items():

        # Skip only truly empty placeholders
        if value in ["", None]:
            continue

        # ----------------------------
        # Handle nested dictionaries
        # ----------------------------
        if isinstance(value, dict) and isinstance(old_memo.get(key), dict):

            for sub_key, sub_value in value.items():

                if sub_value in ["", None]:
                    continue

                old_value = old_memo[key].get(sub_key)

                if old_value != sub_value:
                    updated_memo[key][sub_key] = sub_value

                    changes.append({
                        "field": f"{key}.{sub_key}",
                        "old": old_value,
                        "new": sub_value
                    })

        # ----------------------------
        # Handle lists explicitly
        # ----------------------------
        elif isinstance(value, list):

            old_value = old_memo.get(key, [])

            if value != old_value:
                updated_memo[key] = value

                changes.append({
                    "field": key,
                    "old": old_value,
                    "new": value
                })

        # ----------------------------
        # Handle normal fields
        # ----------------------------
        else:

            old_value = old_memo.get(key)

            if old_value != value:
                updated_memo[key] = value

                changes.append({
                    "field": key,
                    "old": old_value,
                    "new": value
                })

    return updated_memo, changes


def save_v2(account_id, updated_memo, changes):
    folder = f"../outputs/accounts/{account_id}/v2"
    os.makedirs(folder, exist_ok=True)

    # Save updated memo
    with open(f"{folder}/memo.json", "w") as f:
        json.dump(updated_memo, f, indent=4)

    # Save structured changelog
    changelog = {
        "account_id": account_id,
        "version_from": "v1",
        "version_to": "v2",
        "timestamp": datetime.utcnow().isoformat(),
        "total_changes": len(changes),
        "changes": changes
    }

    with open(f"../outputs/accounts/{account_id}/changes.json", "w") as f:
        json.dump(changelog, f, indent=4)

    print(f"{account_id} v2 created successfully.")