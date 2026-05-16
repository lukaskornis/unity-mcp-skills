# MCP Skill System — Handoff for New Chat

## What this is

A repo of thin Python CLI wrappers around MCP tool calls, designed so Claude can invoke
Unity/Rider tools without loading full MCP schemas into context. Claude reads a terse
`skill.md`, runs `python skill.py <args>`, reads stdout.

`unity-mcp-skills` is done (36 skills). The same system needs to be built for:

- `rider-mcp-skills` — wraps JetBrains Rider MCP (`mcp__rider__*` tools)
- `rider-debugger-mcp-skills` — wraps Rider Debugger MCP (`mcp__rider-debugger__*` tools)

Both repos go in `/Users/Chill/Documents/`.

---

## How the Unity MCP HTTP bridge works (reference)

The `mcp-for-unity` stdio server also runs an HTTP sidecar at `http://localhost:8080`.

All tool calls go through one endpoint:

```
POST http://localhost:8080/api/command
{"type": "<tool_name>", "params": {...}}
```

Response shape:
```json
{
  "status": "success",
  "result": {
    "success": true,
    "message": "...",
    "_mcp_status": "pending",   // only on async commands
    "data": { ... }             // the actual payload
  }
}
```

Error fields live at `result.message`, `result.error`, or `result.code` — check all three.

Async commands (packages, build) return `{"data": {"job_id": "..."}}` and must be polled:
```
POST /api/command  {"type": "manage_packages", "params": {"action": "status", "job_id": "..."}}
```
Poll until `result._mcp_status != "pending"`.

**For Rider:** The Rider MCP is also stdio-based (Java process). First task in the new chat
is to discover whether it exposes an HTTP bridge and what port/endpoint it uses.
Check `~/.claude/claude_desktop_config.json` for config, then `lsof -iTCP -sTCP:LISTEN`
for listening ports. If there is no HTTP bridge, skills will need to use a different calling
strategy — probe this before writing any skills.

---

## Repo structure (replicate exactly)

```
<name>-mcp-skills/
  CLAUDE.md          — brief description + "see <domain>/index.md"
  config.json        — {"<domain>_mcp_url": "http://localhost:<port>"}
  .gitignore         — .DS_Store  __pycache__/  *.pyc
  <domain>/
    _index.md        — notation header + one-line entry per skill
    _lib.py          — shared helpers (see below)
    <skill_name>.md  — terse usage spec
    <skill_name>.py  — CLI wrapper
```

`_` prefix on shared files so they sort to the top alphabetically.
One `.md` + one `.py` per skill — flat, no subdirectories.

---

## _lib.py — copy and adapt

```python
import json
import os
import sys
import urllib.request
import urllib.error

_root = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))


def _load_config():
    with open(os.path.join(_root, "config.json")) as f:
        return json.load(f)


def _post(url, payload):
    data = json.dumps(payload).encode()
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=10) as resp:
        return json.loads(resp.read())


def coerce(v):
    """Convert CLI string to best Python type."""
    if v.lower() == "true": return True
    if v.lower() == "false": return False
    try: return int(v)
    except ValueError: pass
    try: return float(v)
    except ValueError: pass
    return v


def require(n, usage):
    if len(sys.argv) < n:
        print(f"ERROR: Usage: {usage}")
        sys.exit(1)


def _command_inner(tool, params):
    config = _load_config()
    url = f"{config['<domain>_mcp_url']}/api/command"
    try:
        result = _post(url, {"type": tool, "params": params})
        inner = result.get("result", {})
        if result.get("status") != "success" or not inner.get("success"):
            msg = inner.get("message") or inner.get("error") or inner.get("code") or result.get("error", "Unknown error")
            print(f"ERROR: {msg}")
            sys.exit(1)
        return inner
    except urllib.error.URLError as e:
        print(f"ERROR: MCP server not reachable at {config['<domain>_mcp_url']} — {e.reason}")
        sys.exit(1)
    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(1)


def command(tool, params):
    return _command_inner(tool, params).get("data")


def poll(tool, params, interval=2, max_tries=20):
    """For async commands that return job_id."""
    import time
    inner = _command_inner(tool, params)
    job_id = (inner.get("data") or {}).get("job_id")
    if not job_id:
        return inner.get("data")
    for _ in range(max_tries):
        time.sleep(interval)
        status = _command_inner(tool, {"action": "status", "job_id": job_id})
        if status.get("_mcp_status") != "pending":
            return status.get("data")
    print(f"ERROR: Timed out waiting for job {job_id}")
    sys.exit(1)
```

Replace `<domain>` with `rider` or `debugger`.

---

## _index.md header (copy verbatim)

```
# <arg>=required  [arg]=optional  type after colon  →=returns  !=errors  #=note
```

---

## skill.md format

```
# optional note line for non-obvious constraints (use sparingly)
python <skill_name>.py <req_arg> [opt_arg]
arg:type  description or enum values
→ return_field1 return_field2
! ErrorType1 ErrorType2
```

Rules:
- No description line — that's in `_index.md`
- `#` note only when there's a real gotcha (destructive op, async, side effects)
- Keep it to 5–8 lines max

---

## skill.py template

```python
import sys
import json
import os
sys.path.insert(0, os.path.dirname(__file__))
from _lib import command, require  # add coerce, poll as needed

def main():
    require(N, "python skill_name.py <arg1> [arg2]")
    params = { ... }
    print(json.dumps(command("tool_name", params), indent=2))

if __name__ == "__main__":
    main()
```

