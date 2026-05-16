import sys
import json
import os
sys.path.insert(0, os.path.dirname(__file__))
from _lib import command

def main():
    category = sys.argv[1] if len(sys.argv) > 1 else "Memory"
    print(json.dumps(command("manage_profiler", {"action": "get_counters", "category": category}), indent=2))

if __name__ == "__main__":
    main()
