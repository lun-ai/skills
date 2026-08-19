#!/usr/bin/env bash
# check_gpus.sh — Slurm GPU availability by type and by node. Run from a login node.
#
# USAGE
#   ~/check_gpus.sh                 # summary by GPU type + per-node list
#   ~/check_gpus.sh -n              # summary only
#   ~/check_gpus.sh -p gpu          # restrict to partition(s), comma-separated
#   ~/check_gpus.sh -e h200:4       # ask scheduler when a gpu:h200:4 job would START
#                                   # (sees hidden jobs — the real "when" answer)
#   ~/check_gpus.sh -h              # this help
#
# HOW TO READ THE OUTPUT
#   Summary:
#     FREE      GPUs allocatable right now (on idle/mixed/allocated nodes).
#     UNAVAIL   GPUs on drained/down/planned nodes. "planned" = the whole node
#               is already promised to a scheduled job, so you won't get them.
#     MAX/NODE  largest free block on one node = ceiling for a single-node
#               multi-GPU job. If you need 4 GPUs and MAX/NODE is 3, you queue.
#   Nodes:
#     FREE/TOT  free vs installed GPUs on that node (0 if node unusable).
#     CPU/MEM   free CPUs and unallocated RAM — a free GPU is only schedulable
#               if the node also has CPUs and memory left for your job.
#     NEXT_END  earliest scheduled end of a running GPU job on that node,
#               i.e. when busy GPUs may free up ("-" = none visible).
#               NOTE: this cluster hides other users' jobs (PrivateData), so
#               NEXT_END and "pending demand" only cover YOUR jobs. For busy
#               nodes with "-", when they free up cannot be predicted here.
#     PARTITIONS  which -p values reach this node.
#
# REQUESTING GPUS (typical)
#   sbatch --gres=gpu:h200:2 --cpus-per-task=8 --mem=64G --time=4:00:00 job.sh
#   On this cluster do NOT pass "-p gpu" (submit plugin rejects it) — request via
#   --gres and the scheduler routes the job; --mem (or --mem-per-cpu) is mandatory.
#   Types on this cluster: a100 (4/node), h200 (4 or 8/node), l40s (8/node).
#   codon-gpu-007's a100s are reachable via ihpc/short_gpu only.

set -euo pipefail

PARTITIONS=""
SHOW_NODES=1
while getopts "p:e:nh" opt; do
  case "$opt" in
    p) PARTITIONS="$OPTARG" ;;
    e) # Scheduler's own start estimate for gpu:<type>:<count> — accounts for
       # jobs hidden by PrivateData. Dummy --mem/--time satisfy submit checks;
       # a longer real --time can push the estimate later.
       exec sbatch --test-only --gres="gpu:$OPTARG" --mem=8G --time=1:00:00 --wrap=true ;;
    n) SHOW_NODES=0 ;;
    h) awk 'NR > 1 && !/^#/ {exit} NR > 1 {sub(/^# ?/, ""); print}' "$0"; exit 0 ;;
    *) exit 1 ;;
  esac
done

TMP=$(mktemp); trap 'rm -f "$TMP"' EXIT

# Per-node earliest end time of running GPU jobs -> "node YYYY-MM-DDTHH:MM:SS"
squeue -h -t RUNNING -o "%N;%e;%b" 2>/dev/null | awk -F';' '$3 ~ /gpu/ && $2 ~ /^20/ {print $1";"$2}' |
while IFS=';' read -r nodelist end; do
  for h in $(scontrol show hostnames "$nodelist" 2>/dev/null); do echo "$h $end"; done
done | sort -k1,1 -k2,2 | awk '!($1 in s){s[$1]=1; print}' > "$TMP"

SINFO_ARGS=(-N -h -O "NodeList:26,StateLong:18,Gres:40,GresUsed:44,CPUsState:18,Memory:12,AllocMem:12,Partition:20")
[[ -n "$PARTITIONS" ]] && SINFO_ARGS+=(-p "$PARTITIONS")

