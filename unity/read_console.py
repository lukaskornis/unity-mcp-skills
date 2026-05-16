import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
from _lib import command

TYPE = {"error": "E", "warning": "W", "log": "L"}

def main():
    params = {"format": "plain"}
    if len(sys.argv) > 1:
        params["types"] = [t.strip() for t in sys.argv[1].split(",")]
    if len(sys.argv) > 2:
        params["page_size"] = int(sys.argv[2])
    d = command("read_console", params)
    total = d.get("total", 0)
    truncated = d.get("truncated", False)
    print(f"total={total}" + (" +more" if truncated else ""))
    for item in d.get("items", []):
        t = TYPE.get(item.get("type", ""), "?")
        msg = item.get("message", "").strip().replace("\n", " | ", 1)
        print(f"{t} {msg}")

if __name__ == "__main__":
    main()
