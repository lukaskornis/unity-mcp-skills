import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
from _lib import command, require

def main():
    require(2, "python delete_script.py <path>")
    path = sys.argv[1]
    name = os.path.splitext(os.path.basename(path))[0]
    command("manage_script", {"action": "delete", "name": name, "path": path})
    print(f"deleted {path}")

if __name__ == "__main__":
    main()
