import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
from _lib import command

def main():
    command("manage_profiler", {"action": "profiler_stop"})
    print("ok")

if __name__ == "__main__":
    main()
