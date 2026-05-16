# async — returns job_id immediately; poll with build_status
python build_player.py <target> <output_path> [development]
target:str       android|ios|windows64|osx|linux64|webgl
output_path:str  e.g. Builds/Android/game.apk
development:bool true for dev build with profiler (default false)
→ job_id  # use build_status to poll result
