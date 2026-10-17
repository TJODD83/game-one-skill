# Lot #10 · Clean-Room Cold-Sandbox Runner & Goal Tower Shipper (`t10_sandbox_shipper`)

- **City Block**: `block-3`
- **Property Lot**: `Lot #10` (`lot-10`)
- **Executable Script**: `Tools/blender/mtd_forge/tools/t10_sandbox_shipper.py`
- **Skill Endpoint**: `GET /skill/lot-10.md`

## 1. Diagnostic Question (Image-Agnostic)
> **Question**: Can the entire 10-Lot chain (t01..t10) run end-to-end in a fresh cold sandbox directory from just the City Block's reference image and base prefab, pass every budget gate, and qualify for the City Block's Goal Tower Top 3?

## 2. Expected Structured Answer Schema
```json
{lots_passed: 10, lots_total: 10, llm_interventions: 0, manifest_sha256: str, reward_score: float, tower_qualified: true}
```

## 3. Deterministic Method & Algorithm (Works Across Any Reference Image)
1. Create an isolated qa_output/sandbox_<run_id>/ directory. 2. Execute t01..t09 sequentially, verifying each Lot's output contract and hard gate before chaining. 3. Lock the SHA-256 manifest, compute Reward = Quality / (1 + 0.01*sec + 0.001*tokens), and promote to the Block's Goal Tower if 10/10 PASS.

## 4. Input & Output Contracts
- **Input Contract**: `All Lot #1..#9 outputs in qa_output/sandbox_<run_id>/`
- **Output Contract**: `ledger.json + locked experiment manifest (SHA-256) + Goal Tower Podium placement`
- **Replaces Manual LLM Thought**: Proves the entire 10-tool chain builds the asset from scratch deterministically and gates the Leaderboard.

## 5. Hard Gate & Chain-Hook End Requirement
> **HARD GATE**: 10/10 Lot Gates PASS in 1-shot cold sandbox with 0 manual LLM edits; otherwise BLOCKED from Goal Tower

To unlock Lot #10 and qualify for the City Block's **Goal Tower**, the worker MUST pass:
```bash
POST /api/lots/10/validate
Authorization: Bearer p0_<worker_key>
Content-Type: application/json

{"target": "Semi2", "sandbox_id": "cold_run_01"}
```
If `validate` returns `FAIL`, the worker is **BLOCKED** from ascending the Goal Tower Leaderboard until the tool passes.
