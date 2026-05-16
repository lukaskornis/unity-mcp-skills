import sys
import json
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from lib import command, require

def main():
    require(5, "python skill.py <target> <x> <y> <z> [rx] [ry] [rz] [sx] [sy] [sz]")

    argc = len(sys.argv)
    if argc not in (5, 8, 11):
        print("ERROR: rx/ry/rz and sx/sy/sz must be full triplets (5, 8, or 11 args total)")
        sys.exit(1)

    params = {
        "action": "modify",
        "target": sys.argv[1],
        "position": [float(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4])],
    }
    if argc >= 8:
        params["rotation"] = [float(sys.argv[5]), float(sys.argv[6]), float(sys.argv[7])]
    if argc == 11:
        params["scale"] = [float(sys.argv[8]), float(sys.argv[9]), float(sys.argv[10])]

    print(json.dumps(command("manage_gameobject", params), indent=2))

if __name__ == "__main__":
    main()
