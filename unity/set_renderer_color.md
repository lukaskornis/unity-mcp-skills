# target must have a Renderer component (MeshRenderer, SpriteRenderer etc.)
python set_renderer_color.py <target> <r> <g> <b> [a]
target:str   GameObject name or instanceID
r g b a:float  0.0–1.0  (a defaults to 1.0)
→ message
! NoRenderer GameObjectNotFound
