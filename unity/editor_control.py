import sys
import json
import os
sys.path.insert(0, os.path.dirname(__file__))
from _lib import command, require

VALID = {"play", "pause", "stop", "undo", "redo"}

def main():
    require(2, "python editor_control.py <action>  # play|pause|stop|undo|redo")
    action = sys.argv[1]
    if action not in VALID:
        print(f"ERROR: action must be one of {sorted(VALID)}")
        sys.exit(1)
    result = command("manage_editor", {"action": action})
    # editor actions return no data, just message in inner — print success
    print(json.dumps({"action": action, "ok": True}, indent=2))

if __name__ == "__main__":
    main()
