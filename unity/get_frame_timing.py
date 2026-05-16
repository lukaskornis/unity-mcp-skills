import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
from _lib import command

def main():
    d = command("manage_profiler", {"action": "get_frame_timing"}) or {}
    # normalise common field name variants
    cpu = d.get("cpuFrameTime") or d.get("cpu") or d.get("cpuTime")
    gpu = d.get("gpuFrameTime") or d.get("gpu") or d.get("gpuTime")
    fps = d.get("fps") or d.get("frameRate")
    parts = []
    if cpu is not None: parts.append(f"cpu={cpu}ms")
    if gpu is not None: parts.append(f"gpu={gpu}ms")
    if fps is not None: parts.append(f"fps={fps}")
    # fallback: dump remaining keys not already shown
    shown = {"cpuFrameTime","cpu","cpuTime","gpuFrameTime","gpu","gpuTime","fps","frameRate"}
    for k, v in d.items():
        if k not in shown and v is not None:
            parts.append(f"{k}={v}")
    print(" ".join(parts) if parts else "no data")

if __name__ == "__main__":
    main()
