import sys
import json
import os
sys.path.insert(0, os.path.dirname(__file__))
from _lib import command, require

def main():
    require(4, "python create_scriptable_object.py <type_name> <folder_path> <asset_name>")
    print(json.dumps(command("manage_scriptable_object", {
        "action": "create",
        "type_name": sys.argv[1],
        "folder_path": sys.argv[2],
        "asset_name": sys.argv[3],
    }), indent=2))

if __name__ == "__main__":
    main()
