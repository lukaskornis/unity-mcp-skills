import sys
import json
import os
sys.path.insert(0, os.path.dirname(__file__))
from _lib import command

def main():
    params = {"action": "get_hierarchy"}
    if len(sys.argv) > 1: params["max_depth"] = int(sys.argv[1])
    if len(sys.argv) > 2: params["max_nodes"] = int(sys.argv[2])
    if len(sys.argv) > 3: params["cursor"] = sys.argv[3]
    print(json.dumps(command("manage_scene", params), indent=2))

if __name__ == "__main__":
    main()
