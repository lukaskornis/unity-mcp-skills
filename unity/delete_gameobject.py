import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
from _lib import command, require

def main():
    require(2, "python skill.py <name>")
    d = command("manage_gameobject", {"action": "delete", "name": sys.argv[1]})
    names = " ".join(item["name"] for item in d) if isinstance(d, list) else sys.argv[1]
    print(f"deleted {names}")

if __name__ == "__main__":
    main()
