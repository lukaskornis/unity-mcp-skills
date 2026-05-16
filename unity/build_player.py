import sys
import json
import os
sys.path.insert(0, os.path.dirname(__file__))
from _lib import _command_inner, require

def main():
    require(3, "python build_player.py <target> <output_path> [development]")
    params = {
        "action": "build",
        "target": sys.argv[1],
        "output_path": sys.argv[2],
        "development": sys.argv[3].lower() == "true" if len(sys.argv) > 3 else False,
    }
    # Build can take minutes — return job_id immediately for polling
    inner = _command_inner("manage_build", params)
    data = inner.get("data") or {}
    print(json.dumps({"job_id": data.get("job_id"), "status": "started", "hint": "poll with: python build_status.py " + (data.get("job_id") or "")}, indent=2))

if __name__ == "__main__":
    main()
