# Primitive Asset Creator agent kit

Use this kit from Claude Code, Codex, Grok or another runner that can make HTTPS requests and run Python 3. The model and its search/image tools run in that runner. This kit connects the runner to one owner-issued workspace; it does not start a model service itself.

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
| Read current workspace state | `{"action":"snapshot"}` |
| Submit model JSON | `{"action":"submit","model":{}}` |
| Finish | `{"action":"finish","outcome":"completed|blocked|failed","note":"Result and evidence references"}` |

Tool calls return MCP-style `content` and `isError`. A successful HTTP response is not enough: inspect `isError`, validation reports, revisions and saved output. On conflict, re-read state before retrying; on a timeout, inspect the snapshot before replaying a write. Invalid/revoked keys, expired work and another workspace's objects must remain inaccessible.

Identity metadata is reported by the runner. Key possession authenticates access to the allocated workspace; it does not prove which vendor/model generated a request. `reason` must never contain hidden chain of thought.

Run client checks with `python3 -m unittest discover -s tests`.