- stdlib only — no httpx, no requests (not available in system Python)
- `ERROR:` prefix on all errors, `sys.exit(1)` on failure
- `print(json.dumps(..., indent=2))` inline — don't wrap in a lib helper
- `if __name__ == "__main__": main()` always at bottom

---

## Workflow (follow exactly)

1. **Discover the HTTP bridge** — check if Rider MCP has one, find the port and endpoint
2. **Load tool schemas** — use `ToolSearch` with `select:mcp__rider__<tool>,...`
3. **Probe live** — `curl` each endpoint before writing a single file; confirm response shape
4. **Mark destructive skills** — `# DESTRUCTIVE` note in skill.md, verify with user before testing
5. **Test every skill end-to-end** — run the actual `.py`, confirm output, clean up test state
6. **Fix errors before moving on** — never skip a failing test
7. **Commit after each logical batch** — not at the very end

---

## Lessons learned building unity-mcp-skills

- **Tool names in HTTP differ from MCP names** — `create_script` MCP tool maps to
  `manage_script` as the HTTP command type. Always probe `{"type": "<name>", "params": {}}`
  to verify the command type name actually works before building the skill.
- **Error fields vary by tool** — some use `message`, some use `error`, some use `code`.
  The `_command_inner` helper checks all three.
- **Async responses** — `_mcp_status: "pending"` is at `result` level, not inside `data`.
  The `poll()` helper handles this correctly.
- **Domain reload** — creating or deleting scripts triggers Unity recompile; MCP disconnects
  for ~5s. Skills that cause this should note it.
- **Destructive skills** — `delete_*`, `remove_package`, `switch_platform` get a
  `# DESTRUCTIVE` or `# slow` note. Test them last, with a recoverable test asset.
- **Primitive GameObjects** created via the API only have Transform — no MeshRenderer.
  `set_renderer_color` needs an object that already has a renderer component.
- **`search_assets` pattern/filter** — filter_type and search_pattern params have no
  observable effect; the tool lists everything under the given path.
- **`read_console` types** must be a list `["error"]`, not a string.
- **`manage_script`** is the correct HTTP command type for both create and delete script
  operations (not `create_script` or `delete_script`).

---

## Rider MCP tools (from deferred tool list)

These are the `mcp__rider__*` tools available — load their schemas with ToolSearch before implementing:

```
mcp__rider__build_project
mcp__rider__create_new_file
mcp__rider__execute_run_configuration
mcp__rider__execute_sql_query
mcp__rider__execute_terminal_command
mcp__rider__find_files_by_glob
mcp__rider__find_files_by_name_keyword
mcp__rider__get_all_open_file_paths
mcp__rider__get_file_problems
mcp__rider__get_file_text_by_path
mcp__rider__get_project_dependencies
mcp__rider__get_project_modules
mcp__rider__get_repositories
mcp__rider__get_run_configurations
mcp__rider__get_symbol_info
mcp__rider__list_database_connections
mcp__rider__list_database_schemas
mcp__rider__list_recent_sql_queries
mcp__rider__list_schema_object_kinds
mcp__rider__list_schema_objects
mcp__rider__open_file_in_editor
mcp__rider__preview_table_data
mcp__rider__read_file
mcp__rider__reformat_file
mcp__rider__rename_refactoring
mcp__rider__replace_text_in_file
mcp__rider__search_file
mcp__rider__search_in_files_by_regex
mcp__rider__search_in_files_by_text
mcp__rider__search_regex
mcp__rider__search_symbol
mcp__rider__search_text
mcp__rider__test_database_connection
```

## Rider Debugger tools

```
mcp__rider-debugger__evaluate_expression
mcp__rider-debugger__execute_run_configuration
mcp__rider-debugger__get_debug_session_status
mcp__rider-debugger__get_source_context
mcp__rider-debugger__get_stack_trace
mcp__rider-debugger__get_variables
mcp__rider-debugger__list_breakpoints
mcp__rider-debugger__list_debug_sessions
mcp__rider-debugger__list_run_configurations
mcp__rider-debugger__list_threads
mcp__rider-debugger__pause_execution
mcp__rider-debugger__remove_breakpoint
mcp__rider-debugger__resume_execution
mcp__rider-debugger__run_to_line
mcp__rider-debugger__select_stack_frame
mcp__rider-debugger__set_breakpoint
mcp__rider-debugger__set_variable
mcp__rider-debugger__start_debug_session
mcp__rider-debugger__step_into
mcp__rider-debugger__step_out
mcp__rider-debugger__step_over
mcp__rider-debugger__stop_debug_session
mcp__rider-debugger__wait_for_pause
```

---

## Existing unity-mcp-skills for reference

Location: `/Users/Chill/Documents/unity-mcp-skills/`

All 36 skills: add_gameobject move_gameobject find_gameobject delete_gameobject
duplicate_gameobject get_hierarchy save_scene load_scene add_component remove_component
set_component_property create_script delete_script read_console refresh_assets screenshot
editor_control profiler_start profiler_stop get_frame_timing get_counters
list_packages search_packages install_package remove_package
set_renderer_color search_assets create_folder move_asset delete_asset
build_player build_status build_settings switch_platform
create_scriptable_object modify_scriptable_object
