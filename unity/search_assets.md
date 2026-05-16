# lists all assets under path; filter params have no effect in current API version
python search_assets.py <path> [page]
path:str  search root e.g. Assets/Sleds Assets/Textures
page:int  page number (default 1, page_size 50)
→ assets[{path name assetType guid}] totalAssets
