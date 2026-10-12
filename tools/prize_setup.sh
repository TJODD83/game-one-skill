#!/usr/bin/env bash
# Set prize rules, fund the pool, open an event and read the result. Run ./g1.sh signin first.
#   ./prize_setup.sh <lot> <entryPrice> <prize> <poolAmount> "<event title>" <days 1-30>
set -euo pipefail; D="$(dirname "$0")"; LOT=$1
"$D/g1.sh" POST /api/lots/$LOT/prize "{\"mode\":\"weekly_top3\",\"prize\":$3,\"entryPrice\":$2}"
"$D/g1.sh" POST /api/lots/$LOT/pool/fund "{\"amount\":$4}"
"$D/g1.sh" POST /api/lots/$LOT/events "{\"title\":\"$5\",\"days\":$6,\"prize\":$3}"
"$D/g1.sh" GET /api/lots/$LOT/prize
