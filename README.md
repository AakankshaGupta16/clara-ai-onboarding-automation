# Clara AI Onboarding Automation Pipeline

## Overview

This project implements a zero-cost automation pipeline that converts:

**Demo Call Transcript**  
→ Structured Account Memo (v1)  
→ Retell Agent Draft Specification  

Then updates that configuration using:

**Onboarding Transcript**  
→ Structured Merge Update  
→ Version 2 Memo (v2)  
→ Regenerated Agent Specification  
→ Structured Change Log  

The system is:

- Fully local  
- Zero-cost compliant  
- Reproducible  
- Idempotent  
- Version-aware  
- Batch-capable across multiple accounts  

This simulates Clara Answers’ real-world onboarding automation workflow:

**Human conversations → structured operational rules → AI voice agent configuration → version-controlled updates**

---

## Real-World Context

Clara Answers is an AI-powered voice agent built using Retell. It handles inbound calls for service trade businesses such as:

- Fire protection companies  
- Sprinkler and alarm contractors  
- Electrical service providers  
- HVAC and facility maintenance companies  

These businesses require:

- Emergency routing logic  
- After-hours handling  
- Inspection scheduling  
- Call transfer protocols  
- Integration constraints  
- Strict operational rules  

The core challenge is converting exploratory sales conversations into production-ready AI configuration safely and consistently.

This project builds that automation layer.

---

## What This Implementation Covers

This solution satisfies the assignment requirements:

- 5 Demo transcripts processed  
- 5 Onboarding transcripts processed  
- Batch execution across all accounts  
- Versioned memo generation (v1 → v2)  
- Structured changelog (`changes.json`)  
- Retell Agent Draft Spec generation  
- Prompt discipline aligned with business vs after-hours flows  
- Safe nested merge logic  
- Idempotent execution  
- Task tracker simulation (mock Asana replacement)  
- Fully zero-cost architecture  
- Reproducible local execution  

---

## Architecture Overview

### Pipeline A: Demo → v1

For each demo transcript:

1. Extract structured Account Memo JSON  
2. Generate preliminary Retell Agent Draft Spec  
3. Store under:

```
outputs/accounts/<ACCOUNT_ID>/v1/
```

4. Create tracking entry in:

```
tasks/tasks.json
```

Constraints:

- v1 is derived strictly from demo transcript  
- No hallucinated values are inserted  
- Missing data is explicitly flagged under `questions_or_unknowns`

---

### Pipeline B: Onboarding → v2

For each onboarding transcript:

1. Load existing v1 memo  
2. Extract updated fields  
3. Apply safe nested merge logic  
4. Generate:
   - v2 `memo.json`
   - v2 `agent_spec.json`
   - `changes.json`
5. Create tracking entry for v2  

Constraints:

- Only explicitly confirmed onboarding changes are applied  
- Unrelated configuration remains untouched  
- Version history preserved  

---

## Folder Structure

```
clara_assignment/
│
├── dataset/
│   ├── demo/               (5 demo transcripts)
│   └── onboarding/         (5 onboarding transcripts)
│
├── outputs/
│   └── accounts/
│       ├── ACCOUNT1/
│       ├── ACCOUNT2/
│       ├── ACCOUNT3/
│       ├── ACCOUNT4/
│       └── ACCOUNT5/
│           ├── v1/
│           │   ├── memo.json
│           │   └── agent_spec.json
│           ├── v2/
│           │   ├── memo.json
│           │   └── agent_spec.json
│           └── changes.json
│
├── scripts/
│   ├── extractor.py
│   ├── merge_engine.py
│   ├── prompt_builder.py
│   ├── task_tracker.py
│   ├── run_onboarding.py
│   └── run_all.py
│
├── tasks/
│   └── tasks.json
│
├── workflows/
│   └── local_pipeline_overview.md
│
├── .gitignore
└── README.md
```

---

## Key Design Decisions

### 1. Structured Schema

Each transcript is converted into a strict JSON schema including:

- `account_id`
- `company_name`
- `business_hours`
- `office_address`
- `services_supported`
- `emergency_definition`
- `emergency_routing_rules`
- `non_emergency_routing_rules`
- `call_transfer_rules`
- `integration_constraints`
- `after_hours_flow_summary`
- `office_hours_flow_summary`
- `questions_or_unknowns`
- `notes`

Rules:

- No hallucinated values  
- Missing data explicitly flagged  
- Demo assumptions are not treated as confirmed configuration  

---

### 2. Versioning Strategy

- v1 derived strictly from demo transcript  
- v2 derived strictly from onboarding confirmation  
- Nested merge ensures:
  - Only changed sub-fields updated  
  - Unrelated fields preserved  

`changes.json` logs:

- account_id  
- version_from  
- version_to  
- timestamp  
- total_changes  
- field-level differences  

Ensures auditability and traceability.

---

### 3. Prompt Discipline

The generated Retell Agent Draft Spec includes structured call handling logic.

#### Business Hours Flow

- Greeting  
- Ask purpose  
- Collect name and phone  
- Determine emergency  
- Transfer per routing rules  
- Fallback if transfer fails  
- Ask if anything else  
- Close politely  

#### After Hours Flow

- Greeting  
- Ask purpose  
- Confirm emergency  
- If emergency:
  - Collect name, number, address immediately  
  - Attempt transfer  
  - Fallback if transfer fails  
- If non-emergency:
  - Collect required details  
  - Confirm business-hour callback  
- Close politely  

Agent behavior:

- No hallucination  
- No internal tool exposure  
- Minimal necessary questioning  
- Clear transfer and fallback protocols  

---

### 4. Idempotency

Safe to rerun.

If v1 exists:

```
ACCOUNT1 v1 already exists. Skipping.
```

If v2 exists:

```
ACCOUNT1 v2 already exists. Skipping.
```

Prevents duplication and accidental overwrites.

---

### 5. Batch Processing

Run entire dataset with:

```
cd scripts
python run_all.py
```

Automatically:

- Processes all demo transcripts  
- Applies onboarding updates  
- Generates v1 and v2 outputs  
- Updates task tracker  

---

### 6. Task Tracker (Mock Integration)

Instead of Asana (paid API), a zero-cost local tracker is used:

```
tasks/tasks.json
```

Each v1 and v2 generation logs:

```
{
  "account_id": "ACCOUNT1",
  "version": "v2",
  "status": "Agent Generated"
}
```

This simulates workflow automation integration while remaining zero-cost compliant.

---

### 7. Zero-Cost Compliance

- Pure Python  
- Local JSON storage  
- No paid APIs  
- No paid LLM usage  
- No paid orchestration tools  
- Fully local execution  

Reproducible on any machine with Python 3.11+.

---

## Example Output Per Account

```
outputs/accounts/ACCOUNT1/
```

Contains:

- v1/memo.json  
- v1/agent_spec.json  
- v2/memo.json  
- v2/agent_spec.json  
- changes.json  

Demonstrates structured configuration, safe merging, and version tracking.

---

## What I Would Improve With Production Access

- Real Asana API integration  
- Database-backed memo storage  
- Conflict detection dashboard  
- Schema validation layer  
- NLP-based extraction enhancement  
- UI diff viewer  
- Containerized deployment  
- Admin dashboard  

---

## Summary

This system demonstrates:

- Systems thinking  
- Structured schema design  
- Safe configuration versioning  
- Clean v1 vs v2 separation  
- Explicit change tracking  
- Prompt hygiene discipline  
- Idempotent automation  
- Batch processing capability  
- Zero-cost reproducibility  

The workflow behaves like a small internal automation product rather than a one-off script.