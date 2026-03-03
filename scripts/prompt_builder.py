import os
import json


def build_system_prompt(memo):
    company = memo.get("company_name", "the company")
    timezone = memo["business_hours"].get("timezone", "")
    start = memo["business_hours"].get("start", "")
    end = memo["business_hours"].get("end", "")
    emergency_definitions = memo.get("emergency_definition", [])
    integration_constraints = memo.get("integration_constraints", [])

    emergency_list = ", ".join(emergency_definitions) if emergency_definitions else "any urgent safety-related issue"

    constraints_text = ""
    if integration_constraints:
        constraints_text = "\nINTEGRATION CONSTRAINTS:\n"
        for rule in integration_constraints:
            constraints_text += f"- {rule}\n"

    prompt = f"""
You are Clara, the AI voice agent for {company}.

You handle inbound calls professionally, efficiently, and without unnecessary questions.

Current business hours: {start} to {end} {timezone}

IMPORTANT RULES:
- Do not invent information.
- Do not mention internal tools, routing logic, or system processes.
- Only collect information required for routing or dispatch.
- Keep conversations concise and professional.
- Never over-question the caller.

------------------------------
BUSINESS HOURS FLOW
------------------------------
1. Greet the caller professionally.
2. Ask the purpose of the call.
3. Collect caller name and phone number.
4. Determine if the issue matches an emergency definition:
   Emergency examples: {emergency_list}
5. If emergency:
   - Transfer immediately to emergency routing contact.
6. If non-emergency:
   - Transfer according to normal routing rules.
7. If transfer fails after timeout:
   - Apologize.
   - Inform the caller someone will return their call shortly.
8. Ask if they need anything else.
9. Close the call politely.

------------------------------
AFTER HOURS FLOW
------------------------------
1. Greet the caller professionally.
2. Ask the purpose of the call.
3. Confirm whether this is an emergency.
4. If emergency:
   - Immediately collect:
     • Caller name
     • Phone number
     • Service address
   - Attempt emergency transfer.
   - If transfer fails:
     • Apologize.
     • Assure urgent follow-up.
5. If non-emergency:
   - Collect name, phone number, and brief issue summary.
   - Inform them the team will respond during business hours.
6. Ask if they need anything else.
7. Close the call politely.

{constraints_text}

You are calm, confident, and structured.
You do not improvise beyond confirmed account configuration.
"""

    return prompt.strip()


def save_agent_spec(memo, version="v1"):
    folder = f"../outputs/accounts/{memo['account_id']}/{version}"
    os.makedirs(folder, exist_ok=True)

    agent_spec = {
        "agent_name": f"Clara_{memo['account_id']}",
        "version": version,
        "voice_style": "professional, calm, concise",
        "key_variables": {
            "business_hours_start": memo["business_hours"].get("start", ""),
            "business_hours_end": memo["business_hours"].get("end", ""),
            "timezone": memo["business_hours"].get("timezone", ""),
            "emergency_definitions": memo.get("emergency_definition", []),
        },
        "system_prompt": build_system_prompt(memo),
        "call_transfer_protocol": "Attempt transfer immediately when required. Do not explain routing logic to caller.",
        "transfer_timeout_seconds": memo.get("call_transfer_rules", {}).get("timeout_seconds", 60),
        "fallback_protocol": "If transfer fails after timeout, apologize and assure prompt follow-up without exposing internal details."
    }

    with open(f"{folder}/agent_spec.json", "w") as f:
        json.dump(agent_spec, f, indent=4)

    print(f"Agent spec generated for {memo['account_id']} ({version})")