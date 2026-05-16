import sys
import json
import os
sys.path.insert(0, os.path.dirname(__file__))
from _lib import command

def main():
    params = {"action": "screenshot", "include_image": False}
    if len(sys.argv) > 1:
        params["fileName"] = sys.argv[1]
    print(json.dumps(command("manage_camera", params), indent=2))

if __name__ == "__main__":
    main()
