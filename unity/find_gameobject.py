import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
from _lib import command, require

def main():
    require(2, "python skill.py <search_term> [search_method]")
    params = {
        "search_term": sys.argv[1],
        "search_method": sys.argv[2] if len(sys.argv) > 2 else "by_name",
    }
    d = command("find_gameobjects", params)
    ids = d.get("instanceIDs", [])
    total = d.get("totalCount", len(ids))
    has_more = d.get("hasMore", False)
    if not ids:
        print("none")
        return
    print(f"total={total}" + (" +more" if has_more else ""))
    print(" ".join(str(i) for i in ids))

if __name__ == "__main__":
    main()
