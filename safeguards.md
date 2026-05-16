# Unity MCP Safeguards

*Known error patterns. Each ## block is checked against every error by log_mcp.py.*
*Format: Pattern (regex), Applies to (tool name or *), Suggestion (fix)*

## read_console types as string

Pattern: "types".*string|types.*str
Applies to: read_console
Suggestion: Pass types as a JSON array, not a string. Use ["error"] not "error". Example: {"types": ["error"]}

## Invalid format value

Pattern: invalid.*format|format.*invalid|unknown.*format
Applies to: read_console
Suggestion: Valid format values are: plain, detailed, json. Do NOT use "full".

