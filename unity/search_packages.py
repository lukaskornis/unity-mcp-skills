import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
from _lib import poll, require

def main():
    require(2, "python search_packages.py <query>")
    d = poll("manage_packages", {"action": "search_packages", "query": sys.argv[1]}) or {}
    pkgs = d.get("packages") or (d if isinstance(d, list) else [])
    for p in pkgs:
        name = p.get("name", "")
        ver = p.get("version") or p.get("latestVersion") or ""
        desc = (p.get("description") or "")[:60]
        print(f"{name} {ver}  {desc}".strip())

if __name__ == "__main__":
    main()
