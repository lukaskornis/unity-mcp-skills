import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
from _lib import poll

def main():
    result = poll("manage_packages", {"action": "list_packages"})
    pkgs = result.get("packages", [])
    for p in pkgs:
        ver = p.get("version") or ""
        src = p.get("source") or ""
        print(f"{p['name']} {ver} {src}".strip())

if __name__ == "__main__":
    main()
