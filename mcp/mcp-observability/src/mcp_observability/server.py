"""MCP server exposing VictoriaLogs and VictoriaTraces as tools."""
from __future__ import annotations
import asyncio
import json
import os
import httpx
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool

VICTORIALOGS_URL = os.environ.get("VICTORIALOGS_URL", "http://victorialogs:9428")
VICTORIATRACES_URL = os.environ.get("VICTORIATRACES_URL", "http://victoriatraces:10428")


def create_server() -> Server:
    server = Server("observability")

    tools = [
        Tool(
            name="logs_search",
            description="Search logs in VictoriaLogs using LogsQL. Example: '_stream:{service.name=\"Learning Management Service\"} AND severity:ERROR'",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "LogsQL query string"},
                    "limit": {"type": "integer", "description": "Max entries to return", "default": 50},
                },
                "required": ["query"],
            },
        ),
        Tool(
            name="logs_error_count",
            description="Count ERROR log entries for a service. Service name example: 'Learning Management Service'",
            inputSchema={
                "type": "object",
                "properties": {
                    "service": {"type": "string", "description": "Full service name, e.g. 'Learning Management Service'"},
                    "limit": {"type": "integer", "default": 500},
                },
                "required": ["service"],
            },
        ),
        Tool(
            name="traces_list",
            description="List recent traces for a service from VictoriaTraces. Service name example: 'Learning Management Service'",
            inputSchema={
                "type": "object",
                "properties": {
                    "service": {"type": "string", "description": "Service name"},
                    "limit": {"type": "integer", "default": 20},
                },
                "required": ["service"],
            },
        ),
        Tool(
            name="traces_get",
            description="Fetch spans for a specific trace ID from VictoriaTraces.",
            inputSchema={
                "type": "object",
                "properties": {
                    "trace_id": {"type": "string", "description": "The trace ID to fetch"},
                },
                "required": ["trace_id"],
            },
        ),
    ]

    @server.list_tools()
    async def list_tools() -> list[Tool]:
        return tools

    @server.call_tool()
    async def call_tool(name: str, arguments: dict | None) -> list[TextContent]:
        args = arguments or {}
        async with httpx.AsyncClient(timeout=10.0) as client:

            if name == "logs_search":
                resp = await client.get(
                    f"{VICTORIALOGS_URL}/select/logsql/query",
                    params={"query": args.get("query", ""), "limit": args.get("limit", 50)},
                )
                return [TextContent(type="text", text=resp.text)]

            elif name == "logs_error_count":
                service = args.get("service", "")
                query = f'_stream:{{service.name="{service}"}} AND severity:ERROR'
                resp = await client.get(
                    f"{VICTORIALOGS_URL}/select/logsql/query",
                    params={"query": query, "limit": args.get("limit", 500)},
                )
                lines = [l for l in resp.text.strip().split("\n") if l.strip()]
                result = {
                    "service": service,
                    "error_count": len(lines),
                    "sample_entries": lines[:5]
                }
                return [TextContent(type="text", text=json.dumps(result, ensure_ascii=False))]

            elif name == "traces_list":
                service = args.get("service", "")
                query = f'_stream:{{resource_attr:service.name="{service}"}}'
                resp = await client.get(
                    f"{VICTORIATRACES_URL}/select/logsql/query",
                    params={"query": query, "limit": args.get("limit", 20)},
                )
                # Extract unique trace_ids
                trace_ids = []
                seen = set()
                for line in resp.text.strip().split("\n"):
                    if not line.strip():
                        continue
                    try:
                        entry = json.loads(line)
                        tid = entry.get("trace_id")
                        if tid and tid not in seen:
                            seen.add(tid)
                            trace_ids.append({
                                "trace_id": tid,
                                "span_name": entry.get("name", ""),
                                "time": entry.get("_time", ""),
                            })
                    except Exception:
                        continue
                result = {"service": service, "trace_count": len(trace_ids), "traces": trace_ids[:10]}
                return [TextContent(type="text", text=json.dumps(result, ensure_ascii=False))]

            elif name == "traces_get":
                trace_id = args.get("trace_id", "")
                query = f'trace_id:"{trace_id}"'
                resp = await client.get(
                    f"{VICTORIATRACES_URL}/select/logsql/query",
                    params={"query": query, "limit": 100},
                )
                spans = []
                for line in resp.text.strip().split("\n"):
                    if not line.strip():
                        continue
                    try:
                        spans.append(json.loads(line))
                    except Exception:
                        continue
                result = {"trace_id": trace_id, "span_count": len(spans), "spans": spans}
                return [TextContent(type="text", text=json.dumps(result, ensure_ascii=False))]

            return [TextContent(type="text", text=f"Unknown tool: {name}")]

    _ = list_tools, call_tool
    return server


async def main() -> None:
    server = create_server()
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())
