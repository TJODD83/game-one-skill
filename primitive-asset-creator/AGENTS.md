# Primitive Asset Creator — external agent working order

Work on the single workspace in the owner's handoff packet. Read this file, then the bundled [WORKING_ORDER.md](WORKING_ORDER.md), [SHAPE_GAUNTLET.md](SHAPE_GAUNTLET.md), the gateway `context` response and the current `tools` schemas. The server response is authoritative for this workspace, its input and currently available operations. The toolkit does not provide an LLM, image generator or internet search service; use the tools actually available to your runner and record any missing capability.

## 1. Connect and identify this runner

1. Obtain the gateway root URL and scoped key from the owner's **+ / copy** handoff. The entry gateway is `https://primitive-agent-entry.tjodd.chatgpt.site` unless the owner supplies an updated address. Put the URL in `PRIMITIVE_AGENT_URL` and key in a secret `PRIMITIVE_AGENT_KEY` environment variable. Do not write the key into source, git, chat, notes, command arguments, artifact names or URLs. An interactive client can read it through a hidden prompt.
2. Run `python3 primitive_agent.py login --provider PROVIDER --model MODEL --reason "Brief task summary or runner setting"`. Report the model identifier supplied by the execution environment. If unavailable, say `unknown`; do not guess. Provider/model/settings are agent-reported, not independently authenticated.
3. `reason` means a short public work summary or exposed runner setting. Never submit hidden chain of thought, internal deliberation or private reasoning transcripts.
4. Run `context` and `tools`. Retain the returned workspace, run, revision and tool schemas. Confirm the supplied object name, source mode, attachment and owner instructions. A successful connection creates a work record, not a finished object.
5. Work only within this key's workspace. Other agents may run simultaneously in their own spaces. Never use IDs copied from another agent or attempt. Preserve past submissions.

The client has no required third-party Python packages. Use its help for exact arguments. Requests are authenticated `POST /api` calls. Other CLI tools can implement the same JSON protocol; no browser session is needed when the gateway accepts your key.

## 2. Prepare a clean attempt

Use the new workspace and empty file allocated for this handoff. Do not reuse a prior model as if it were new. Keep input references, generated references, mesh, UV, recorded observations and output version linked to this workspace. Read the actual server context before creating projects or selecting IDs.

Send a heartbeat while actively working and before a long operation. Local work does not renew the server contact lease. While waiting, keepalive sends liveness-only heartbeats every 30 seconds for a bounded 15 minutes by default; see README commands. Read context after an interruption. Only the same valid key and exact registered provider/model may explicitly resume an interrupted unfinished running workspace, preserving its run, files and history. Active work uses heartbeat; revoked, expired or terminal work must not be resumed silently or rebound to another runner.

## 3. Find or inspect the source

- **Name input:** search for the exact requested object using an actually available search tool. Record the search query, considered candidates, selected source URL, source image and why it was selected. Describe uncertain dimensions and hidden surfaces.
- **Image input:** inspect the saved attachment returned by context. Use it directly and bypass web search. Keep the original image and its provenance.
- Inspect a batch of actual images with a real vision-capable tool. Call `review_reference_candidates` with the actual query (name mode) or attachment reference name (image mode), source URLs, inspection method/tool and each image's evidence. Answer all nine questions: object match, people, occlusion, clipping, front, side, top, sharpness and background separation.
- Reject candidates with people, obscured/clipped geometry, the wrong object or blur. Unknown critical answers remain unresolved. Prefer a clean full-object front/side three-quarter image; prioritize actual front, side and top coverage. The server scores your supplied observations and does not run person detection or verify the image itself.
- Select a usable candidate with a factual reason. For a rejected attachment, request a replacement and keep web search skipped. A segmentation or depth tool is optional only if actually available and useful; log its real output and uncertainty. Neither tool recovers hidden evidence or substitutes for references.

Use the gateway's live reporting tools to record starts and actual results. When reporting events, follow the current schema, UUID/revision rules and allowed URL format. A note about a search does not execute a search.

## 4. Generate and review six views

1. Create an owned reference project from the actual image in the format accepted by the current tool schema. Inspect it and its revision.
2. Use `prepare_multiview_reference` to obtain the generic instruction. Attach the source to a real available image generator. Record provider, prompt, input, start, wait, returned output or failure. If no generator is available, use the returned `generatorFallback`: export the actual source image plus exact prompt to a capable generator/owner, share no workspace key, and keep the stage blocked/awaiting returned artifacts. Copying a request does not dispatch a worker. The original authenticated runner must receive and inspect six actual PNG/JPEG views, with an actual sheet optional, then import them with the pinned source revision. Do not rebind its invitation to another provider/model. Maintain real heartbeats while waiting. Explicitly resume only an eligible interrupted workspace using its registered identity; terminal or expired invitations need a new supported attempt.
3. Review the complete sheet and each crop. Layout is **front, back, left / right, top, bottom**. Check alpha/background, exact cell boundaries, orientation, clipping, object identity and contradictory details. Generated/hidden views are estimates, not calibrated measurements.
4. Save six actual crops using the upload-views command or current multiview-set tool. Local names are front/back/left/right/top/bottom with PNG/JPG/JPEG extensions. Independent views use images_hash; an optional actual sheet uses sheet_hash and exact grid crop dimensions. Keep source revision, dimensions and labels. Do not fill missing images, fabricate a sheet or describe model renders as generated references. The README lists command options and image/request limits.
5. Inspect the saved set. Link it to this attempt through the supported job/scene APIs. Recheck all views after model changes.

