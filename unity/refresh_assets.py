import sys
import json
import os
sys.path.insert(0, os.path.dirname(__file__))
from _lib import command

def main():
    params = {"mode": "if_dirty", "scope": sys.argv[1] if len(sys.argv) > 1 else "all",
              "compile": sys.argv[2] if len(sys.argv) > 2 else "none"}
    print(json.dumps(command("refresh_unity", params), indent=2))

if __name__ == "__main__":
    main()
