# MCP Skill System — Handoff for New Chat

## What to build

Two more repos following the same pattern as `unity-mcp-skills`:

- `/Users/Chill/Documents/rider-mcp-skills` — wraps `mcp__rider__*` tools
- `/Users/Chill/Documents/rider-debugger-mcp-skills` — wraps `mcp__rider-debugger__*` tools

Reference implementation: `/Users/Chill/Documents/unity-mcp-skills` (also at https://github.com/lukaskornis/unity-mcp-skills)

---

## Development approach (replicate this process)

The system was built iteratively — never speculatively. Each decision came from real evidence.

**1. Discover before building**
Before writing a single file, probe how the MCP server is actually reachable. Check
`claude_desktop_config.json` for transport mode, scan `lsof` for listening ports, curl
candidate endpoints. Only then decide on the calling strategy. For Unity this revealed
an HTTP sidecar at `:8080/api/command` that wasn't obviously documented.

**2. One skill first, then reflect**
Build and test exactly one skill end-to-end before anything else. Get it working, commit it,
then step back and ask: is the folder structure right? Is the file format right? Is the
invocation clean? Fix structural decisions before they're repeated across 30 files.
For Unity: `add_gameobject` was built first. This revealed the stdlib-only constraint
(no httpx in system Python), confirmed the response shape, and validated the whole pipeline.

**3. Add a second skill, then look for shared code**
Add one more skill, then compare the two side by side. Extract only what is genuinely
repeated and identical — not what might be repeated. For Unity: two skills showed the
4-line import header, arg validation, and HTTP logic were all duplicated → extracted
`_lib.py` with `command()` and `require()`.

**4. Batch the rest, but probe each one first**
Once the pattern is established, implement remaining skills in groups. But still probe
every tool live with curl before writing its skill — response shapes vary, some tools
are async, some have surprising param names. Never assume from the schema alone.

**5. Refine format through use**
The skill.md format evolved through the process:
- Started verbose (full description, labelled sections)
- Trimmed description (index already has it)
- Replaced `Returns:` / `Errors:` labels with `→` / `!` symbols
- Added `#` for notes
- Moved notation definition to `_index.md` so it's paid once

**6. Structural decisions made during the process**
- Folders → flat files: each skill folder held exactly 2 files with generic names
  (`skill.md`, `skill.py`) — the folder was doing the naming job. Flatten so the skill
  name is in the filename: `add_gameobject.py`, not `add_gameobject/skill.py`.
- `_` prefix on shared files so `_index.md` and `_lib.py` sort above skill files.

**7. Destructive skills last, carefully**
Test all read-only and safe skills first. Test destructive ones (delete, remove, switch
platform) last, using throwaway assets, confirming the test can be undone before running.

**8. Commit after each logical batch, not at the end**
Each commit is a coherent unit: one new skill, one refactor, one structural decision.
Makes the history readable and makes it easy to revert a bad decision.

---

## How the Unity HTTP bridge works (for reference)

Unity MCP is stdio-based but also runs an HTTP sidecar at `http://localhost:8080`.

All tool calls:
```
POST http://localhost:8080/api/command
{"type": "<tool_name>", "params": {...}}
```

Response:
```json
{
  "status": "success",
  "result": {
    "success": true,
    "message": "...",
    "_mcp_status": "pending",
    "data": { ... }
  }
}
```

**For Rider:** also stdio-based (Java process, `IJ_MCP_SERVER_PORT=64342`). First task is
to discover if it exposes an HTTP bridge. Check `~/.claude/claude_desktop_config.json` for
config, probe `lsof -iTCP -sTCP:LISTEN` for listening ports, then curl candidate ports.
If no HTTP bridge exists, investigate alternatives before writing any skills.

---

## Repo structure

```
<name>-mcp-skills/
  README.md
  CLAUDE.md
  config.json        — {"<domain>_mcp_url": "http://localhost:<port>"}
  .gitignore         — .DS_Store  __pycache__/  *.pyc
  <domain>/
    _index.md        — notation header + one-liner per skill
    _lib.py          — shared helpers
    <skill>.md       — terse spec
    <skill>.py       — CLI wrapper
```

`_` prefix on shared files so they sort to the top.

---

## _lib.py — copy and adapt (replace `<domain>` key in config lookup)

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
        print(f"ERROR: MCP server not reachable — {e.reason}")
        sys.exit(1)
    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(1)


def command(tool, params):
    return _command_inner(tool, params).get("data")


def poll(tool, params, interval=2, max_tries=20):
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

---

## skill.md format

```
# note only for real gotchas (destructive, async, side effects)
python <skill>.py <req_arg> [opt_arg]
arg:type  description or enum values
→ return_field1 return_field2
! ErrorType1 ErrorType2
```

- No description line — that lives in `_index.md`
- 5–8 lines max

## _index.md header (verbatim)

```
# <arg>=required  [arg]=optional  type after colon  →=returns  !=errors  #=note
```

## skill.py template

```python
import sys
import json
import os
sys.path.insert(0, os.path.dirname(__file__))
from _lib import command, require  # add coerce, poll as needed

def main():
    require(N, "python skill.py <arg1> [arg2]")
    print(json.dumps(command("tool_name", {...}), indent=2))

if __name__ == "__main__":
    main()
```

- stdlib only — no httpx, no requests
- `ERROR:` prefix + `sys.exit(1)` on all failures
- `print(json.dumps(..., indent=2))` inline, never wrapped in a helper

---

## Workflow

1. Check `~/.claude/claude_desktop_config.json` — find Rider MCP config
2. Probe `lsof -iTCP -sTCP:LISTEN` — find candidate ports
3. Curl candidate ports to discover the HTTP bridge and endpoint format
4. Load tool schemas with `ToolSearch select:mcp__rider__<tool>,...`
5. Probe every tool live with curl before writing any file
6. Write skill.md + skill.py, test end-to-end, fix before moving on
7. Commit after each logical batch
8. Push to GitHub as public repo under `lukaskornis`

---

## Lessons learned

- **Probe tool name mapping** — MCP tool name ≠ HTTP command type. Always curl `{"type":"<name>","params":{}}` to verify it works before building the skill.
- **Error fields vary** — check `result.message`, `result.error`, `result.code` in that order.
- **`_mcp_status: "pending"`** lives at `result` level, not inside `data`. `poll()` handles this.
- **Domain reload** — creating/deleting scripts disconnects MCP for ~5s.
- **Async commands** return `job_id`; use `poll()`. Long ops (builds) should return `job_id` immediately rather than blocking.
- **Destructive skills** get `# DESTRUCTIVE` in skill.md. Test last, with a recoverable asset.
- **`read_console` types** must be a list `["error"]`, not a string `"error"`.
- **`manage_script`** is the correct HTTP type for both create and delete (not `create_script`/`delete_script`).

---

## Rider MCP tools to wrap

```
mcp__rider__build_project
mcp__rider__create_new_file
mcp__rider__execute_run_configuration
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
mcp__rider__open_file_in_editor
mcp__rider__read_file
mcp__rider__reformat_file
mcp__rider__rename_refactoring
mcp__rider__replace_text_in_file
mcp__rider__search_file
mcp__rider__search_in_files_by_regex
mcp__rider__search_in_files_by_text
mcp__rider__search_symbol
mcp__rider__search_text
```

Probably skip (DB-specific, unlikely needed): `cancel_sql_query` `execute_sql_query`
`list_database_connections` `list_database_schemas` `list_recent_sql_queries`
`list_schema_object_kinds` `list_schema_objects` `preview_table_data`
`test_database_connection`

## Rider Debugger tools to wrap

```
mcp__rider-debugger__evaluate_expression
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
mcp__rider-debugger__execute_run_configuration
```
