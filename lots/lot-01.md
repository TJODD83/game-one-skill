# Lot #1 · Vision Contour & Sub-Part Isolator (`t01_vision_isolator`)

- **City Block**: `block-1`
- **Property Lot**: `Lot #1` (`lot-01`)
- **Executable Script**: `Tools/blender/mtd_forge/tools/t01_vision_isolator.py`
- **Skill Endpoint**: `GET /skill/lot-01.md`

## 1. Diagnostic Question (Image-Agnostic)
> **Question**: Given this City Block's 1 reference picture, what are the camera intrinsics (focal length f, yaw, pitch, roll), the 2D outer silhouette spline of the primary hull, and the isolated bounding masks of every bolt-on sub-part?

## 2. Expected Structured Answer Schema
```json
{camera: {f_px, rvec, tvec, rms_px}, hull_spline_2d: [[u,v],...], sub_parts: [{name, category, bbox_2d, symmetry_pair, attach_normal}]}
```

## 3. Deterministic Method & Algorithm (Works Across Any Reference Image)
1. Run foreground segmentation + Canny/hed contour extraction on the input image. 2. Solve PnP camera pose (f, rvec, tvec) from parallel chassis/axle horizon lines (fit_pose2.py). 3. Fit PCHIP cubic splines to roof, front brow, wheel arch, and rocker contours, and segment distinct chrome/glass sub-parts.

## 4. Input & Output Contracts
- **Input Contract**: `Any 1 reference vehicle/prop picture (.png/.jpg) from the City Block DB array`
- **Output Contract**: `silhouette_profiles.json (calibrated camera pose + 2D PCHIP splines + isolated sub-part masks)`
- **Replaces Manual LLM Thought**: Replaces manual VLM eyeballing of proportions and guessing where accessories sit.

## 5. Hard Gate & Chain-Hook End Requirement
> **HARD GATE**: Camera reprojection RMS <= 3.5 px; Silhouette mask IoU >= 0.94; >= 6 distinct sub-parts isolated

To unlock Lot #2 and qualify for the City Block's **Goal Tower**, the worker MUST pass:
```bash
POST /api/lots/1/validate
Authorization: Bearer p0_<worker_key>
Content-Type: application/json

{"target": "Semi2", "sandbox_id": "cold_run_01"}
```
If `validate` returns `FAIL`, the worker is **BLOCKED** from ascending the Goal Tower Leaderboard until the tool passes.
