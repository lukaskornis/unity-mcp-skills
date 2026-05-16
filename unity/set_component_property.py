import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
from _lib import command, require, coerce

def main():
    require(5, "python set_component_property.py <target> <component_type> <property> <value>")
    params = {
        "action": "set_property",
        "target": sys.argv[1],
        "component_type": sys.argv[2],
        "property": sys.argv[3],
        "value": coerce(sys.argv[4]),
    }
    command("manage_components", params)
    print("ok")

if __name__ == "__main__":
    main()
