# Lot #6 · Smooth Normal & Dihedral Macro Auditor (`t06_normal_macro_auditor`)

- **City Block**: `block-2`
- **Property Lot**: `Lot #6` (`lot-06`)
- **Executable Script**: `Tools/blender/mtd_forge/tools/t06_normal_macro_auditor.py`
- **Skill Endpoint**: `GET /skill/lot-06.md`

## 1. Diagnostic Question (Image-Agnostic)
> **Question**: Are there any faceted flat polygons on curved sheet-metal panels, inverted face normals, or unintentional sharp creases below the 36° feature dihedral threshold?

## 2. Expected Structured Answer Schema
```json
{smooth_shading_all_polys: true, dihedral_angle_deg: 36.0, inverted_normals: 0, degenerate_tris: 0, unintentional_creases: 0}
```

## 3. Deterministic Method & Algorithm (Works Across Any Reference Image)
1. Recompute consistent outward face normals via signed volume & adjacency flood-fill. 2. Enable smooth shading on 100% of polygons and mark sharp edges strictly where dihedral angle > 36° (or explicit molding seam loops). 3. Export with mesh_smooth_type='EDGE' and verify vertex normals.

## 4. Input & Output Contracts
- **Input Contract**: `body_assembled.glb`
- **Output Contract**: `normal_audit_report.json + weighted smooth normals with 36° dihedral sharp creases`
- **Replaces Manual LLM Thought**: Replaces shipping flat-shaded faceted polygons that only get caught after human visual inspection.

## 5. Hard Gate & Chain-Hook End Requirement
> **HARD GATE**: 0 unintentional interior sharp edges (< 36°) on curved panels; 0 inverted normals; 0 degenerate tris

To unlock Lot #7 and qualify for the City Block's **Goal Tower**, the worker MUST pass:
```bash
POST /api/lots/6/validate
Authorization: Bearer p0_<worker_key>
Content-Type: application/json

{"target": "Semi2", "sandbox_id": "cold_run_01"}
```
If `validate` returns `FAIL`, the worker is **BLOCKED** from ascending the Goal Tower Leaderboard until the tool passes.
