import sys
import json
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from lib import command

def main():
    print(json.dumps(command("manage_scene", {"action": "save"}), indent=2))

if __name__ == "__main__":
    main()
