import sys
import json
import os
sys.path.insert(0, os.path.dirname(__file__))
from _lib import poll, require

def main():
    require(2, "python remove_package.py <package> [force]")
    params = {"action": "remove_package", "package": sys.argv[1]}
    if len(sys.argv) > 2 and sys.argv[2].lower() == "true":
        params["force"] = True
    result = poll("manage_packages", params)
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
