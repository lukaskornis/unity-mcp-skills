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


def require(n, usage):
    if len(sys.argv) < n:
        print(f"ERROR: Usage: {usage}")
        sys.exit(1)


def coerce(v):
    """Convert a CLI string arg to the most appropriate Python type."""
    if v.lower() == "true": return True
    if v.lower() == "false": return False
    try: return int(v)
    except ValueError: pass
    try: return float(v)
    except ValueError: pass
    return v


def _command_inner(tool, params):
    config = _load_config()
    url = f"{config['unity_mcp_url']}/api/command"
    try:
        result = _post(url, {"type": tool, "params": params})
        inner = result.get("result", {})
        if result.get("status") != "success" or not inner.get("success"):
            msg = inner.get("message") or inner.get("error") or inner.get("code") or result.get("error", "Unknown error")
            print(f"ERROR: {msg}")
            sys.exit(1)
        return inner
    except urllib.error.URLError as e:
        print(f"ERROR: Unity MCP server not reachable at {config['unity_mcp_url']} — {e.reason}")
        sys.exit(1)
    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(1)


def command(tool, params):
    return _command_inner(tool, params).get("data")


def poll(tool, params, interval=2, max_tries=20):
    """For async commands that return job_id — polls status until complete."""
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
