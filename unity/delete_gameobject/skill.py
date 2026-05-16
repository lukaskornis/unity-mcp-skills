import sys
import json
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from lib import command, require

def main():
    require(2, "python skill.py <name>")

    print(json.dumps(command("manage_gameobject", {"action": "delete", "name": sys.argv[1]}), indent=2))

if __name__ == "__main__":
    main()
