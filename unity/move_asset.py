import sys
import json
import os
sys.path.insert(0, os.path.dirname(__file__))
from _lib import command, require

def main():
    require(3, "python move_asset.py <path> <destination>")
    print(json.dumps(command("manage_asset", {"action": "move", "path": sys.argv[1], "destination": sys.argv[2]}), indent=2))

if __name__ == "__main__":
    main()
