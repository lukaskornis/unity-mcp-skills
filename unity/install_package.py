import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
from _lib import poll, require

def main():
    require(2, "python install_package.py <package>")
    d = poll("manage_packages", {"action": "add_package", "package": sys.argv[1]}) or {}
    name = d.get("name") or sys.argv[1]
    ver = d.get("version") or ""
    print(f"ok {name} {ver}".strip())

if __name__ == "__main__":
    main()
