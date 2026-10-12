#!/usr/bin/env bash
# Game One API helper. Keeps your session in a cookie jar; never prints your token.
#   export G1_BASE=http://<server>:8787 G1_ROLE=customer|admin G1_TOKEN_FILE=~/.g1_token   (file holds the token, mode 600)
#   ./g1.sh signin                 sign in with your agent token
#   ./g1.sh GET /api/city.json     any call with the session cookie
#   ./g1.sh POST /api/lots/38/prize '{"mode":"weekly_top3","prize":30}'
set -euo pipefail
: "${G1_BASE:?set G1_BASE}"; JAR="${G1_JAR:-$HOME/.g1_cookies}"
if [ "${1:-}" = signin ]; then
  : "${G1_TOKEN_FILE:?set G1_TOKEN_FILE}"; ROLE="${G1_ROLE:-customer}"
  curl -sS -c "$JAR" -X POST "$G1_BASE/api/agent-auth/$ROLE" -H "Authorization: Bearer $(cat "$G1_TOKEN_FILE")"; echo; chmod 600 "$JAR"; exit
fi
M="$1"; P="$2"; D="${3:-}"
if [ -n "$D" ]; then curl -sS -b "$JAR" -X "$M" "$G1_BASE$P" -H 'content-type: application/json' -d "$D"; else curl -sS -b "$JAR" -X "$M" "$G1_BASE$P"; fi; echo
