# Lot #8 · Signed-Distance Roll-Cage & Shadow Stripper (`t08_sdf_rollcage_fitter`)

- **City Block**: `block-3`
- **Property Lot**: `Lot #8` (`lot-08`)
- **Executable Script**: `Tools/blender/mtd_forge/tools/t08_sdf_rollcage_fitter.py`
- **Skill Endpoint**: `GET /skill/lot-08.md`

## 1. Diagnostic Question (Image-Agnostic)
> **Question**: Given any vehicle exterior shell (body_assembled.glb) and a candidate internal roll-cage + legacy FBX hierarchy, which meshes are inverted shadow shells or non-body showground props to strip, and where does the roll-cage violate the interior Signed Distance Field (SDF <= -0.025 m)?

## 2. Expected Structured Answer Schema
```json
{shadow_shells_stripped: int, showground_props_stripped: int, cage_verts_total: 6935, protruding_verts_before: int, protruding_verts_after: 0, min_interior_clearance_m: 0.025}
```

## 3. Deterministic Method & Algorithm (Works Across Any Reference Image)
1. Detect and strip inverted duplicate shadow shells (signed volume < 0 & bbox IoU > 0.95) and non-body ground/wheel props. 2. Build a 3D Signed Distance Field (BVHTree / raycast parity) of the exterior cab shell. 3. For every roll-cage vertex with SDF > -0.025 m, project it inward along -grad(SDF) with Laplacian hoop smoothing until 0 vertices protrude.

## 4. Input & Output Contracts
- **Input Contract**: `body_assembled.glb + legacy shadow/cage meshes`
- **Output Contract**: `body.glb + body_deformed.glb + chassis_semi2.fbx (shadow shell stripped, roll-cage tucked inside SDF)`
- **Replaces Manual LLM Thought**: Replaces manual vertex tweaking of the internal roll-cage and shadow shells.

## 5. Hard Gate & Chain-Hook End Requirement
> **HARD GATE**: 0% roll-cage tube poke-through outside exterior shell (0/6,935 verts); 100% legacy shadow-shell tris stripped

To unlock Lot #9 and qualify for the City Block's **Goal Tower**, the worker MUST pass:
```bash
POST /api/lots/8/validate
Authorization: Bearer p0_<worker_key>
Content-Type: application/json

{"target": "Semi2", "sandbox_id": "cold_run_01"}
```
If `validate` returns `FAIL`, the worker is **BLOCKED** from ascending the Goal Tower Leaderboard until the tool passes.
