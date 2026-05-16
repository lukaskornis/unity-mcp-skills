# requires profiler to be running (profiler_start first)
python get_counters.py [category]
category:str  Render|Memory|Scripts|Physics|Audio|CPU  (default Memory)
→ counters{name: value}  # _valid and _unit suffixed keys included
