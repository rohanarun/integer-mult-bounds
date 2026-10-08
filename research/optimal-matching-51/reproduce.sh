#!/usr/bin/env bash
# Reproduce the optimal-matching witness on PR #51's graphs. Run from repo root.
# Needs: Python 3.10+, g++ (C++17), numpy+scipy (solver only), and PR #51's rebuild inputs:
#   PR36_SRC  = CrocSwap commit 11817cc source tree
#   EVIDENCE  = hipotures/rad .../checkpoint-1605-recovery/agents/graph/fixtures (gzip records)
set -euo pipefail
D=research/optimal-matching-51; P=research/enlarged-positive-frame-networks; W=${REBUILD_WORK:-/tmp/om51}
mkdir -p "$W/in"
for H in 23 25; do for K in base-parent whole-clones mapped-partitions; do
  gzip -dc "$EVIDENCE/best-positive-negative-$K-$H.json.gz" > "$W/in/$K-$H.json"; done
  python3 "$P/agents/graph/code/rebuild_alternative_selected.py" --source "$PR36_SRC" --work "$W/h$H" \
    --base-parent "$W/in/base-parent-$H.json" --whole-selected "$W/in/whole-clones-$H.json" --selected "$W/in/mapped-partitions-$H.json"
done
g++ -O3 -std=c++17 -include algorithm -I scripts/partial_swap "$D/tools/cprof.cpp" -o "$W/cprof"
for H in 23 25; do
  DAG="$W/h$H/alternatives/round-1/dag.bin"
  python3 - "$W/h$H/alternatives/round-1/selected-links.json" "$DAG" "$W/pr51-$H.uses" <<'PY'
import json,struct,sys
d=json.load(open(sys.argv[1]));n=struct.unpack_from('<4I',open(sys.argv[2],'rb').read(16))[2]
open(sys.argv[3],'wb').write(struct.pack('<2I',n,len(d['links']))+b''.join(struct.pack('<2I',a,b) for a,b in d['links']))
PY
  DUMP_EDGES="$W/edges$H.txt" "$W/cprof" "$DAG" "$W/pr51-$H.uses" -4 $((3*(H+3))) /dev/null
  python3 "$D/tools/solve51.py" $H "$DAG" "$W/opt$H.uses" "$W/edges$H.txt" "$W/pr51-$H.uses"
  cmp <(python3 -c "import struct,sys;r=open(sys.argv[1],'rb').read();k=struct.unpack_from('<2I',r)[1];print(sorted(struct.unpack_from('<2I',r,8+8*i) for i in range(k)))" "$W/opt$H.uses") \
      <(python3 -c "import struct,sys;r=open(sys.argv[1],'rb').read();k=struct.unpack_from('<2I',r)[1];print(sorted(struct.unpack_from('<2I',r,8+8*i) for i in range(k)))" "$D/links-$H.uses") && echo "h=$H pinned links regenerated"
  "$W/cprof" "$DAG" "$D/links-$H.uses" -4 $((3*(H+3))) "$W/profile-$H.json"
done
REBUILD_WORK="$W" python3 "$D/tools/legal51.py"
python3 "$P/code/explicit_profile_composition.py" --axes "$D/axes-optimal-matching.json" --phase "$P/fixtures/phase-pr36.json" \
  --assembly "$P/code/adopted_pr37_balanced_assembly.py" --geometry "$P/agents/geometry/results/both-negative-data-input-audit.json" \
  --data "$P/fixtures/both-negative-data-profile.json" --output "$W/exact-certificate.json"
