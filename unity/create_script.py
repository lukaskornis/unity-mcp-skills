import sys
import json
import os
sys.path.insert(0, os.path.dirname(__file__))
from _lib import command, require

def main():
    require(3, "python create_script.py <path> <contents>")
    path = sys.argv[1]
    name = os.path.splitext(os.path.basename(path))[0]
    contents = sys.argv[2]
    print(json.dumps(command("manage_script", {"action": "create", "name": name, "path": path, "contents": contents}), indent=2))

if __name__ == "__main__":
    main()
