"""Canonical package for the LMS MCP server."""

from lms_mcp.client import LMSClient
from lms_mcp.server import main

__all__ = ["LMSClient", "main"]
