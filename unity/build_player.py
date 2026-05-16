import sys
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
    inner = _command_inner("manage_build", params)
    job_id = ((inner.get("data") or {}).get("job_id") or "?")
    print(f"job_id={job_id}  poll: python build_status.py {job_id}")

if __name__ == "__main__":
    main()
