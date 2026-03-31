# Observability Skill

## When to use this skill
Use when the user asks about errors, failures, system health, logs, or traces.

## Service names in VictoriaLogs
- Backend: `Learning Management Service`
- Qwen API: `Qwen Code API`

## Investigation strategy

### Step 1 — Count errors first
Use `logs_error_count` with service name `Learning Management Service`.

### Step 2 — Search logs for details
Use `logs_search` with query: `_stream:{service.name="Learning Management Service"} AND severity:ERROR`

### Step 3 — Fetch trace if trace_id found
Use `traces_get` with the trace_id from the log entry.
Use `traces_list` to browse recent traces.

## How to present results
- Summarize: how many errors, which service, what type, when
- State root cause clearly (e.g. DB connection refused)
- If no errors found, say the system looks healthy
