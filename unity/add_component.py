import sys
import json
import os
sys.path.insert(0, os.path.dirname(__file__))
from _lib import command, require

def main():
    require(3, "python add_component.py <target> <component_type>")
    print(json.dumps(command("manage_components", {"action": "add", "target": sys.argv[1], "component_type": sys.argv[2]}), indent=2))

if __name__ == "__main__":
    main()
