import sys
import json
import os
sys.path.insert(0, os.path.dirname(__file__))
from _lib import command, require

def main():
    require(5, "python set_renderer_color.py <target> <r> <g> <b> [a]")
    params = {
        "action": "set_renderer_color",
        "target": sys.argv[1],
        "color": {
            "r": float(sys.argv[2]),
            "g": float(sys.argv[3]),
            "b": float(sys.argv[4]),
            "a": float(sys.argv[5]) if len(sys.argv) > 5 else 1.0,
        },
    }
    # returns no data field — print success message
    print(json.dumps({"ok": True}, indent=2))
    command("manage_material", params)

if __name__ == "__main__":
    main()
