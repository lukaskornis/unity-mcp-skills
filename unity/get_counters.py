import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
from _lib import command

def main():
    category = sys.argv[1] if len(sys.argv) > 1 else "Memory"
    d = command("manage_profiler", {"action": "get_counters", "category": category}) or {}
    counters = d.get("counters") or d
    if isinstance(counters, dict):
        for k, v in counters.items():
            print(f"{k}={v}")
    else:
        print(counters)

if __name__ == "__main__":
    main()
