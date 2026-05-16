import sys
import json
import os
sys.path.insert(0, os.path.dirname(__file__))
from _lib import poll

def main():
    result = poll("manage_packages", {"action": "list_packages"})
    pkgs = result.get("packages", [])
    print(json.dumps([{"name": p["name"], "version": p.get("version"), "source": p.get("source")} for p in pkgs], indent=2))

if __name__ == "__main__":
    main()
