import sys
import json
import os
sys.path.insert(0, os.path.dirname(__file__))
from _lib import command, require

def _coerce(v):
    if v.lower() == "true": return True
    if v.lower() == "false": return False
    try: return int(v)
    except ValueError: pass
    try: return float(v)
    except ValueError: pass
    return v

def main():
    require(5, "python set_component_property.py <target> <component_type> <property> <value>")
    params = {
        "action": "set_property",
        "target": sys.argv[1],
        "component_type": sys.argv[2],
        "property": sys.argv[3],
        "value": _coerce(sys.argv[4]),
    }
    print(json.dumps(command("manage_components", params), indent=2))

if __name__ == "__main__":
    main()
