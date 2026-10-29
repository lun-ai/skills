# Background job discipline

For long-running work (Slurm jobs, batch API calls), prefer resumable harnesses. A run that
loads already-completed results and skips them on restart makes "cancel and resubmit to pick
up a fix" lossless instead of throwing away partial progress. Verify that a resume actually
skipped existing work (grep the restart log for a "loaded N already-completed" line) rather
than assuming the resume flag did what it says.

If a job-monitoring mechanism reports that it lost track of a job ("no completion record
found, it may have stopped"), that is a statement about the monitor, not the job. Check the
job's actual state directly (queue status, output file, log tail) before reporting anything
as failed. Monitoring infrastructure and job infrastructure fail independently.

Tag job names with the experiment number where the scheduler allows it (`--job-name
E007-signor-full-cv`), so the queue itself shows which experiment each job belongs to.

## Record the job ID once a job is finished and approved

When a job (Slurm, batch API, any scheduler-issued run) has finished *and* the user has
approved its results, record its ID in three places. Append it to the experiment's heading in
the topic file, as in `## E002 — Does retrieval help on SIGNOR? (job 41873920)` or
`(jobs 41873920, 41874115)`. Add it to the `jobs:` attribute of the experiment's registry
row. The run's section heading in `e###/results.md` carries it from submission, with the
review state (`not yet reviewed` until the user approves). Every reported number then traces to its logs without a separate lookup table.

Do not add an ID while the job is still running or before approval: a recorded ID means
"these are the accepted results of this job". If a rerun later supersedes an approved result,
replace the ID once that rerun is approved rather than accumulating stale IDs.
