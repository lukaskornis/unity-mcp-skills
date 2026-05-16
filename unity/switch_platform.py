import sys
import json
import os
sys.path.insert(0, os.path.dirname(__file__))
from _lib import command, require

def main():
    require(2, "python switch_platform.py <target>  # android|ios|windows64|osx|linux64|webgl")
    print(json.dumps(command("manage_build", {"action": "platform", "target": sys.argv[1]}), indent=2))

if __name__ == "__main__":
    main()
