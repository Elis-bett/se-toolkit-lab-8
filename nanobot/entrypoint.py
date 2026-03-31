import json
import os

config_path = "/app/nanobot/config.json"
resolved_path = "/app/nanobot/config.resolved.json"
workspace = "/app/nanobot/workspace"

with open(config_path) as f:
    config = json.load(f)

# LLM provider
config["providers"]["custom"]["apiKey"] = os.environ.get("LLM_API_KEY", "")
config["providers"]["custom"]["apiBase"] = os.environ.get("LLM_API_BASE_URL", "")

# Model
config["agents"]["defaults"]["model"] = os.environ.get("LLM_API_MODEL", "coder-model")

# Gateway host/port
config["gateway"]["host"] = os.environ.get("NANOBOT_GATEWAY_CONTAINER_ADDRESS", "0.0.0.0")
config["gateway"]["port"] = int(os.environ.get("NANOBOT_GATEWAY_CONTAINER_PORT", "18790"))

# MCP server env vars
if "lms" in config["tools"]["mcpServers"]:
    config["tools"]["mcpServers"]["lms"]["env"] = {
        "NANOBOT_LMS_BACKEND_URL": os.environ.get("NANOBOT_LMS_BACKEND_URL", ""),
        "NANOBOT_LMS_API_KEY": os.environ.get("NANOBOT_LMS_API_KEY", ""),
    }

# Webchat channel
if "webchat" in config.get("channels", {}):
    config["channels"]["webchat"]["access_key"] = os.environ.get("NANOBOT_ACCESS_KEY", "")
    config["channels"]["webchat"]["host"] = os.environ.get("NANOBOT_WEBCHAT_CONTAINER_ADDRESS", "0.0.0.0")
    config["channels"]["webchat"]["port"] = int(os.environ.get("NANOBOT_WEBCHAT_CONTAINER_PORT", "8765"))


# Observability MCP server env vars
if "observability" in config["tools"]["mcpServers"]:
    config["tools"]["mcpServers"]["observability"]["env"] = {
        "VICTORIALOGS_URL": os.environ.get("VICTORIALOGS_URL", "http://victorialogs:9428"),
        "VICTORIATRACES_URL": os.environ.get("VICTORIATRACES_URL", "http://victoriatraces:10428"),
    }

with open(resolved_path, "w") as f:
    json.dump(config, f, indent=2)

os.execvp("nanobot", ["nanobot", "gateway", "--config", resolved_path, "--workspace", workspace])
