# returns instanceIDs only, not full object data
python skill.py <search_term> [search_method]
search_term:str
search_method:str  by_name|by_tag|by_layer|by_component|by_path|by_id  (default by_name)
→ instanceIDs totalCount hasMore nextCursor
! NotFound
