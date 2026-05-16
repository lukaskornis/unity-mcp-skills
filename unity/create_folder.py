import sys
import json
import os
sys.path.insert(0, os.path.dirname(__file__))
from _lib import command, require

def main():
    require(2, "python create_folder.py <path>")
    print(json.dumps(command("manage_asset", {"action": "create_folder", "path": sys.argv[1]}), indent=2))

if __name__ == "__main__":
    main()
