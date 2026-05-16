import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
from _lib import command

def main():
    params = {"action": "get_hierarchy"}
    if len(sys.argv) > 1: params["max_depth"] = int(sys.argv[1])
    if len(sys.argv) > 2: params["max_nodes"] = int(sys.argv[2])
    if len(sys.argv) > 3: params["cursor"] = sys.argv[3]
    d = command("manage_scene", params)
    items = d.get("items", [])
    total = d.get("total", len(items))
    cursor = d.get("next_cursor")
    print(f"total={total}" + (f" +more cursor={cursor}" if d.get("truncated") else ""))
    for obj in items:
        comps = " ".join(obj.get("componentTypes", []))
        children = f" children={obj['childCount']}" if obj.get("childCount", 0) > 0 else ""
        print(f"{obj['name']} {obj['instanceID']}{children}  [{comps}]")

if __name__ == "__main__":
    main()
