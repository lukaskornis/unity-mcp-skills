import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
from _lib import command

def main():
    params = {"action": "screenshot", "include_image": False}
    if len(sys.argv) > 1:
        params["fileName"] = sys.argv[1]
    d = command("manage_camera", params) or {}
    path = d.get("filePath") or d.get("path") or d.get("fileName") or str(d)
    print(path)

if __name__ == "__main__":
    main()