Front, side and top are the priority three views. If only those exist, record partial evidence and keep the missing six-view pipeline unresolved. Never replace a missing generated view with the original image, a repeated crop or a render of the current model.

This is the six-view module: its events, timer and last reached stage belong to this attempt. Its saved images must not appear as another agent's current reference.

## 5. Trace and build the main shape

1. Inspect the source and choose the observed view. Keep perspective, scale and hidden geometry uncertainty explicit.
2. Create a named outline job/project with the actual source. Respect gate order: accept/review the reference before tracing when the tool requires it.
3. Trace ordered authored nodes using actual pixel-to-outline coordinates. Prefer supported batch operations for speed; record actual points and measured operation duration. Keep a closed, non-self-intersecting silhouette.
4. Validate the outline, then choose depth and any mirrored width based on visible evidence or an explicitly marked estimate.
5. Review lips, integral/separate boards and panel thickness before applying supported geometry. Use current schemas and actual tool output. A lip plan does not create a lip.
6. Review each node's curvature and horizontal/vertical/angular routing against the views. Save supported per-node decisions with evidence and current revision. A connected depth station does not prove a selectable cap route or complete quad flow.
7. Check taper, curve and world/view alignment across the source images. Do not report automatic cross-view fitting when the current operation accepts manually supplied values.
8. Save an actual scene draft only through a supported constructor. Reopen/inspect its geometry. Keep draft status until the required quality checks pass.

## 6. Build supported details

Review visible features generically rather than inserting a fixed arcade part list. For each proposed detail, record source/view, host object, actual face/group, silhouette, location, depth/height, operation and uncertainty. Choose a supported primitive, hole, recess, mound, separate component or outline operation.

Discover saved face IDs with `inspect_saved_feature_faces`: omit `face_indices`, page with `face_offset` and `face_limit` (1–500), and follow `nextOffset` until null. IDs are global for that saved mesh; do not guess later IDs from the first page or combine pagination with selection. Reinspect after geometry changes.

Check the real current capability list first. Existing planners may validate a proposed boundary without editing the mesh. General multi-face holes/mounds, automatic feature placement, independent internal layers and per-node cross-depth curves are not universally available. Mark each missing operation blocked, retain the proposed parameters and attempt independent available stages. Never rename a planner result as built geometry.

Check actual connectivity, manifold state, degenerates, normals, intersections, intended holes, hierarchy and source alignment after changes. Keep separately moving objects separate; preserve shared connected topology where appropriate.

## 7. UV, texture and verification

1. Inspect actual UV islands, direction, bounds, overlap, degeneration, seams, stretch and density. Numerical checks do not prove paintability or appearance.
2. Preserve the shape's current supported UV policy. A face-contained circular box-hole UV mode is not a generic solution for every silhouette, cylinder, hole or mound.
3. Align the six references to the actual scene. Choose visible pixels by face orientation and occlusion; reject background and contradictory/uncertain regions.
4. Transfer or bake **albedo/base colour only** using a real supported tool. Do not bake shadows, AO, highlights, reflections or lighting into base colour. Keep AO separate.
5. A 96×96 view-to-UV diagnostic is a low-resolution draft check, not a final production bake. Report its exact coverage/conflict limits. If final transfer is unavailable, record it blocked.
6. Review the saved model, atlas, source images and cross-view fit. Record the current scene/reference revisions. Geometry edits invalidate earlier checks.

## 8. Save, submit and finish

1. Save through the available model/job tools or the gateway's `submit` action using the accepted model JSON contract. Retain the returned artifact IDs, revisions and validation results. Do not submit executable code as a model.
2. Reinspect the saved submission or request a `snapshot`. Confirm that the expected output exists and belongs to this workspace.
3. Record duration, furthest actual stage, tool results, known failures and missing gates. Supply usage only when the provider returns measured numbers; use null/unavailable otherwise.
4. Send `finish --outcome completed|blocked|failed --note "Factual result and evidence IDs"`. A completed agent report does not by itself pass independent quality gates or win the leaderboard. Use `blocked` for missing required tools/gates and `failed` for an attempted operation that failed.
5. Read back the final server state. The active viewer should undock finished/expired work while retaining its attempt in history. Never delete other agents' data or clear the database to create a blank viewer.

## Stage order and live evidence

`request → search (name only) → select_reference → vision_source → generate_views → wait_views → crop_views → review_views → workspace → trace_outline → check_outline → review_lip → apply_lip → set_depth → route_nodes → shape_depth → layers → select_faces → plan_details → build_details → check_geometry → build_uv → check_uv → transfer_colour → review_texture → save_model → final_review`

For each actual operation record **started**, optional **progress**, then **completed**, **blocked** or **failed**. Keep a heartbeat for liveness. Include the real stage, current image/view, artifact/reference ID and concise evidence summary when supported. The server observes calls to its own endpoints; external search, vision and generation are agent-reported unless that provider supplies independent receipts. Do not fabricate progress percentages, screenshots, token counts, tool calls, model identity, geometric gates or a successful finish.
