import sys
import json
import os
import urllib.request
import urllib.error


def load_config():
    config_path = os.path.join(os.path.dirname(__file__), "..", "..", "config.json")
    with open(os.path.normpath(config_path)) as f:
        return json.load(f)


def post(url, payload):
    data = json.dumps(payload).encode()
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=10) as resp:
        return json.loads(resp.read())


def main():
    if len(sys.argv) < 5:
        print("ERROR: Usage: python skill.py <name> <x> <y> <z> [primitive_type] [prefab_path] [parent]")
        sys.exit(1)

    config = load_config()
    name = sys.argv[1]
    x, y, z = float(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4])
    primitive_type = sys.argv[5] if len(sys.argv) > 5 else None
    prefab_path = sys.argv[6] if len(sys.argv) > 6 else None
    parent = sys.argv[7] if len(sys.argv) > 7 else None

    params = {"action": "create", "name": name, "position": [x, y, z]}
    if primitive_type:
        params["primitive_type"] = primitive_type
    if prefab_path:
        params["prefab_path"] = prefab_path
    if parent:
        params["parent"] = parent

    try:
        result = post(f"{config['unity_mcp_url']}/api/command", {"type": "manage_gameobject", "params": params})
        if result.get("status") != "success" or not result.get("result", {}).get("success"):
            error = result.get("result", {}).get("message") or result.get("error", "Unknown error")
            print(f"ERROR: {error}")
            sys.exit(1)
        print(json.dumps(result["result"]["data"], indent=2))
    except urllib.error.URLError as e:
        print(f"ERROR: Unity MCP server not reachable at {config['unity_mcp_url']} — {e.reason}")
        sys.exit(1)
    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
