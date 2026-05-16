import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
from _lib import command, require

def main():
    require(2, "python delete_asset.py <path>")
    command("manage_asset", {"action": "delete", "path": sys.argv[1]})
    print(f"deleted {sys.argv[1]}")

if __name__ == "__main__":
    main()
