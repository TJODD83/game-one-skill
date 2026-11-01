# Primitive Asset Creator agent kit

Use this kit from Claude Code, Codex, Grok or another runner that can make HTTPS requests and run Python 3. The model and its search/image tools run in that runner. This kit connects the runner to one owner-issued workspace; it does not start a model service itself.

## Discover the v3 modelling order

Read `context`, `tools`, [AGENTS.md](AGENTS.md) and [WORKING_ORDER.md](WORKING_ORDER.md) before acting. New v3 jobs explicitly pass `job_schema_version: 3` to `start_primitive_job`; omitted versions keep legacy v2, and existing invitations/jobs retain their pinned contracts.

The v3 silhouette order uses `record_silhouette_view`, `record_outline_span` and `record_category_features` for a two-pass, named-feature trace without a fixed node target. After lip review and depth, use `configure_outline_node_depth`, `record_depth_contour_review` and `record_depth_band_review` before the surface phase. The current advertised schemas define exact view rows, offsets, source/model revisions, target face IDs and render/operation receipt requirements; a proposal is not applied geometry.

`add_scene_object` creates supported separate components in immutable saved versions. `apply_saved_face_feature` creates supported connected planar recess/mound geometry. `render_saved_model` produces actual untextured model PNGs and persists a server receipt with inspection not asserted. Supported geometry mutations return four PNGs automatically; inspect them and record your observations. If rendering fails after geometry saves, retain the saved model ID and follow `moduleWarnings`; retry rendering instead of duplicating the geometry mutation.

An unavailable image generator leaves generation blocked. V3 can continue supported single-reference modelling with the actual source view, missing views explicitly unavailable, and estimated/category-typical hidden geometry; actual saved-model rendering needs no image generator. This does not resolve missing six-view evidence, unsupported localized/curved lips, arbitrary multi-knot contour fitting or final UV/source-match approval.

The image above your agent card previews geometry actually saved in that key's workshop workspace, including an optional validated `scene.colorAtlas` when it was really saved and still matches the packed UV0 geometry. Local/unsaved CLI models and reference images are not streamed or used as textures. Empty/untraced workspaces stay blank. Saving or changing an artifact refreshes its content revision even if its ID is unchanged; a geometry change invalidates stale saved atlas data. Click the card to inspect that exact workspace in the main viewer. A preview or render receipt does not approve the build.

External runners can use `attach_saved_color_atlas` with model_id, actual PNG/JPEG data_url, encoded width/height and reason (optional color_space/flip_y). It saves a new immutable model with server-computed packed-UV binding: maximum 450,000 data URL characters, 1600 pixels per axis, matching square/portrait atlas aspect and 50,000 geometry vertices. The tool returns four untextured geometry PNGs plus the uploaded atlas image; mapped colour appears in a verified WebGL viewer. It does not generate paint, project a reference or approve texture quality.

Read [AGENTS.md](AGENTS.md) first. [WORKING_ORDER.md](WORKING_ORDER.md) and [SHAPE_GAUNTLET.md](SHAPE_GAUNTLET.md) describe the current workshop tools and limitations.

## Connect

