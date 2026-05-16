# Unity MCP Skills

Lightweight wrappers for the Unity MCP server — call Unity editor tools from the terminal without loading full MCP schemas.

## Setup

The Unity MCP HTTP server must be running. It starts automatically when Claude Code is open and Unity is running with the MCP plugin.

Default URL: `http://localhost:8080` (configured in `config.json`).

## Available Skills

See `unity/index.md` for the full command list.

## Usage

```
python unity/<skill_name>/skill.py [args]
```

All scripts print JSON to stdout. Errors are prefixed with `ERROR:` and exit with code 1.
