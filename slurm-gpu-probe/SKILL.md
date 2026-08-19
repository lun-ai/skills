---
name: slurm-gpu-probe
description: Probe GPU resources on a Slurm cluster to inform GPU-heavy job decisions (LLM inference/training, vLLM servers, agent experiments). Use whenever the user asks which GPUs are free/available, which GPU type or count to request, which node or partition to target, whether an N-GPU job would start now or queue, or before writing an sbatch/srun request for a GPU job. Provides a ready-made availability report script plus the raw sinfo/squeue primitives for custom probing.
---

# Slurm GPU Probe

Informative skill: a modular, programmatic entry point for probing GPU
availability on a Slurm cluster before committing to a resource request.

## Quick answer: run the bundled script

```bash
~/.claude/skills/slurm-gpu-probe/scripts/check_gpus.sh           # summary + per-node table
~/.claude/skills/slurm-gpu-probe/scripts/check_gpus.sh -n        # summary by GPU type only
~/.claude/skills/slurm-gpu-probe/scripts/check_gpus.sh -p gpu    # restrict to partition(s)
~/.claude/skills/slurm-gpu-probe/scripts/check_gpus.sh -e h200:4 # WHEN would gpu:h200:4 start?
```

(Also symlinked at `~/check_gpus.sh`. Run from a login node, never a compute node.)

Example output:

```
TYPE      TOTAL   USED   FREE  UNAVAIL  MAX/NODE
l40s          8      0      8        0         8
h200         16      8      8        0         7
a100         48     36     12        0         4

NODE               TYPE   FREE/TOT  CPUfree  MEMfree  STATE      NEXT_END  PARTITIONS
codon-gpu-001      h200       7/8        120    1413G  mixed      -         gpu,short_gpu
codon-gpu-007      a100       4/4         48     449G  idle       -         ihpc,short_gpu
...
```

## Interpreting the report for job decisions

- **FREE** = allocatable now (nodes in idle/mixed/allocated/completing state).
  **UNAVAIL** = GPUs on drained/down/planned nodes; "planned" means the whole
  node is promised to an already-scheduled job — do not count on them.
- **MAX/NODE** is the largest free block on a single node: the ceiling for a
  single-node multi-GPU job. Requesting more than MAX/NODE of that type means
  the job queues until GPUs drain.
- A free GPU is only schedulable if the node also has **free CPUs and memory**
  (CPUfree/MEMfree columns). A node can have free GPUs and 0 free CPUs —
  effectively unusable. Size `--cpus-per-task`/`--mem` to what the target node
  actually has left.
- **PARTITIONS** tells you which `-p` reaches each node; some nodes are only
  reachable via specific partitions (e.g. an `ihpc`-only node).
- **NEXT_END** = earliest scheduled end of a *visible* running GPU job on that
  node. Caveat: clusters with `PrivateData=jobs` (like EBI codon) hide other
  users' jobs, so NEXT_END and the pending-demand section cover only the
  user's own jobs. To answer "when would my request start" despite hidden
  jobs, use `-e <type>:<count>` — it runs `sbatch --test-only`, which asks the
  scheduler itself and prints estimated start time, node, and partition:

  ```
  $ check_gpus.sh -e h200:8
  sbatch: Job N to start at 2026-08-20T15:49:31 ... on nodes codon-gpu-001 in partition short_gpu
  ```

Decision heuristic: pick the GPU type whose MAX/NODE ≥ GPUs needed, check the
target node has enough CPUfree/MEMfree, then confirm with `-e type:count`
before submitting. Prefer typed `--gres=gpu:<type>:<n>` so the scheduler
doesn't give a weaker GPU than the workload needs.

Cluster-specific submit rules (EBI codon, discovered empirically): do NOT pass
`-p gpu` (the submit plugin rejects it — request GPUs via `--gres` and the
scheduler routes the job), and `--mem` or `--mem-per-cpu` is mandatory:

```bash
sbatch --gres=gpu:h200:2 --cpus-per-task=8 --mem=64G --time=4:00:00 job.sh
```

## Modular primitives (for custom probing)

Use these directly when the question doesn't fit the script's report:

```bash
# Per-node GPU config vs in-use (the core primitive the script builds on)
sinfo -N -h -O "NodeList:26,StateLong:18,Gres:40,GresUsed:44,CPUsState:18,Memory:12,AllocMem:12,Partition:20"
#   Gres      = installed, e.g. gpu:h200:8(S:0-1)
#   GresUsed  = allocated, e.g. gpu:h200:1(IDX:4)  -> free = installed - used
#   CPUsState = Allocated/Idle/Other/Total

# Full detail for one node (exact TRES accounting)
scontrol show node <node>          # CfgTRES vs AllocTRES lines

# What GPU types/partitions exist at all
sinfo -N -h -o "%N %P %G" | awk '$3 ~ /gpu/'

# Own GPU jobs: state, node, scheduled end
squeue -h -u "$USER" -o "%i %T %N %e %b"

# Estimated start time for a hypothetical request without submitting it
sbatch --test-only --gres=gpu:a100:4 --mem=8G --time=1:00:00 --wrap=true
```

Node-state suffixes in `sinfo` output: `-` planned for a future job, `$`
maintenance reservation, `*` unresponsive, `~` powered down. Treat base states
drained/draining/down/maint/planned as unavailable.

## Notes

- The script is generic Slurm (parses `Gres`/`GresUsed`); only the header's
  "types on this cluster" comment is site-specific.
- `sbatch --test-only` is the only way to get a start-time estimate when other
  users' jobs are hidden — it asks the scheduler itself instead of predicting.
- For orchestrating the jobs themselves (launchers, lifecycle, readiness
  probes), use the companion `slurm` skill; this skill is read-only probing.
