# Handover — Game One admin

Public copy for agents that cannot see the private server repo. Written 2026-10-15 07:55 SGT, after the previous Grok admin session ran out of tokens and never committed this file.

The city server is **private**: `TJODD83/game-one`. It does not show up in a public repo list. GitHub returns 404 to any account or GitHub App that has not been granted that repo. The only collaborator is TJODD83. Codex can see it because that app's install includes the repo. Other bots do not, until TJ opens GitHub → Settings → Applications → the bot's install → Repository access, and adds `TJODD83/game-one`. Do not make the server repo public to get around this.

Code search on that private repo also comes back empty even for the owner. Open `TJODD83/game-one` by path. Do not conclude it is missing because a search returned nothing.

The running game is not in git. Address is in the README (`http://100.122.106.125:8787`), tailnet only. Tokens are on the server in `.secrets/agent_tokens/`, never in this repo. A bot that can read git still cannot sign in unless it is on the tailnet. Checked 2026-10-15: that address timed out from outside the tailnet.

## Last commit on the server repo

| | |
|---|---|
| Repo | `TJODD83/game-one` (private) |
| SHA | `e04fc15a848c0e26284f193778c49547045bc53e` |
| Message | Sync bot activity (15:24 SGT) |
| When | 2026-10-14 15:30 SGT |
| Diff | `bot-activity/BOT_ACTIVITY.md` only, +1 / −1 |

Every commit after the 12 Oct initial commit is an activity sync of that one file. No game code since then. The same handover also sits on branch `handover-admin-2026-10-15` in the private repo.

## Where the admin bot stopped

From `bot-activity/BOT_ACTIVITY.md` in the private repo, generated 15:29 SGT on 14 Oct. About 16 hours stale when this was written. The 5-minute sync that writes it had stopped, so "running" is the last report, not a live check.

**g1-admin** (Game One Admin). Started by `tools/bots/run_live.sh` → `node tools/bots/agent.js g1-admin`, guide = `ADMIN.md` in this repo. Token file, on the server only: `.secrets/agent_tokens/g1-admin.token`.

- Reported state: running
- Step: `GET /api/hall/election`
- Stage: concept
- Games built: none
- Economy chain (game live, rules, pool, event): all unchecked
- Last decision, 12 Oct 23:00 SGT: audit the board and scores. Question #1 was not answered within 180s, so it kept its own proposal.

**g1-builder** (same supervisor, `CUSTOMER.md`). Not the admin task.

- CityQuest is live on lot #55, v1, play review pass, score 110 (12 Oct 23:08 SGT).
- Prize pool is not funded. No event announced.
- Last notes are questions at 23:09 and 23:15 SGT on 12 Oct.

Owner-dashboard identities, separate from those two processes:

- `game-one-customer` → `agent-grokbot-customer`
- `game-one-admin` → `agent-grokbot-admin`

Neon Shard Rush on lot #38 was approved and marked live.

`tools/bots/run_live.sh` calls `node tools/bots/activity_report.js` every 5 minutes. That script is not in the git repo. It exists only on the server. If it dies, GitHub goes quiet even when the bots are still in the city.

## Next, on the server, read-only first

Rules in `ADMIN.md` still apply. No burn, no news, no hiding a board post without TJ's OK for that exact item.

1. Confirm `tools/bots/run_live.sh` and `agent.js g1-admin` are actually up.
2. Sign in with the existing admin token. Do not mint one. Do not paste it into git or chat.
3. Continue the audit it already chose: the board, then scores. `GET /api/board`, `GET /api/payouts`, `GET /api/economy`, and `GET /api/lots/<id>/prize` for a scored lot. Record works / partly / missing / broken with the status code.
4. Do not top up a prize pool. That spends TJ's token fund. CityQuest's empty pool stays until TJ says to fund it.
5. Private PR #1 (prize form input) is still open. Leave it alone.

Never commit `.secrets`, tokens, the dev password, or `data/p0.sqlite`.
