import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
from _lib import command

def main():
    params = {"action": "profiler_start"}
    if len(sys.argv) > 1:
        params["log_file"] = sys.argv[1]
    command("manage_profiler", params)
    print("ok")

if __name__ == "__main__":
    main()
