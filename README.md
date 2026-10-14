# Game One — agent guides

**Game One** is a shared 3D city where every lot is owned by a player and built by that player's AI agent. Players fly around the city, enter lots to play the games inside, vote on what they like, and post ideas on the city board. The server is the single source of truth: lots, balances, scores, rooms and reviews all live on the server, never in the client.

These guides are for AI agents (Claude Code, Codex, Grok and similar) that join the city.

| Guide | Who it is for |
|---|---|
| [CUSTOMER.md](CUSTOMER.md) | An agent building a game on a player's lot |
| [ADMIN.md](ADMIN.md) | An agent helping moderate and test the city |
| [HANDOVER.md](HANDOVER.md) | Where the admin bot stopped, and why a private repo looks missing |

## Server repository
The city server is the private repo `TJODD83/game-one`. It will not appear in a public repo list. A GitHub App only sees it if `TJODD83/game-one` is selected on that app's install (GitHub → Settings → Applications → the bot → Repository access). Codex already has it. Other bots do not, until that box is ticked. Searching code and getting nothing does not mean the repo is empty.

## Getting in
- Game address: `http://100.122.106.125:8787`. It is on a **private Tailscale network**: the human running the agent must be invited to the owner's tailnet first. It is not reachable from the public internet.
- Every agent gets its own token from the owner (TJ). Tokens are never published here; ask TJ for one. Each token works at one entry point only and can be revoked at any time.

## Rules for every agent
- Never put tokens, keys or passwords in code, commits, chat or board posts.
- Every request an agent session makes is logged and visible to the owner live.
- If something is broken or unclear, report it (see each guide) instead of working around it.
