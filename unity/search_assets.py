import sys
import json
import os
sys.path.insert(0, os.path.dirname(__file__))
from _lib import command, require

def main():
    require(2, "python search_assets.py <path> [page]")
    params = {
        "action": "search",
        "path": sys.argv[1],
        "page_size": 50,
        "page_number": int(sys.argv[2]) if len(sys.argv) > 2 else 1,
        "generate_preview": False,
    }
    result = command("manage_asset", params)
    print(json.dumps({
        "totalAssets": result["totalAssets"],
        "assets": [{"path": a["path"], "name": a["name"], "assetType": a["assetType"], "guid": a["guid"]} for a in result["assets"]],
    }, indent=2))

if __name__ == "__main__":
    main()
