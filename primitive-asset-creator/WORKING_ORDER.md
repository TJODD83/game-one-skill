# External workspace entry

For a plus-tile invitation, use the supplied public agent entry URL and workspace bearer key. POST /api with action begin and your provider, model and a brief work summary or reasoning setting. These identity labels are self-reported; the key authenticates access to this workspace. Then action context returns the pinned work order, exact object name, source mode and attachment. Action tools lists the available schemas. Call a tool with action tool, name and arguments. Use the returned runId for report_live_benchmark. The gateway records tool activity automatically; report external search, vision and generation honestly. Heartbeat at least every 30 seconds; a five-minute silence interrupts the active tile. Finish the workspace with a truthful outcome and note. Each plus invitation is isolated; never use another workspace's key or IDs.

The owner-Site claim/key instructions later in this document describe the older signed-in queue. They are not required for a plus-tile external workspace. Its invitation and begin action establish the workspace directly. The gateway cannot supply your search, model subscription or image-generator credentials. Use your runner's tools and record unavailable operations as blocked. Give brief decision summaries, never private chain of thought.

# Outline tool: image-led workflow

The outline tool is an experimental editable panel in the Primitive Asset Workshop. It accepts an image as a visual reference; it does not itself run an LLM, edge detector, segmentation model, camera calibration or automatic 3D reconstruction.

## Evidence and view

1. Load and save the reference in the outline project. The saved image is a resized JPEG and its pixel dimensions and position in the SVG editor are recorded. The original file is not retained.
2. Choose the observed view. Perspective/unknown is the safe default. Treat occluded outlines, depth, dimensions, opposite sides, exact button counts and the back as unknown or estimated. A perspective image is not an orthographic reference.
3. Observe the image using the actual tool available to the agent. State whether the input was inspected visually, processed by an edge detector, or supplied by a person. Never claim edge extraction, tool execution, model identity, token usage, or UI actions that did not happen.
4. For each part decide whether it is a supported primitive or a custom outline. Name the part, the observation and uncertainty. One profile produces one panel; a whole assembly requires separate components and constraints.

## Agent tools and coordinates

The workshop's connected MCP server can create an outline project from a JPEG reference, list projects, inspect a project and return its image, and accept `edit_outline_step` actions. Use `configure_outline_shape` to set panel depth, mirrored pair width, mirror state, the deterministic curve rule, and validated whole-perimeter rounding (`edge_round`). Inspect reports the per-point decisions. These controls do not enable unsupported 3D loop or feature operations. Each action requires the current `updated_at`; a conflict requires reinspection. Actions are `begin`, `point`, and `finish`, with an observed reason. Each accepted action is saved. An unfinished draft does not replace the last closed panel.

The inspector reports the image rectangle in SVG coordinates. Map a displayed image pixel to the outline as follows:

- model x = image x + pixel x / pixel width × image width
- model y = −(image y + pixel y / pixel height × image height)

This aligns to the displayed image, not to physical metres. No image-plane calibration is performed. The editor can replay saved action states. Replay is not a capture of physical mouse movements unless actual cursor events are explicitly recorded.

## Shape and validation

See [Shape creation and UV guide](SHAPE_GAUNTLET.md) for the shared layers and capability boundaries.

Points must form a closed, non-self-intersecting outline. The panel supports deterministic corner rounding based on turn angle, convex/concave classification, curve size and per-point overrides. These rules operate on a drawn contour and do not interpret the image. The shared 3D inspector can select edge loops and side-wall face bands and experimental quad-cap bands; legacy triangular caps stop selection, and transition poles limit regular flow. Holes, mounds, creases and general arbitrary-image reconstruction are not implemented for this shape. The panel depth and mirror separation are adjustable; mirrored copies in the main scene become independent objects. The preview's arcade parts are fixed estimates. The 3D assembly and its separate model-library save are separate from the outline project.

The UV geometry test checks overlaps, bounds, degeneracy and distortion after the curve is generated. The six-view orientation report is diagnostic and uses provisional world axes. It does not repair UVs, prove object semantics, or guarantee readable artwork.

## Usage and provenance

The app cannot see the agent's model identifier, token usage, or monetary cost unless the execution provider explicitly returns those measurements and the agent supplies them. Record unavailable values as null, not zero. A user-entered model name or usage is reported data, not automatically verified. If a vision call reports no token breakdown, mark input/output/image-token figures unavailable. Do not infer image token counts from file dimensions.

For the layered “amazing box out” workflow, angle-scaled outline curves, experimental convex end-edge rounding, its inset and UV limitations, and experimental cap topology and its quality limits, see [SHAPE_GAUNTLET.md](./SHAPE_GAUNTLET.md). Outline points selected from an image are observations; the deterministic curve rule is not image edge detection.

## Individual-node curvature decisions

