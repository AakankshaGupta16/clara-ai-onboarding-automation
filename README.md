# Clara AI Onboarding Automation Pipeline

## Overview

This project implements a zero-cost automation pipeline that converts:

Demo Call Transcript  
→ Structured Account Memo (v1)  
→ Retell Agent Draft Specification  

Then updates that configuration using:

Onboarding Transcript  
→ Structured Merge Update  
→ Version 2 Memo (v2)  
→ Regenerated Agent Specification  
→ Structured Change Log  

The system is fully local, reproducible, idempotent, version-aware, and supports batch execution across multiple accounts.

---

## What This Implementation Covers

This solution satisfies:

- 5 Demo transcripts
- 5 Onboarding transcripts
- Batch execution
- Versioned memo generation (v1 → v2)
- Structured changelog (`changes.json`)
- Retell Agent Draft Spec generation
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
   outputs/accounts/<ACCOUNT_ID>/v1/
4. Create tracking entry in:
   tasks/tasks.json

---

### Pipeline B: Onboarding → v2

For each onboarding transcript:

1. Load existing v1 memo
2. Extract updated fields
3. Apply nested merge (safe update, no overwriting unrelated fields)
4. Generate:
   - v2 memo.json
   - v2 agent_spec.json
   - changes.json (diff log)
5. Create tracking entry for v2

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
│           ├── v2/
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

- account_id
- company_name
- business_hours
- office_address
- services_supported
- emergency_definition
- emergency_routing_rules
- non_emergency_routing_rules
- call_transfer_rules
- integration_constraints
- after_hours_flow_summary
- office_hours_flow_summary
- questions_or_unknowns
- notes

No hallucinated values are inserted.  
Missing values are explicitly flagged.

---

### 2. Versioning Strategy

- v1 is derived strictly from demo transcript.
- v2 is derived strictly from onboarding updates.
- Nested dictionary merge ensures:
  - Only changed sub-fields are updated.
  - Unrelated fields remain untouched.
- `changes.json` logs:
  - field
  - old value
  - new value

---

### 3. Idempotency

The system is safe to rerun.

If v1 exists:
```
ACCOUNT1 v1 already exists. Skipping.
```

If v2 exists:
```
ACCOUNT1 v2 already exists. Skipping.
```

This prevents duplication or accidental overwrites.

---

### 4. Batch Processing

The system processes all transcripts automatically:

```
cd scripts
python run_all.py
```

This runs:

- Demo extraction for all demo files
- Onboarding updates for all onboarding files

No manual babysitting required.

---

### 5. Task Tracker (Mock Integration)

Instead of using Asana (paid API), a zero-cost mock tracker is implemented:

tasks/tasks.json

Each v1 and v2 generation creates a structured tracking entry:

```
{
  "account_id": "ACCOUNT1",
  "version": "v2",
  "status": "Agent Generated"
}
```

This simulates workflow automation integration.

---

### 6. Zero-Cost Compliance

- Pure Python
- No paid APIs
- No paid LLM usage
- No paid orchestration tools
- Fully local execution

Meets the assignment’s zero-spend requirement.

---

## Example Output Per Account

For each account:

```
outputs/accounts/ACCOUNT1/
```

Contains:

- v1/memo.json
- v1/agent_spec.json
- v2/memo.json
- v2/agent_spec.json
- changes.json

---

## How To Run

From project root:

```
cd scripts
python run_all.py
```

This will:

- Process all demo transcripts
- Apply all onboarding updates
- Generate versioned outputs
- Create tracking entries

---

## What I Would Improve With Production Access

- Real task tracker integration (Asana API)
- Database-backed memo storage
- Conflict detection dashboard
- Improved NLP-based extraction
- UI diff viewer for v1 → v2 comparison
- Structured onboarding form ingestion
- Deployment as a containerized service

---

## Summary

This system demonstrates:

- Systems thinking
- Structured schema design
- Safe versioned configuration management
- Idempotent automation
- Batch processing capability
- Zero-cost reproducibility
- Clear separation between exploratory (demo) and confirmed (onboarding) data

The workflow behaves like a small internal automation product rather than a one-off script.