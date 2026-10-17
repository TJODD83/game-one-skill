# Lot #2 · Chassis & Wheel-Well Calibrator (`t02_chassis_calibrator`)

- **City Block**: `block-1`
- **Property Lot**: `Lot #2` (`lot-02`)
- **Executable Script**: `Tools/blender/mtd_forge/tools/t02_chassis_calibrator.py`
- **Skill Endpoint**: `GET /skill/lot-02.md`

## 1. Diagnostic Question (Image-Agnostic)
> **Question**: How does the 2D silhouette from Lot #1 map into the target Unity chassis coordinate frame (+Z front, +Y up) so the body clears the monster-truck tires under full suspension compression?

## 2. Expected Structured Answer Schema
```json
{world_aabb: {min:[x,y,z], max:[x,y,z]}, wheelbase_m, front_arch: {y,z,radius_m}, rear_arch: {y,z,radius_m}, frame_rail_y_m}
```

## 3. Deterministic Method & Algorithm (Works Across Any Reference Image)
1. Read wheel axle centers and shock travel from the target Unity prefab (truck_*.prefab). 2. Compute affine scale/translation mapping r2b() from photo silhouette metres to Unity axle centres. 3. Carve cylindrical wheel-well clearance envelopes (R >= 0.545 m) around front and rear axles.

## 4. Input & Output Contracts
- **Input Contract**: `Base Unity prefab (truck_*.prefab) + silhouette_profiles.json`
- **Output Contract**: `chassis_anchors.json (exact world-space AABB, wheel-arch clearances, frame rail Y-plane)`
- **Replaces Manual LLM Thought**: Replaces trial-and-error scaling/translating of the mesh over the monster truck tires.

## 5. Hard Gate & Chain-Hook End Requirement
> **HARD GATE**: Max AABB delta <= 0.015 m vs reference chassis; 0 tire-to-fender intersections under 0.35 m suspension travel

To unlock Lot #3 and qualify for the City Block's **Goal Tower**, the worker MUST pass:
```bash
POST /api/lots/2/validate
Authorization: Bearer p0_<worker_key>
Content-Type: application/json

{"target": "Semi2", "sandbox_id": "cold_run_01"}
```
If `validate` returns `FAIL`, the worker is **BLOCKED** from ascending the Goal Tower Leaderboard until the tool passes.
