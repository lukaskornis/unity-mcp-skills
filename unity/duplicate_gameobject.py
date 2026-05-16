import sys
import json
import os
sys.path.insert(0, os.path.dirname(__file__))
from _lib import command, require

def main():
    require(2, "python duplicate_gameobject.py <target> [x] [y] [z]")
    params = {"action": "duplicate", "target": sys.argv[1]}
    if len(sys.argv) == 5:
        params["position"] = [float(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4])]
    print(json.dumps(command("manage_gameobject", params), indent=2))

if __name__ == "__main__":
    main()
