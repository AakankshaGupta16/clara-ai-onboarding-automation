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

The system is fully local, reproducible, idempotent, and version-aware.

---

## Architecture

The pipeline consists of two primary stages.

### Pipeline A: Demo → v1

1. Read demo transcript from `dataset/demo/`
2. Extract structured account configuration
3. Generate:
   - `memo.json`
   - `agent_spec.json`
4. Store under:

outputs/accounts/<ACCOUNT_ID>/v1/

---

### Pipeline B: Onboarding → v2

1. Read onboarding transcript from `dataset/onboarding/`
2. Load existing v1 memo
3. Extract updated fields
4. Merge changes safely (no overwrite of unrelated fields)
5. Generate:
   - Updated `memo.json` (v2)
   - Updated `agent_spec.json`
   - `changes.json` (diff log)
6. Store under:

outputs/accounts/<ACCOUNT_ID>/v2/

---

## Folder Structure
```
clara_assignment/
│
├── dataset/
│   ├── demo/
│   └── onboarding/
│
├── outputs/
│   └── accounts/
│       └── SAMPLE/
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
│   ├── run_onboarding.py
│   └── run_all.py
│
├── .gitignore
└── README.md
```
---

## Key Design Decisions

### 1. Structured Schema

All transcripts are converted into a structured memo schema including:

- Business hours  
- Emergency definitions  
- Routing rules  
- Integration constraints  
- Call transfer logic  
- Unknown fields explicitly flagged  

No hallucinated data is inserted.

---

### 2. Versioning Strategy

- v1 is derived strictly from demo transcript.
- v2 updates only fields explicitly confirmed during onboarding.
- A structured `changes.json` logs:
  - Field name
  - Old value
  - New value

Nested dictionary merging ensures only changed sub-fields are updated.

---

### 3. Idempotency

The system is safe to rerun.

If v1 already exists:
SAMPLE v1 already exists. Skipping.

If v2 already exists:
SAMPLE v2 already exists. Skipping.

This ensures:

- No accidental overwrites  
- Safe batch execution  
- Production-style behavior  

---

### 4. Zero-Cost Constraint

The solution uses:

- Pure Python  
- Local file storage  
- No paid APIs  
- No external dependencies  

Fully reproducible on any machine with Python 3.11+.

---

## How To Run

From project root:

cd scripts  
python run_all.py  

This executes:

- Demo pipeline (v1 generation)
- Onboarding update (v2 generation)

Outputs will be generated inside `outputs/accounts/`.

---

## Example Generated Artifacts

Inside:

outputs/accounts/SAMPLE/

You will find:

- v1/memo.json  
- v1/agent_spec.json  
- v2/memo.json  
- v2/agent_spec.json  
- changes.json  

These demonstrate:

- Structured configuration  
- Safe merge logic  
- Version tracking  

---

## What I Would Improve in Production

If production access were available:

- Add structured onboarding form ingestion  
- Add schema validation layer  
- Add database-backed configuration storage  
- Add detailed logging and error handling  
- Improve extraction robustness using NLP models  
- Add automated conflict detection reporting  
- Add UI dashboard for diff visualization  

---

## Summary

This system demonstrates:

- Systems thinking  
- Structured schema design  
- Safe configuration versioning  
- Idempotent automation  
- Zero-cost reproducibility  
- Clean separation between exploratory (demo) and confirmed (onboarding) data  

The workflow behaves like a small internal product rather than a one-off script.
