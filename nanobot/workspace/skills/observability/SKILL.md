---
name: observability
description: Use observability MCP tools to query logs and traces
always: true
---

# Observability Skill

## Available tools
- `logs_search` — search structured logs with LogsQL
- `logs_error_count` — count errors for a service over a time window
- `traces_list` — list recent traces for a service
- `traces_get` — fetch a full trace by ID to see span hierarchy

## Strategy: "What went wrong?" or "Check system health"
When the user asks "What went wrong?", "Check system health", or similar:
1. Call `logs_error_count` for service "Learning Management Service" to get recent error count
2. Call `logs_search` with query `_stream:{service.name="Learning Management Service"} AND severity:ERROR` and limit 5 to get recent error details
3. If any log entry contains a `trace_id` field, call `traces_get` with that trace_id
4. Summarize findings in 3-5 sentences — do NOT dump raw JSON
5. Mention: what failed, when it failed, and what the trace shows about where it failed

## Strategy: general error queries
- When the user asks about errors — call `logs_error_count` first
- If error count > 0 — call `logs_search` to get details
- If trace_id appears in results — call `traces_get`

## Formatting
- Summarize concisely — no raw JSON dumps
- Show error counts as plain numbers
- For traces, mention service name, span name, and whether it succeeded or failed
- Keep responses to 3-5 sentences unless user asks for more details
