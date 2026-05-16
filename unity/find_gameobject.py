import sys
import json
import os
sys.path.insert(0, os.path.dirname(__file__))
from _lib import command, require

def main():
    require(2, "python skill.py <search_term> [search_method]")

    params = {
        "search_term": sys.argv[1],
        "search_method": sys.argv[2] if len(sys.argv) > 2 else "by_name",
    }

    print(json.dumps(command("find_gameobjects", params), indent=2))

if __name__ == "__main__":
    main()