sinfo "${SINFO_ARGS[@]}" | awk -v show_nodes="$SHOW_NODES" -v endfile="$TMP" '
function base_state(s) { gsub(/[*~#%$@!+-]+$/, "", s); return s }
function usable(s) { s = base_state(s); return (s == "idle" || s == "mixed" || s == "allocated" || s == "completing") }

# Extract "gpu:<type>:<count>" pairs from a GRES string into arr[type]=count
function parse_gres(str, arr,    n, parts, i, m, f) {
  delete arr
  n = split(str, parts, ",")
  for (i = 1; i <= n; i++)
    if (match(parts[i], /^gpu:[^:(]+:[0-9]+/)) {
      m = substr(parts[i], RSTART, RLENGTH)
      split(m, f, ":")
      arr[f[2]] += f[3]
    }
}

BEGIN {
  while ((getline line < endfile) > 0) { split(line, a, " "); next_end[a[1]] = a[2] }
  close(endfile)
}

{
  node = $1; state = $2; gres = $3; gused = $4; cpus = $5; mem = $6; amem = $7; part = $8
  if (gres !~ /gpu:/) next                      # skip non-GPU nodes
  if (node in seen) {                           # one line per (node,partition): merge
    if (index("," nparts[node] ",", "," part ",") == 0) nparts[node] = nparts[node] "," part
    next
  }
  seen[node] = 1
  nparts[node] = part
  nstate[node] = state
  order[++nn] = node

  parse_gres(gres,  tot)
  parse_gres(gused, use)

  for (t in tot) {
    ntype[node] = (node in ntype) ? ntype[node] "+" t : t
    ntot[node,t] = tot[t]; nuse[node,t] = use[t] + 0
    type_total[t] += tot[t]
    types[t] = 1
    if (usable(state)) {
      free = tot[t] - (use[t] + 0)
      type_used[t] += use[t] + 0
      type_free[t] += free
      if (free > type_maxblock[t]) type_maxblock[t] = free
    } else
      type_unavail[t] += tot[t]
  }

  split(cpus, c, "/"); ncpufree[node] = c[2]; ncputot[node] = c[4]   # A/I/O/T
  nmemfree[node] = int((mem - amem) / 1024)                          # MB -> GB unallocated
}

END {
  printf "%-8s %6s %6s %6s %8s %9s\n", "TYPE", "TOTAL", "USED", "FREE", "UNAVAIL", "MAX/NODE"
  for (t in types)
    printf "%-8s %6d %6d %6d %8d %9d\n", t, type_total[t], type_used[t] + 0, type_free[t] + 0, type_unavail[t] + 0, type_maxblock[t] + 0

  if (show_nodes) {
    printf "\n%-18s %-6s %8s %8s %8s  %-12s %-12s %s\n", "NODE", "TYPE", "FREE/TOT", "CPUfree", "MEMfree", "STATE", "NEXT_END", "PARTITIONS"
    for (i = 1; i <= nn; i++) {
      node = order[i]
      split(ntype[node], tl, "+")
      for (j in tl) {
        t = tl[j]
        free = usable(nstate[node]) ? ntot[node,t] - nuse[node,t] : 0
        ne = (node in next_end) ? substr(next_end[node], 6, 11) : "-"
        sub(/T/, " ", ne)
        printf "%-18s %-6s %5d/%-3d %8d %7dG  %-12s %-12s %s\n", \
          node, t, free, ntot[node,t], ncpufree[node], nmemfree[node], nstate[node], ne, nparts[node]
      }
    }
  }
}'

echo
echo "Pending GPU jobs (yours only — cluster hides other users' queue):"
squeue -h -t PENDING -o "%b %D" 2>/dev/null | awk '
  $1 ~ /gpu/ {
    n = ($2 == "" ? 1 : $2)
    if (match($1, /gpu:[^:,(]+:[0-9]+/)) { split(substr($1, RSTART, RLENGTH), f, ":"); key = f[2]; d[key] += f[3] * n }
    else if (match($1, /gpu:[0-9]+/))    { split(substr($1, RSTART, RLENGTH), f, ":"); key = "(any)"; d[key] += f[2] * n }
    else if (match($1, /gpu:[^:,(]+/))   { split(substr($1, RSTART, RLENGTH), f, ":"); key = f[2]; d[key] += 1 * n }
    else { key = "(any)"; d[key] += 1 * n }
    jobs[key]++
  }
  END {
    if (length(d) == 0) { print "  none"; exit }
    for (t in d) printf "  %-8s %4d GPUs across %d job(s)\n", t, d[t], jobs[t] + 0
  }'
