python get_hierarchy.py [max_depth] [max_nodes] [cursor]
max_depth:int  how deep to recurse (default unlimited)
max_nodes:int  max nodes per page (default 50)
cursor:str     pagination cursor from previous response
→ items[{name instanceID path childCount componentTypes}] total truncated next_cursor
