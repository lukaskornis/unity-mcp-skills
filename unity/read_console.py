import sys
import json
import os
sys.path.insert(0, os.path.dirname(__file__))
from _lib import command

def main():
    params = {"format": "plain"}
    if len(sys.argv) > 1:
        params["types"] = [t.strip() for t in sys.argv[1].split(",")]
    if len(sys.argv) > 2:
        params["page_size"] = int(sys.argv[2])
    print(json.dumps(command("read_console", params), indent=2))

if __name__ == "__main__":
    main()