Use `set_outline_node_curvature` for one node in a saved outline project. Supply its current project revision, zero-based node index, a radius fraction from 0 to 0.4 and/or inward/outward bias from −1 to +1 (null clears that setting), and an evidence-based reason. The tool validates the result and records the action. Reinspect after changes because indices are not stable IDs. The 3D workshop exposes the same local curve amount and in/out bias with numbered control-node guides and on-object drag handles. The bias does not switch a convex corner to concave. This adjusts the 2D outline corner, independently of end-edge rounding across depth.

The service does not run image or shape detection. An agent can examine a supplied image with its actually available tools and decide whether to change a node; it must record the real source and not invent usage. See [SHAPE_GAUNTLET.md](./SHAPE_GAUNTLET.md#individual-outline-node-decisions-in-the-workshop) for current behavior, limits and validation.

The read-only MCP tool `analyze_outline_topology` can propose additional points and world-axis connections on the saved control polygon; supply the actual world matrix for a transformed scene, otherwise it uses identity. These are guides only and do not form a cap quad mesh. See the topology proposals section of the gauntlet; do not report them as generated mesh loops.

The `cap_uv` setting chooses `strips` or experimental `silhouette` (curved bands remain with the face). Always inspect the UV audit: the arcade silhouette candidate currently fails stretch and is not ready for painting. The mesh uses continuous rows only for supported one-interval horizontal slices; other outlines fall back to transition patches.

## Agent job capability check

Call `get_agent_workflow_status` to retrieve the current MCP tool names, shape capability records and the current image-to-shape stage boundaries. Its result is discovery only, not a job, a scene, an automatically enforced sequence, per-job authorisation or a gate pass. Agent-callable empty-scene creation, general scene-feature edits and automatic cross-view fitting remain blocked. An agent may now create and inspect a saved outline draft through the dedicated scene-draft tool; an action log alone is not proof of a scene.

## Reference candidate questions and selection

Before choosing a search image, inspect a batch of actual candidates with your available vision tool and call `review_reference_candidates`. Record the real query, source/image URLs, inspection method/tool, image dimensions when known, and an evidence note for each image. The tool asks these exact questions with `yes`, `no` or `unknown` answers:

1. Does this show the requested object?
2. Are any people visible in the image?
3. Is any part of the object obscured?
4. Is any part cut off by the image edge?
5. Is the front clearly visible?
6. Is a side clearly visible?
7. Is the top clearly visible?
8. Is the object sharp enough to trace silhouette and details?
9. Can the object boundary be separated from the background?

Declared people, occlusion, clipping, object mismatch or blur reject a candidate. Missing visual inspection or unknown critical answers leave it unresolved and prevent selection. The tool ranks supplied observations; it does not fetch images, detect people or independently verify the answers. Review and select a usable candidate with a factual reason. Prefer a clean, complete front/side three-quarter view. Front, side and top coverage are the priority three views; missing coverage remains explicit rather than being filled with guessed geometry. Repeated reviews use the returned review ID/current revision and remain scoped to the same workspace. This new report does not retrospectively change the gates of an older job.

For an attachment request, skip web search and assess the actual saved attachment with its reference name. If the attachment is rejected, record why and request a suitable replacement; do not silently substitute a search result.

Optional segmentation or depth tools are the agent's choice when actually available. A mask may help separate a clear object's boundary; it cannot recover an obscured or clipped object. A depth estimate is not a calibrated dimension or proof of hidden geometry. Record the actual tool/provider, input, output, uncertainty and validation. No segmentation/depth model or paid service is installed or invoked by the candidate-review tool.

## Generated six-view reference

A single perspective image does not determine its hidden views. Use `prepare_multiview_reference` on an owned saved image project to get the generic 3-column × 2-row prompt and source revision. Inspect the source image with the available image tool. If an actual image-generation tool is available in the agent session, attach that source and request the sheet; otherwise record the generation step as blocked. The workshop itself does not call ChatGPT image generation or search the internet.

The layout is FRONT, BACK, LEFT on the first row; RIGHT, TOP, BOTTOM on the second. Import the complete 16:9 sheet in the silhouette workspace, inspect the whole sheet and each crop, then save the linked set and select a view. The 3×2 crop uses exact pixel boundaries. Alternatively an agent can crop the sheet and call `create_multiview_reference_set` with all seven PNG/JPEG images, their dimensions, `sheet_hash` (the SHA-256 of the UTF-8 sheet data URL) and the unchanged source revision. A second import mode accepts exactly six independent PNG/JPEG images labelled front, back, left, right, top and bottom: no sheet or grid is required, and the images may have different dimensions. Supply `images_hash` instead: SHA-256 lowercase hex of `VIEW_ORDER.map(view => view + '\n' + dataUrl[view]).join('\n')` encoded as UTF-8, where VIEW_ORDER is front, back, left, right, top, bottom. The JSON API names these digests `sheetHash` and `imagesHash`. Independent imports validate PNG/JPEG headers and encoded dimensions; this is not image decoding or a check of the pictured content. The set reports `layoutType: independent`, `sheetHash: null`, `imagesHash`, and `sheet: null`; do not synthesize a sheet. Each image must be at most 1600 pixels per dimension and 450,000 data URL characters. External agent requests remain capped at 3,400,000 UTF-8 bytes total: reduce real files locally if necessary, preserving their view identity, and retry only after correcting an oversize error. Saving is atomic; the set records owner, source, revision, hash and view label. Each view is a fresh outline project. A sheet project cannot be used as a silhouette job; choose a cropped view.

Generated panels are **unverified estimates**, not calibrated orthographic measurements. Labels and crop dimensions do not prove the generator placed the correct view in each panel, that the object stayed inside each cell, that its proportions agree between panels, or that hidden details exist. Inspect and reject incorrect panels. Do not treat generated pixels as exact 3D coordinates or claim a model or a UV has been created by this step.

## When this runner cannot generate the views

`prepare_multiview_reference` returns the actual generation prompt, pinned source project/revision, layout and `generatorFallback` instructions. It prepares a request only. If this runner lacks image generation, export the real source image (using `inspect_outline_project`) and the prepared prompt to a capable generator or ask the owner to run it. Do not pass the workspace key or service credentials to a second provider. An active invitation remains bound to its original declared provider/model.

Keep `generate_views`/`wait_views` blocked or awaiting external output until the artifacts actually return. A copied request is not automatic dispatch. The capable generator returns six actual labelled PNG/JPEG images (or a real sheet plus its six exact-grid crops) to the original authenticated runner; that runner inspects them, computes the applicable images or sheet hash and calls `create_multiview_reference_set` with the unchanged source revision. Then inspect the saved set before tracing. The independent return contract is six actual images: front, back, left, right, top and bottom. The legacy grid contract remains seven images including the real sheet. Both remain agent-supplied, visually unverified evidence until reviewed.

If only front, side and top are available, record those three as partial priority evidence and keep the six-view pipeline unresolved. Do not duplicate one image into the missing cells. Neither the original perspective photo nor a projection/render of the current model is a generated reference. Optional depth or segmentation output does not replace generated or observed views.

While the original runner is truly alive it may maintain its lease with real heartbeats. If the workspace expires or ends, obtain a linked retry key and retain source/generation lineage; do not silently resume an expired session. Continue independent available checks and give the exact blocker rather than claiming a finished reconstruction.

## Shared six-view scene inspection

In the 3D workshop, open **Six-view reference + shared scene** and choose a saved six-view set. The same live scene is projected into six fixed orthographic camera frames; the 3D editor and UV view remain available. The fixed frame does not follow later geometry edits until **Frame scene** is requested. Reference-image scale, offset, rotation, opacity and mirror are independent per view and do not move the geometry. They are manual, unverified alignments; orientation, inferred hidden surfaces, inconsistent image proportions and image-to-model fit require review. A generated reference set is not calibrated orthographic evidence. Save the whole scene or selected object after alignment to retain the link and alignment settings.

For a connected agent, `inspect_multiview_reference_set` returns the six owned reference images and provenance. `inspect_saved_scene_six_views` reconstructs a **saved** owned scene through the workshop's geometry generator and returns six reference images, each actual object's projected image bounds, world positions and bounded vertex samples in the shared camera frame. It uses saved image-alignment settings if available, otherwise reports an unaligned initial frame. Neither state proves calibration. It does not inspect live unsaved edits, automatically render or compare image silhouettes, identify surface features or approve a match. For live visual overlays, use the workshop board and its exported board image. Report missing views, visual uncertainty and any sample or geometry limits.

## Record the complete attempt from the request

Start **3D Asset Workshop · session recording** before searching or generating references. Start without a linked job if necessary; select the job after it is created. Add timestamped decision notes for the request, actual search terms and candidate/source choice, image-generation provider/tool and instruction, returned sheet, view review, silhouette/depth decisions, feature observations, checks and blockers. These are supplied notes, not automatic transcripts. The recorder captures its two embedded workshop workspaces, model, UVs and open six-view board; it does not capture outside tabs, the image-generation interface, private reasoning or earlier actions. If a step is unavailable to capture, record the actual gap. Stop and download both video and journal. Never reconstruct unrecorded footage and call it a full recording.

When inspecting a six-view set or saved scene, the image order is reported explicitly: the current source image, when accessible, comes first, then the sheet when applicable, followed by front, back, left, right, top and bottom. The source revision is compared with the revision recorded when the sheet was made. If it is unavailable or different, say so; a current image is not a guaranteed copy of the source at generation time. Review all views against that source, including mismatched features, perspective, occlusion and inferred hidden surfaces. Image blocks are returned together; they are not a single composited picture or an automatic vision call.

## Generic image-to-feature plan

For any object, establish its visible parts and uncertain or hidden areas using the source plus all available views, then trace the main silhouette and choose depth. After each stage review the shared 3D scene and UVs across views. The front cross-depth shape at each silhouette node and exact horizontal/vertical 5/10/10 corner routes through the model are requested capabilities, not the current 2D node curve, midpoint quad cuts or read-only width evaluator. Record them as blocked until actual connected geometry and UVs pass their checks.

Next examine visible scene surfaces and record candidate feature silhouettes, without assuming a subject-specific component list. For each candidate record: source/view and visible evidence; host object and actual face or connected region where known; 2D boundary points, orientation, margins and scale; proposed operation (recess, mound, separate component or unknown); depth/height and its evidence or estimate; confidence, missing views, tool choice and blocker. Trace only with a supported face-local operation, verify placement against other views, and rerun topology, shading and UV checks. The present placement planner handles one supplied planar boundary; it does not discover faces, trace images, apply geometry or place a feature on a profile panel. Do not pretend each render triangle is a separately meaningful surface, or infer precise depth from a single image.

Every accepted feature needs its own named hierarchy entry linked to its host and operation, including the source/view, editable parameters and check status. A recess or mound may still be part of a connected watertight host mesh: a separately selectable logical child is not permission to detach its shared faces. Separately movable parts require their own actual object and attachment. This hierarchy and image-to-feature executor are not yet implemented in the current workshop; record the request as blocked rather than inventing a child or claiming the mesh was modified.

## Node-axis edge-loop check

Use **Check selected node routes** in the workshop to inspect each requested policy and its actual generated depth station. Strict horizontal/vertical loop closure is an optional read-only diagnostic via `audit_outline_node_axis_loops`; it is not a requirement for angular routing or a job gate. A depth station is not proof that its cap route is selectable or closed, and the report does not approve UVs or image fit. Failed or missing station results remain visible.

## Per-node routing and feature silhouette plans

After the source views, silhouette and depth, inspect each visible region and consider whether a particular outline node needs no extra boundary point, horizontal, vertical, both, or an angular route. Call `evaluate_outline_node_routing` on an owned saved outline with explicit zero-based per-node policies; omitted nodes use the current experimental both-axes rule. Angular mode uses the two endpoints of an eligible opposing straight segment to propose a perpendicular direction within the caller's 0–80° limits. Directions are in the silhouette's local face plane; establish the real object's world/view orientation separately. The returned candidate is temporary: points and depth-edge stations may exist, but dashed face paths are guides and the tool does not create corresponding cap edges, save routing choices, adjust the 5/5/5 corner march to the route, or interpret images. Check actual geometry, UV status, deferred matches and node-loop audit. The older comparison controls remain session-only. Separately, newly created scene silhouettes default to horizontal on all nodes. The selected profile's **Selected node route** controls can override one node or all nodes, including horizontal plus angular, and save choices with a model; these controls create depth stations but do not force a cap path. Inspect the relevant reference views and record why each override was chosen; image analysis and application by the agent are not automated. An agent can save an individual node override with `set_outline_node_routing`, supplying the current revision, the source-based reason, a mode, and angle limits where needed. The saved outline passes that choice to newly created profiles. The tool does not modify an existing scene or infer what the image shows. Reinspect after point insertion or removal because indices can change.

Next identify potential host surfaces from the views and trace a generic feature silhouette. `plan_silhouette_feature` checks the supplied local boundary, rounded outline, inward hole or outward mound, requested depth and margin on one caller-supplied planar face. Its depth-derived default rounding is a starting heuristic, not a measured property or applied modifier. Hole plans require supplied host depth to pass. The `view` is an agent-supplied label, not validated scene orientation. The tool does not select real faces, join multiple faces, create the feature, maintain hierarchy, calculate its feature UV, or verify the input against an image. Those operations remain blocked; record the missing capability rather than asserting completion. Recheck the image, node loops and UVs after any future real edit.

## Ordered semantic surface groups

Read the side reference and any usable front, back and top views before assigning surface roles. Identify the authored silhouette nodes in their drawn running order, and record a named group between two nodes with the view, visible observation and intended feature (unknown, hole, mound, silhouette or multiple). A display or control panel is only a candidate when supported by the actual reference; generated views, hidden faces and depths remain estimates. Choose topology choices after considering those candidate feature regions. The agent must report uncertainty and conflicting views rather than assert an image measurement.

The workshop's **Select node surface span** selects the actual across-depth sidewall faces between two authored nodes in forward outline order, wrapping through the end when necessary. A saved named group stores those authored indices, not generated support nodes. Rounding samples, parity splits and routing stations are included in the connected surface but do not become new semantic selection targets. The group can be selected after the mesh is rebuilt, including after an authored node moves. The two boundary corners are included; neighbouring groups may share these corner faces. This tool does not select arbitrary interior cap faces, detect an image feature, edit a hole/mound or approve its UV.

For an owned outline project, `inspect_outline_surface_span` reports the actual selected sidewall triangle count and local bounds; `set_outline_surface_group` validates and saves a named group, intent, view and an evidence note using the current revision; `remove_outline_surface_group` removes a named group with a recorded reason. The group is inherited when a new scene profile is made. This is a supplied observation, not automated vision, calibrated alignment, or an edit to an already saved scene. Inserting or removing a non-boundary authored point in the outline editor adjusts the indices; a saved group boundary cannot be deleted until the group is changed or removed.

## Cross-depth node groups and curves still needed

For each named surface, compare corresponding authored node groups against the side, top and front references. Record which depth, taper, angle and curve are observed, inferred or unknown. A future cross-depth tool must tie each start/middle/end curve control to its moved node group and regenerate connected geometry, so endpoints remain flush as the group moves. Front-view and top-view constraints can disagree; preserve the evidence and require a decision rather than pretending one image determines the whole shape. The existing width-profile tool is temporary, length-based and not this per-node front-and-top dependent curve system. Real multi-face feature silhouettes, hole/mound geometry, curve dependency, feature UVs, and image-to-scene automation remain blocked.


### Profile-wide depth shaping

The workshop can now save local-axis length and height taper plus one shared middle rise on a scene profile. It creates real depth sections and checks geometry. Values are supplied manually; do not describe this as automatic multi-view image fitting, a pillar group, or independent per-node curve controls. It does not change an outline project or expose an agent write command. Compare measured front and top projections with calibrated references before proposing values, and keep UV, normals, symmetry and fit checks open.


### Decide details across the six views

For every relevant face or surface group, review the source and each available front, back, left, right, top and bottom view. Record which view is actually observed, generated, or unavailable; generated details remain proposals. Identify whether the area is plain, texture, silhouette, hole, mound or multiple features. For each proposed feature record its visible footprint (silhouette, circle, rectangle, cross or other), sharp or curved corners, supporting view and observation. Use existing named authored-node spans when they truly cover the host; do not substitute sidewall spans for an interior cap or pretend they select an unrelated screen.

The workshop reports how many current UV-connected islands the selected span touches. Inspect the host's actual selected triangles and current UVs before a feature is built; a region can cross seams, and a UV island is not proof of a feature or image match. Recalculate and audit after geometry changes. `plan_silhouette_feature` can accept an agent-selected sharp or curved option for a supplied planar 2D host boundary. It remains a plan, not a 3D cut, selected-face validation, automatic image inference, or UV approval. The saved outline group operation optionally records `feature_shape`, `corner`, and up to six `observations`; evidence is supplied by the agent, not independently verified. A single group is not a complete multi-feature scene ledger.

For an owned saved model with a square atlas, `inspect_saved_surface_uv` rebuilds and packs the scene, then reports the selected profile span’s actual UV-connected islands and bounds. Object and node indices are zero-based. It is read-only and supports authored-node sidewall spans only; portrait atlases, interior cap footprints and live unsaved scene state are not supported. Island identifiers do not persist through repacking.


The scene workshop now offers authored-node start/end depth, length and height offsets, plus middle bias, and rebuilds connected depth sections. The middle defaults to the line between endpoints. It does not automatically read six-view images or enforce exact horizontal face routes. The agent cannot yet write these settings to an outline or live scene; inspect and compare the actual result and its UVs rather than treating this as completed multiview fitting.


### Lip review and final depth

For new jobs, review each view and apply any supported lip with provisional panel thickness before setting final depth. The job checks the applied whole-cap geometry and its source UV islands. Six-view notes, unobserved surfaces and UV approval remain separate. Existing v1 jobs retain their older post-depth `lip_review`, which records a proposal only. See the detailed new-job order below.


### Detail ledger and all-detail gate

For each view, call `record_primitive_view` with the actual observed or generated source, expected number of visible details and evidence note. Use `unavailable` with a null count when a view is missing. Use `record_primitive_detail` once for each physical detail and list every view where it appears; reuse its ID to update it. Record host, placement, operation, shape, curved or sharp corners, depth, host margin, spacing from neighbours, linked authored nodes and the evidence. Node indices are local authored indices, not synchronized world-space coordinates. The job inspection shows per-view counts, individual blockers, and any comparable same-host and same-view supplied planar footprint spacing checks. Changing a view or detail increments the job version.

A supplied footprint can be checked against a caller-supplied host boundary and margin. Two supplied footprints on the same named host and same view are checked for planar overlap and required spacing. This is an early plan check only: names and coordinates are supplied, host geometry is not selected or verified, and it does not test real 3D collisions, reconstruct an object across views, move linked nodes, apply features or validate UVs. Treat generated views as estimates. The all-detail status remains blocked until actual geometry, view matching, collision and UV checks exist and pass. Do not report a completed model from matching counts or a planar plan.

### Inspect selected feature faces

In the main workshop use **Select feature faces** to add or remove actual mesh faces on the selected object, then **Inspect selected boundary**. Existing face bands and named profile spans can also be inspected. A connected, consistently wound planar selection with one simple boundary produces a local boundary and current UV-island count. Disconnected selections, branching or multiple loops and curved/non-planar hosts are rejected with a reason. Use **Preview feature silhouette** to see a curved or sharp inward contour, with a requested percentage of the smaller local boundary dimension. This is an outline guide only: it does not alter mesh topology, construct a hole or mound, fit a detail to reference views, or approve UVs. Selections and preview are temporary.

For an owned saved model, `inspect_saved_feature_faces` without indices lists up to 500 selectable faces and local centres per page. Start with `face_offset: 0`, use `face_limit` from 1 to 500, then follow `nextOffset` until null to inspect all `faceCount` faces. Listed indices remain global across pages; do not guess face IDs beyond the first page. Pagination cannot be combined with `face_indices`. Reinspect after a geometry revision, then provide indices to inspect their actual connected planar boundary and optionally a silhouette guide. Face IDs and source UVs belong to that saved geometry; they are not stable across regeneration, do not refer to the live scene, and are not a packed-atlas or UV approval. Curved and multi-loop selections require later tools. The caller must still determine a genuine host and feature from the source, views and current scene, and apply only a supported construction tool.


### Required detail work order

After silhouette depth and lip review, start each relevant view by asking which actual object and single face or connected set of faces may host detail. Compare the source and all useful views and identify the current UV island. Then decide whether the area requires a hole, mound, separate object, texture, no work, or remains unknown; do not force geometry onto a plain or textured face. Record each view's expected count, and link one physical detail to all views that show it.

For every required detail, choose the host-derived or drawn silhouette, circle, rectangle, cross or another shape; specify the operation, curved or sharp corners, depth or height, face margin, spacing, evidence, uncertainty and linked authored nodes. Inspect a real connected selection and use a planar footprint/spacing plan only where applicable. Compare the same proposed placement in all relevant views; check actual shared 3D positions and collisions when those tools exist. Consult the shape catalogue before choosing an operation; a missing or inapplicable tool is blocked, not a successful detail.

Construct each supported detail, verify connected geometry, normals and clearance, rerun UV seams, overlap, stretch and orientation checks, and revisit the views. Repeat until every recorded detail on every reviewed view has an actual result. Recheck results after changes to host geometry or the atlas. The detail completion gate cannot pass merely because counts match or an outline preview fits. Current general selected-face feature execution, cross-view node synchronization, 3D collision verification and feature UV approval are not implemented.


### Lip and extrusion order for new jobs

For new jobs, trace the side silhouette using provisional panel thickness. Before final extrusion depth, mirror or node-angle decisions, inspect every available view and record its source and observation with `record_primitive_lip_view`; mark unavailable views as unavailable. For the perimeter, decide whether there is a board/lip, where it sits, its thickness, whether its outer curve follows the silhouette, and whether the region inside it is recessed. Record which faces, intended view, evidence, curved/sharp profile and UV island need review. Unknown is not a completed decision.

If the actual intended host is an entire local end-cap, apply its supported `cap_recess` setting to the owned outline with `configure_outline_shape`, then advance `lip_preflight` with `target: full_endcap`. The job checks the actual deformed geometry and identifies source UV-connected islands, but it does not map a view to the cap, inspect a packed scene atlas or approve stretch, overlap or orientation. Recess depth is a fraction of panel thickness and changes when final panel depth changes; an independent world-space lip depth is not supported. Board thickness independent of panel depth, automatic curve matching, arbitrary single or multi-face lips and automatically executing an LLM decision remain unavailable. The new job stays blocked rather than substitute the whole cap for a different host. If no lip is observed, record the evidence and the uncertainty of missing/generated views. Independent per-node routing edits are still callable outside the job and are not yet blocked by this checkpoint; review the lip before making those edits. Existing v1 jobs retain their prior post-depth lip step.

Next set final depth and mirror where justified. For each relevant view and host face or connected faces, record whether it needs straight inward or outward extrusion, by how much and whether it is a hole, mound, separate object or unchanged. Draw or supply a silhouette in the appropriate view; check margins, adjacent details, and the other views. Consider horizontal, vertical, angular or no additional node per authored node and how routing relates to the intended geometry. Current planners and node choices do not construct general multi-face extrusion, automatically match views or approve UVs; keep those steps blocked until the actual tools and validations pass.


### Optional six-view internal silhouette reference

After reviewing the exterior six views and before deciding lips, panel thickness and internal layers, call `prepare_internal_silhouette_reference` for the owned original. Attach that original and the reviewed exterior sheet to an actually available ChatGPT image-generation tool and request the separate six-view conceptual X-ray/cutaway sheet. Record the provider, prompt, inputs, output and actual recording gaps. Review the six images against the source; visible evidence and inferred hidden silhouettes must remain distinguishable. An inferred panel, board, hole or depth is a proposal, not measured geometry.

Ledger each proposed internal silhouette, its host, layer order, visible/inferred source, lip or no-lip boundary, estimated depth and UV region. A real multi-layer construction and separate internal-image provenance/storage are not implemented, so do not import the conceptual sheet as an ordinary exterior view or claim a layer was built. Mark absent image-generation tool or unsafe/inapplicable construction as blocked. Existing lip preflight is limited to an already-applied whole local cap; per-face and multi-face operations remain outstanding.


### Repeated silhouette layers and face-contained feature UV

For each outer and internal silhouette layer, review each relevant view, trace its contour and place its authored nodes in running order. Match corresponding nodes only when the references support a real correspondence; record absent or unavailable views and generated X-ray suggestions separately. Repeat for all layers, then for every host face and detail. A count, guide or trace is not a generated 3D layer: independent layer meshes, automated node synchronization and completion checks remain open.

The desired feature UV policy keeps the rounded lip, depth wall and floor within the host-face feature footprint, for holes and outward mounds wherever the geometry admits a non-overlapping layout. The feature may use lower pixel density than the host. Check actual UV connectivity, seams, overlap, directional distortion and measured density separately; uniform lower density does not by itself prove that a stretched wall is paintable. Do not waive the existing threshold automatically. When the layout cannot meet it, report the measured block and preserve the source/previous UV option.

The workshop has a selectable face-contained UV mapping for an existing circular **box** hole, with a floor-size percentage and the older separate-strip option. It maps connected wall and floor into the face footprint. This is not a general hole, mound, silhouette or cylinder solution. UV audit and image-based paintability still apply.

### Multi-view texture transfer and approval

After the actual geometry and details are complete, inspect source provenance and register the observed/generated views to the current scene. Verify each silhouette and feature mask, face orientation, UV island, density and existing UV audit. For every target surface, select visible source views using the world-space face angle and scene occlusion; reject background, wrong features and hidden/uncertain pixels. Compare views and report disagreements. Then bake an albedo-only atlas at the target resolution, check missing pixels, view reprojection, feature placement, seams and mip padding, and use AO separately. All checks must refer to the current scene, atlas and reference revision; edits invalidate them.

The six-view board now has a 96 × 96 diagnostic that samples the actual UV triangles using scene world transforms, interpolated surface normals, face direction and full-scene ray occlusion. Green marks samples transferred from the best-facing available view, red marks samples without a visible source and orange marks raw colour disagreement. It rejects overlapping, degenerate, out-of-bounds or unpacked atlas geometry and scenes above 15000 triangles. It checks neither source silhouette masks nor image calibration, lighting, UV seam appearance, feature identity, mip padding, production resolution or visual fidelity. It can show or download a low-resolution draft for review; it never approves a production atlas. Generated images remain estimates and can contain background or lighting; even green samples are not approved. The selected-face and complete-scene work, actual bake and aggregate texture gate remain blocked.

### Two-view authored-node match

On a selected outline panel, choose one authored point and enter the same physical target as X/Y percentages of two reference images. The panel uses the current image transforms, solves one world point, rejects incompatible observations or pairs that do not constrain all three axes, and converts the point to one selected start/end node-depth edit. It preserves the other nodes and their depth controls, runs the existing profile geometry validation and updates the connected scene mesh. Disable linked edits for this operation. It rejects global taper and cap recess and movement beyond the existing 15% bounds. The inputs, registration, derived angles, curves and UVs still require review; rounded curves need not pass through an authored control point. This is not automatic feature detection, automatic matching of all nodes, a scene agent-write tool, a physical layer generator or a complete six-view fit.

### Bounds alignment and exploratory attempts

In the six-view board, Fit six image bounds estimates each reference object bounds from alpha or a plain border background, then uniformly scales and centres each image against the current model projections. Review width and height fit and all views: matching bounds does not match internal features, prove camera calibration, resolve an incorrect silhouette, or make generated images observed. Transparent masks and border-colour masks are heuristics; unclear or cropped images are rejected. The fit is atomic and retains rotation and mirror choices.

When a job gate fails, continue trying independent available stages and record each later outcome using the attempt ledger. The ledger records caller-supplied results and the current outline revision but does not change the blocked gate, create missing geometry or mark the model complete. Record where the actual operation stopped and preserve the full session recording.

### Scene draft after a blocked stage

An agent may call `build_primitive_scene_draft` with a current job version, `uv_mode` (`current` or `strips`) and a reason. The operation creates one new, owned saved model from the actual closed outline and links it to the job. The saved profile includes the selected UV mode and a source revision. The response contains its actual packed UV audit. It neither changes existing saved models nor advances a gate. The outline can be opened in an empty workshop using **Build outline draft scene**; an existing live scene is left intact. Repeat calls are rejected rather than creating duplicates. A draft remains incomplete: later details, source alignment, UV orientation and a final texture require independent checks. Continue with `record_primitive_attempt` for every later stage, including failures.

For texture diagnostics, the six-view board excludes pixels identified as transparent or connected plain-border background before comparing available views. This is an estimated foreground mask, not verified semantic segmentation: it can miss foreground or include wrong features. An image with an unreliable or cropped mask blocks the diagnostic. Remaining view conflicts are still reported and do not pass automatically.

After the draft is linked, `check_primitive_scene_draft` runs independent checks through final review and records the results without changing the current phase. It rebuilds the saved model, checks actual node loops, inspects an example authored surface span, checks geometry and the packed UV atlas, and explicitly records unavailable alignment, layers, features and final texture. An example surface span is not an image-selected feature. This operation does not run the browser texture transfer or create missing details.

## Live build monitor

The site home opens the live build monitor. To make an actual autonomous attempt visible from before search, an authorised agent must explicitly use these tools; the monitor is not a runner and cannot see private model reasoning or calls made in another service:

1. Call `start_live_benchmark` with the exact subject before reference search. Keep its run ID and version.
2. Call `report_live_benchmark` with `action: event`, the run ID, current version and a unique UUID `eventId` for each real action. Supply stage, kind, outcome and a short factual message; use `started` while a real call is pending, then `completed`, `blocked` or `failed` for its actual result. Record a heartbeat only while the runner is actually alive.
3. For a search event include the actual query and up to six actual source candidates; include the image currently inspected when there is an allowed stable HTTPS URL. The monitor accepts only HTTPS URLs without query strings or fragments; do not send credentials, signed links, private reasoning or hidden data. Generated six-view images already saved in the workshop appear from the linked reference set.
4. Once the workshop job exists, call `report_live_benchmark` with `action: attach_job` and its owned `job_id`. The viewer then polls its saved outline and saved draft, UV and reference set; this is a delayed saved-state view, not a video stream of the agent's screen.
5. Report the real `tool` and stable `callId` on results. Supply token counts only when the provider returns them, otherwise leave fields null. Calls without a `callId` and tool name are not counted. If the run version conflicts, inspect and retry the same `eventId`; duplicates are not added.
6. Finish the run with its actual result: `completed`, `failed`, `blocked` or `interrupted`. Completion requires the independent build gates; a monitoring record is not a completed asset.

Stages: `request`, `search`, `select_reference`, `vision_source`, `generate_views`, `wait_views`, `crop_views`, `review_views`, `workspace`, `trace_outline`, `check_outline`, `review_lip`, `apply_lip`, `set_depth`, `route_nodes`, `shape_depth`, `layers`, `select_faces`, `plan_details`, `build_details`, `check_geometry`, `build_uv`, `check_uv`, `transfer_colour`, `review_texture`, `save_model`, `final_review`. Existing jobs can be watched without a benchmark record, but external search/call activity and total usage are not inferred from the job.

## Queued build requests

`list_build_requests` lists saved owner requests; `inspect_build_request` returns the request and, for image mode, the actual reference image. A `name` request requires finding a reference; an `image` request uses the supplied image and skips web search. Retry creates a new request linked to the prior request with the same source and instruction. Requests are queued records; listing a request does not start work. An authenticated claimant can use the claim and lease tools described below, but there is no automatic dispatcher. Never claim an agent ran, a file was produced or a quality gate passed without corresponding evidence. Continue to use the actual run and job reporting tools when an agent performs a request.

## Claiming an existing request

A Site owner can create and revoke agent identity keys in the live monitor. A claimant with the existing authenticated Site connection can call `claim_build_request` with `request_id` and `agent_key`; the stored key label is used for attribution. This verifies possession of an owner-issued key, not the human or model behind it. Keys alone do not grant Site access. A legacy claim may instead use `agent_label`, which is caller supplied and marked as reported. The response includes a one-time per-claim `leaseToken`; keep both secrets private. Call `update_build_claim` with `action: heartbeat` before the 120-second lease expires, providing both the lease token and the same agent key when the claim was key-verified. Revocation prevents further updates. Finish with `action: finish`, a `completed`, `blocked` or `failed` outcome and an evidence note. A completed claim is a worker report, not a validated model. If a lease expires, queue a new retry rather than continuing the expired claim. Claiming does not start an agent and these calls require a working Site-authenticated connection.

## Linking a claimed request to its live run

After claiming and before research, call `start_request_benchmark` with `request_id`, `claim_id`, and `lease_token`; include `agent_key` if the claim used one. This creates or returns the same run for the active claim and links it to the request. Keep both secrets private. The monitor can open that linked run from the request. Report actual activity with `report_live_benchmark`, including search only for name inputs; image inputs use the saved attachment and skip search. Renew the claim before it expires, and finish both the run and claim with an honest outcome. A run record and a claim do not launch an agent or prove asset quality. An expired claim cannot start or resume a run; create a retry.
