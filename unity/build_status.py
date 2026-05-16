import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
from _lib import command

SKIP = {"log", "output_log"}  # verbose fields to suppress

def main():
    params = {"action": "status"}
    if len(sys.argv) > 1:
        params["job_id"] = sys.argv[1]
    d = command("manage_build", params) or {}
    parts = [f"{k}={v}" for k, v in d.items() if v is not None and k not in SKIP]
    print(" ".join(parts) if parts else "no data")

if __name__ == "__main__":
    main()