Download/clone the published kit from [TJODD83/game-one-skill/primitive-asset-creator](https://github.com/TJODD83/game-one-skill/tree/main/primitive-asset-creator). Obtain the gateway root and key from the owner's **+ / copy** handoff packet. Keep the key in the runner's secret environment as `PRIMITIVE_AGENT_KEY`. The gateway root is `https://primitive-agent-entry.tjodd.chatgpt.site`. Set `PRIMITIVE_AGENT_URL` to that address, or the exact replacement supplied in a later handoff packet. This toolkit is public. The complete server/editor source is stored separately in the private `TJODD83/odd3dassets` repository. Never commit either secrets or response attachments containing private information.

Run these commands from inside the downloaded `primitive-asset-creator` folder.

```sh
export PRIMITIVE_AGENT_URL=https://primitive-agent-entry.tjodd.chatgpt.site
python3 primitive_agent.py login --provider Anthropic --model MODEL_ID --reason "Build the requested object from its working order"
python3 primitive_agent.py context
python3 primitive_agent.py tools
python3 primitive_agent.py call TOOL_NAME @arguments.json
python3 primitive_agent.py heartbeat --stage trace_outline --message "Tracing the inspected source silhouette"
python3 primitive_agent.py snapshot
python3 primitive_agent.py finish --outcome blocked --note "Required operation unavailable; see recorded evidence"
```

Replace `MODEL_ID` and `TOOL_NAME` using the actual runner and returned schemas. Tool arguments must be a JSON object. The client also accepts a JSON object directly, but file input is safer for large image payloads. Use `--output response.json` before the command to save a response locally. Use `submit model.json` only with a saved workshop model in the gateway's accepted schema.

If the key environment variable is absent, an interactive terminal prompts with hidden entry. Noninteractive runs fail clearly. The client does not accept a key command-line flag and does not follow redirects with a credential.

## HTTP contract

All actions use the exact gateway origin from the handoff packet:

```http
POST /api
Authorization: Bearer <workspace key from secret storage>
Content-Type: application/json
Accept: application/json
```

| Action | JSON body |
|---|---|
| Begin / login | `{"action":"begin","provider":"Anthropic","model":"actual-model-id","reason":"Brief work summary or exposed runner setting"}` |
| Read assigned input and work order | `{"action":"context"}` |
| Discover allowed tool schemas | `{"action":"tools"}` |
| Invoke a tool | `{"action":"tool","name":"tool_name","arguments":{}}` |
| Renew active work | `{"action":"heartbeat","stage":"trace_outline","message":"Short factual update"}` |
| Liveness while waiting | `{"action":"heartbeat"}` |
| Resume interrupted work | `{"action":"resume","provider":"same registered provider","model":"same registered model"}` |
| Read current workspace state | `{"action":"snapshot"}` |
| Submit model JSON | `{"action":"submit","model":{}}` |
| Finish | `{"action":"finish","outcome":"completed|blocked|failed","note":"Result and evidence references"}` |

Tool calls return MCP-style `content` and `isError`. A successful HTTP response is not enough: inspect `isError`, validation reports, revisions and saved output. On conflict, re-read state before retrying; on a timeout, inspect the snapshot before replaying a write. Invalid/revoked keys, expired work and another workspace's objects must remain inaccessible.

Identity metadata is reported by the runner. Key possession authenticates access to the allocated workspace; it does not prove which vendor/model generated a request. `reason` must never contain hidden chain of thought.

Run client checks with `python3 -m unittest discover -s tests`.

## Reference selection and unavailable generators

Before selecting a source, use the current `review_reference_candidates` schema to record a visually inspected batch. It asks about requested-object identity, people, obstruction, clipping, front/side/top coverage, sharpness and background separation. Supplied observations are scored; the server does not detect those properties itself. Prefer a clean full-object front/side three-quarter image and record why it was selected.

If this runner cannot generate images, `prepare_multiview_reference` supplies the exact prompt and a manual handoff/resume contract. Export the source plus prompt to a capable generator or the owner, and return the actual artifacts to the original authenticated runner for inspection/import. Never transfer the workspace key to another provider. Keep the generation stage blocked/awaiting output, and record front/side/top-only evidence as partial. The source image, current mesh render or repeated crops do not count as generated views. No automatic generator dispatch, segmentation model or depth model is installed by this kit.

Saved face inspection supports `face_offset`/`face_limit` pages (up to 500). Follow `nextOffset` until null before choosing actual global face IDs; do not guess IDs outside the returned page.

## Upload generated views from a local folder

The generator can return six separate files. Save them as front.png, back.png, left.png, right.png, top.png and bottom.png in one folder; .jpg or .jpeg may be used instead, with one file per view. Keep the original key with the original runner. The generator does not need that key.

    python3 primitive_agent.py upload-views ./views --source-project-id SOURCE_PROJECT_UUID --source-revision SAVED_SOURCE_REVISION

Use the actual source project ID and exact revision timestamp returned by prepare_multiview_reference. The client reads the files, measures dimensions from their bytes, base64-encodes them, and calls create_multiview_reference_set. Six independent images use a canonical images_hash. It creates no sheet, copies no missing views and performs no image generation.

If the folder also contains an actual sheet.png, sheet.jpg or sheet.jpeg, the client uses the seven-image sheet import instead. That sheet must be 16:9 or 3:2, with exact three-column/two-row crop dimensions in order **front, back, left / right, top, bottom**. It calculates sheet_hash from the actual sheet data URL. Remove an unrelated sheet from the folder before using independent views.

Limits are **1600 pixels per axis**, **450,000 characters per image data URL**, and **3,400,000 bytes for the complete JSON request**. Resize/recompress actual images when needed. The client checks PNG chunk/pixel-stream integrity and PNG/JPEG header dimensions; this is not a visual inspection or full JPEG decoder. Review identity, orientation, clipping, transparency/background and contradictions yourself. Saved views remain estimates.

## Waiting for output and resuming

Local generation, downloads and file work do not contact the server. After five minutes without server contact, a running session is shown as interrupted.

Run a separate terminal with the same secret environment while the original runner waits:

    python3 primitive_agent.py keepalive

This sends only an action heartbeat immediately and every 30 seconds for 15 minutes, then stops. It does not overwrite the current stage/message or claim that tools progressed. Use **--duration SECONDS** (1–3600) and **--interval SECONDS** (10–60) for a bounded wait. A rejected heartbeat, authentication error or Ctrl+C stops the loop. Keepalive does not resume interrupted or finished work.

Read context after an interruption. If it is still the same unfinished workspace, explicitly resume with the same registered identity:

    python3 primitive_agent.py resume --provider REGISTERED_PROVIDER --model REGISTERED_MODEL
    python3 primitive_agent.py snapshot

The same key and matching provider/model are required. Resume keeps the existing run, files and history. Active sessions use heartbeat; completed, blocked, failed, revoked or expired invitations require the owner's next supported action or a new invitation. Never silently rebind a workspace to a different provider/model.
