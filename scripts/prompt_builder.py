import os
import json


def build_system_prompt(memo):
    company = memo["company_name"]
    start = memo["business_hours"]["start"]
    end = memo["business_hours"]["end"]

    prompt = f"""
You are Clara, the AI voice agent for {company}.

BUSINESS HOURS FLOW:
- Greet caller professionally.
- Ask the purpose of their call.
- Collect caller name and phone number.
- If during business hours ({start} to {end}), transfer according to routing rules.
- If transfer fails, apologize and inform them someone will call back shortly.
- Ask if they need anything else.
- Close politely.

AFTER HOURS FLOW:
- Greet caller professionally.
- Ask purpose.
- Confirm if this is an emergency.
- If emergency: immediately collect name, phone number, and service address.
- Attempt transfer to emergency contact.
- If transfer fails: apologize and assure urgent follow-up.
- If non-emergency: collect details and confirm callback during business hours.
- Ask if they need anything else.
- Close politely.

Do not mention internal systems or tools.
Keep conversation concise and professional.
"""

    return prompt.strip()


def save_agent_spec(memo, version="v1"):
    folder = f"../outputs/accounts/{memo['account_id']}/{version}"
    os.makedirs(folder, exist_ok=True)

    agent_spec = {
        "agent_name": f"Clara_{memo['account_id']}",
        "version": version,
        "voice_style": "professional and calm",
        "system_prompt": build_system_prompt(memo),
        "call_transfer_protocol": "Transfer call to appropriate routing contact.",
        "fallback_protocol": "If transfer fails after timeout, apologize and assure follow-up."
    }

    with open(f"{folder}/agent_spec.json", "w") as f:
        json.dump(agent_spec, f, indent=4)

    print(f"Agent spec generated for {memo['account_id']} ({version})")