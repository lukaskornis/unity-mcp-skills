import sys
import json
import os
sys.path.insert(0, os.path.dirname(__file__))
from _lib import command

def main():
    print(json.dumps(command("manage_profiler", {"action": "get_frame_timing"}), indent=2))

if __name__ == "__main__":
    main()
