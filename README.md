# unity-mcp-skills

Lightweight CLI wrappers around the [MCP for Unity](https://github.com/CoPlay-Dev/mcp-for-unity) server, designed for use with Claude Code.

Instead of loading full MCP tool schemas into context on every task, Claude reads a small `skill.md` file and runs a Python script. The script calls the Unity MCP HTTP server and prints JSON to stdout.

## Why

MCP tool schemas are large. Loading all Unity MCP schemas at once consumes significant context. This system lets Claude:

1. Read `unity/_index.md` — a one-liner list of available skills (~20 tokens per skill)
2. Read `unity/<skill>.md` — a terse 5-line spec only when needed
3. Run `python unity/<skill>.py <args>` — the script handles the HTTP call

## Requirements

- Unity Editor open with [MCP for Unity](https://github.com/CoPlay-Dev/mcp-for-unity) plugin installed
- `mcp-for-unity` server running in HTTP mode at `http://localhost:8080`
- Python 3 (stdlib only — no extra packages needed)

### Enabling HTTP mode

By default the MCP server runs in stdio mode. To also expose the HTTP endpoint used by these scripts, set the environment variable before starting Claude Code:

```bash
UNITY_MCP_HTTP_HOST=localhost UNITY_MCP_HTTP_PORT=8080 claude
```

Or add to your shell profile. The HTTP server runs alongside the stdio MCP connection.

## Usage

```bash
python unity/<skill>.py <args>
```

All scripts print JSON to stdout on success. Errors are prefixed with `ERROR:` and exit with code 1.

## Available Skills

| Skill | Description |
|---|---|
| `add_gameobject` | Create a GameObject or primitive in the scene |
| `move_gameobject` | Set position, rotation, scale of an existing GameObject |
| `find_gameobject` | Search GameObjects by name, tag, layer, component, path, or id |
| `delete_gameobject` | Delete a GameObject by name |
| `duplicate_gameobject` | Duplicate a GameObject with optional new position |
| `get_hierarchy` | Get the scene object tree (paginated) |
| `add_component` | Add a component to a GameObject |
| `remove_component` | Remove a component from a GameObject |
| `set_component_property` | Set a single property on a component |
| `save_scene` | Save the active scene to disk |
| `load_scene` | Load a scene by asset path |
| `screenshot` | Capture the game view to Assets/Screenshots/ |
| `create_script` | Create a new C# script file |
| `delete_script` | Move a C# script to trash |
| `read_console` | Read Unity console messages, filtered by type |
| `refresh_assets` | Refresh the asset database |
| `editor_control` | Play, pause, stop the editor or undo/redo |
| `search_assets` | List assets under a given path |
| `create_folder` | Create an asset folder |
| `move_asset` | Move or rename an asset file |
| `delete_asset` | Delete an asset file |
| `set_renderer_color` | Set RGBA color on a GameObject's Renderer |
| `install_package` | Install a Unity package by name, version, or git URL |
| `remove_package` | Remove an installed package |
| `list_packages` | List all installed packages |
| `search_packages` | Search Unity registry by keyword |
| `build_player` | Start a player build (async, returns job_id) |
| `build_status` | Check build job status or last build result |
| `build_settings` | Read or write build settings |
| `switch_platform` | Switch active build target platform |
| `profiler_start` | Enable Unity profiler |
| `profiler_stop` | Disable Unity profiler |
| `get_frame_timing` | Read CPU/GPU frame times |
| `get_counters` | Read profiler counters by category |
| `create_scriptable_object` | Create a new ScriptableObject asset by type name |
| `modify_scriptable_object` | Patch ScriptableObject fields by serialized property name |

## Skill file format

Each skill has two files:

**`unity/<skill>.md`** — terse spec read by Claude before calling the script:
```
# optional note for non-obvious constraints
python skill_name.py <required_arg> [optional_arg]
arg:type  description or enum values
→ return_field1 return_field2
! ErrorType1 ErrorType2
```

**`unity/<skill>.py`** — CLI wrapper, stdlib only, prints JSON to stdout.

The notation convention is defined once in `unity/_index.md`:
```
# <arg>=required  [arg]=optional  type after colon  →=returns  !=errors  #=note
```

## Shared library

`unity/_lib.py` provides:

- `command(tool, params)` — POST to `/api/command`, return `data`, exit on error
- `poll(tool, params)` — like `command` but handles async `job_id` responses
- `require(n, usage)` — exit with usage message if arg count is insufficient
- `coerce(v)` — convert CLI string to `bool`, `int`, `float`, or `str`

## Adding a new skill

1. Find the tool name and params from the Unity MCP schema
2. Probe it live with `curl` to confirm the response shape
3. Write `unity/<skill>.md` (5–8 lines)
4. Write `unity/<skill>.py` (import `_lib`, call `command` or `poll`, print JSON)
5. Add a one-liner to `unity/_index.md`
6. Test end-to-end

## Config

`config.json` at the repo root:
```json
{
  "unity_mcp_url": "http://localhost:8080"
}
```

Change the port here if your server runs elsewhere.
