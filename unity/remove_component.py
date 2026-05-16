import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
from _lib import command, require

def main():
    require(3, "python remove_component.py <target> <component_type>")
    command("manage_components", {"action": "remove", "target": sys.argv[1], "component_type": sys.argv[2]})
    print(f"ok removed {sys.argv[2]}")

if __name__ == "__main__":
    main()
