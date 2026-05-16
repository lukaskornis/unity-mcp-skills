# <arg>=required  [arg]=optional  type after colon  →=returns  !=errors  #=note

- add_gameobject: create a GameObject or primitive in the scene
- move_gameobject: set position, rotation, scale of an existing GameObject
- find_gameobject: search GameObjects by name, tag, layer, component, path, or id
- delete_gameobject: delete a GameObject by name
- save_scene: save the active scene to disk
- load_scene: load a scene by asset path
- add_component: add a component to a GameObject
- remove_component: remove a component from a GameObject
- set_component_property: set a single property on a component
- duplicate_gameobject: duplicate a GameObject with optional new position
- get_hierarchy: get the scene object tree (paginated)
- read_console: read Unity console messages, filtered by type
- refresh_assets: refresh the asset database and optionally trigger recompile
- screenshot: capture the game view to Assets/Screenshots/
- create_script: create a new C# script file (triggers domain reload)
- delete_script: move a C# script to trash (DESTRUCTIVE, triggers domain reload)
