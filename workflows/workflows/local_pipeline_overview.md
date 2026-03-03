# Local Automation Workflow Overview

## Stage 1: Demo Processing
- Ingest transcript
- Extract structured memo
- Generate Retell Agent Draft Spec
- Store v1 artifacts
- Create task tracker entry

## Stage 2: Onboarding Update
- Load existing v1 memo
- Extract updated fields
- Merge safely (nested diff)
- Generate v2 memo + spec
- Produce changes.json
- Update task tracker

## Execution
Run:
cd scripts
python run_all.py

Batch processes all demo + onboarding files.

This replaces n8n orchestration with local Python orchestration for zero-cost compliance.