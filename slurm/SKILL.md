---
name: slurm
description: >
  General strategies for orchestrating HPC work through Slurm: submission,
  resource requests, service management, lifecycle actions, and job observability.
  Use when writing or reviewing any Slurm launcher, job script, or HPC workflow.
version: 1.0.0
---

# Slurm HPC Orchestration

Apply the following principles whenever writing, reviewing, or debugging Slurm
launchers, job scripts, and multi-step HPC workflows.

---

## Core Principles

**1. Separate Control Layers**
Keep the workflow split into distinct layers: a launcher on the login node, a
node-setup step on the allocated compute node, and the actual workload or service
start command. This lets submission, provisioning, and execution be changed
independently.

**2. Submit From the Login Node Only**
Perform `sbatch`, `squeue`, `scancel`, and other Slurm commands from the login
node. Reserve compute-node actions for resources granted by the scheduler.

**3. Request Explicit Resources**
Declare wall time, accelerator type and count, CPU count, memory, and all other
scheduling constraints explicitly. Never rely on cluster defaults.

```bash
#SBATCH --time=4:00:00
#SBATCH --gres=gpu:h100:1
#SBATCH --cpus-per-task=8
#SBATCH --mem=64G
#SBATCH --partition=gpu
```

**4. Wait For Confirmed Allocation Only When Needed**
Do not start node-local setup or services until the job is running and the
assigned compute host is known. If the launcher is submit-style and post-hoc
logs are sufficient, it may return immediately after submission.

**5. Configure On The Assigned Node**
Run environment preparation, dependency activation, scratch setup, and hardware
discovery on the allocated compute node. Do not assume the login-node environment
matches runtime conditions.

**6. Start Services Close To The Workload**
Launch inference servers, databases, notebooks, or other runtime services on the
allocated compute node so the consuming workload shares scheduled resources and
network context.

**7. Verify Service Readiness Before Launching Work**
Probe ports, health endpoints, process state, or log messages before starting
dependent jobs.

```bash
until curl -sf http://localhost:${PORT}/health; do sleep 2; done
```

**8. Persist Run Metadata**
Record the job ID, compute hostname, allocated resources, service endpoints,
environment path, and primary log locations in a small machine-readable file
(e.g., `run_meta.json`). Every later status/log/stop action reads this file.

**9. Provide Full Lifecycle Actions**
Design launchers with at least `start`, `status`, `logs`, and `stop` actions so
users can manage long-running jobs without manually reconstructing scheduler state.

**10. Prefer Idempotent Setup**
Make node setup safe to rerun. Provide a way to skip expensive preparation when
the environment is already in place.

**11. Keep Logs Central And Predictable**
Write wrapper, setup, and workload logs to stable paths discoverable from the
stored run metadata. Avoid relying on temporary directories or raw scheduler
output alone.

```bash
#SBATCH --output=logs/slurm_%j_%x.out
#SBATCH --error=logs/slurm_%j_%x.err
```

**12. Clean Up Explicitly**
On stop or failure: cancel the Slurm job, terminate any detached sessions or
background services, and remove stale state files that would confuse the next run.

```bash
stop() {
  local job_id=$(jq -r .job_id run_meta.json)
  scancel "$job_id"
  rm -f run_meta.json
}
```

**13. Distinguish Queue Wait From Runtime Failure**
Report `PENDING`, `RUNNING`, `COMPLETED`, `CANCELLED`, and `FAILED` states
separately. Time spent waiting for resources is not an execution error. For
submit-style launchers that exit before allocation, surface this distinction
clearly in status output.

**14. Expose Safe Runtime Overrides**
Allow controlled overrides for resource requests, environment locations, scripts,
and service parameters via CLI flags or environment variables. This keeps shared
launchers generic across users and clusters.

**15. Treat The Scheduler As Source Of Truth**
Use Slurm state (`squeue`, `sacct`), assigned node information, and recorded
metadata to decide what is running. Do not assume a local shell session reflects
actual job state. Apply this for status checks, attachment logic, and recovery
from stale sessions.

---

## Common Patterns

### Submit and capture job ID
```bash
JOB_ID=$(sbatch --parsable job.slurm)
echo "Submitted job $JOB_ID"
```

### Wait for job to reach RUNNING state
```bash
while true; do
  STATE=$(squeue -j "$JOB_ID" -h -o "%T" 2>/dev/null)
  [[ "$STATE" == "RUNNING" ]] && break
  [[ -z "$STATE" ]] && { echo "Job not found"; exit 1; }
  sleep 5
done
NODE=$(squeue -j "$JOB_ID" -h -o "%N")
```

### Persist metadata
```bash
jq -n \
  --arg job_id   "$JOB_ID"  \
  --arg node     "$NODE"    \
  --arg log_out  "logs/slurm_${JOB_ID}.out" \
  --arg log_err  "logs/slurm_${JOB_ID}.err" \
  '{job_id: $job_id, node: $node, log_out: $log_out, log_err: $log_err}' \
  > run_meta.json
```

### Check job state for status action
```bash
STATE=$(sacct -j "$JOB_ID" --format=State --noheader | head -1 | tr -d ' ')
case "$STATE" in
  PENDING)   echo "Waiting in queue" ;;
  RUNNING)   echo "Running on $(jq -r .node run_meta.json)" ;;
  COMPLETED) echo "Finished successfully" ;;
  FAILED)    echo "Job failed — check $(jq -r .log_err run_meta.json)" ;;
  CANCELLED) echo "Cancelled" ;;
  *)         echo "Unknown state: $STATE" ;;
esac
```
