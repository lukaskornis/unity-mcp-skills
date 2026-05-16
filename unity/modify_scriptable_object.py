import sys
import json
import os
sys.path.insert(0, os.path.dirname(__file__))
from _lib import command, require, coerce

def main():
    require(3, "python modify_scriptable_object.py <path> <field=value> [field=value ...]")
    patches = []
    for pair in sys.argv[2:]:
        if "=" not in pair:
            print(f"ERROR: expected field=value, got: {pair}")
            sys.exit(1)
        field, _, value = pair.partition("=")
        patches.append({"path": field.strip(), "value": coerce(value.strip())})
    result = command("manage_scriptable_object", {
        "action": "modify",
        "target": {"path": sys.argv[1]},
        "patches": patches,
    })
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
