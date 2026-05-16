import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
from _lib import command, require

def main():
    require(2, "python search_assets.py <path> [page]")
    params = {
        "action": "search",
        "path": sys.argv[1],
        "pageSize": 50,
        "pageNumber": int(sys.argv[2]) if len(sys.argv) > 2 else 1,
        "generate_preview": False,
    }
    d = command("manage_asset", params)
    total = d["totalAssets"]
    assets = d["assets"]
    shown = len(assets)
    print(f"total={total}" + (f" +more" if shown < total else ""))
    for a in assets:
        print(f"{a['assetType']} {a['path']}")

if __name__ == "__main__":
    main()
