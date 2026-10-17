# Lot #4 · Topology Feature Cutter & Raised Molding Extruder (`t04_feature_cutter_molding`)

- **City Block**: `block-2`
- **Property Lot**: `Lot #4` (`lot-04`)
- **Executable Script**: `Tools/blender/mtd_forge/tools/t04_feature_cutter_molding.py`
- **Skill Endpoint**: `GET /skill/lot-04.md`

## 1. Diagnostic Question (Image-Agnostic)
> **Question**: Where are the recessed apertures (windshields, side windows, radiator grille, door seams) located on the hull, and how wide must their surrounding pillar/molding rings be so they never collide with the corner fillets?

## 2. Expected Structured Answer Schema
```json
{apertures: [{id, bounds, recess_depth_m, molding_thickness_m, center_divider_bar_m, corner_clearance_m}]}
```

## 3. Deterministic Method & Algorithm (Works Across Any Reference Image)
1. Clamp front windshield and side window outer X/Y bounds inside the flat face prior to the 7-segment corner bevel (|x| <= W/2 - 0.19 m). 2. Knife-project closed contour loops, inset by molding width (0.025 m), extrude raised rubber/chrome trim rings outward (+0.008 m), and recess glass panes inward (-0.028 m) with a center divider pillar.

## 4. Input & Output Contracts
- **Input Contract**: `hull_base.glb + window/grille/door aperture curves from Lot #1`
- **Output Contract**: `hull_molded.glb (recessed split windshields, center pillar bar, raised rubber/chrome gasket rings)`
- **Replaces Manual LLM Thought**: Replaces flat vertex-painted windows that collided with corner fillets on Semi 2.

## 5. Hard Gate & Chain-Hook End Requirement
> **HARD GATE**: Every glass pane surrounded by a closed contour edge loop with >= 0.06 m pillar clearance from corner bevels

To unlock Lot #5 and qualify for the City Block's **Goal Tower**, the worker MUST pass:
```bash
POST /api/lots/4/validate
Authorization: Bearer p0_<worker_key>
Content-Type: application/json

{"target": "Semi2", "sandbox_id": "cold_run_01"}
```
If `validate` returns `FAIL`, the worker is **BLOCKED** from ascending the Goal Tower Leaderboard until the tool passes.
