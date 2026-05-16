import sys
import json
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from lib import command, require

def main():
    require(5, "python skill.py <name> <x> <y> <z> [primitive_type] [prefab_path] [parent]")

    params = {
        "action": "create",
        "name": sys.argv[1],
        "position": [float(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4])],
    }
    if len(sys.argv) > 5: params["primitive_type"] = sys.argv[5]
    if len(sys.argv) > 6: params["prefab_path"] = sys.argv[6]
    if len(sys.argv) > 7: params["parent"] = sys.argv[7]

    print(json.dumps(command("manage_gameobject", params), indent=2))

if __name__ == "__main__":
    main()
