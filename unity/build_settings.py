import sys
import json
import os
sys.path.insert(0, os.path.dirname(__file__))
from _lib import command, require, coerce

def main():
    require(2, "python build_settings.py <property> [value]")
    params = {"action": "settings", "property": sys.argv[1]}
    if len(sys.argv) > 2:
        params["value"] = coerce(sys.argv[2])
    print(json.dumps(command("manage_build", params), indent=2))

if __name__ == "__main__":
    main()
