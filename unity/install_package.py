import sys
import json
import os
sys.path.insert(0, os.path.dirname(__file__))
from _lib import poll, require

def main():
    require(2, "python install_package.py <package>")
    result = poll("manage_packages", {"action": "add_package", "package": sys.argv[1]})
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
