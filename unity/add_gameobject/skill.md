Create a GameObject or primitive in the current Unity scene.

Usage: python skill.py <name> <x> <y> <z> [primitive_type] [prefab_path] [parent]

Args:
  name           (req) str   - GameObject name
  x y z          (req) float - world position
  primitive_type (opt) str   - Cube, Sphere, Capsule, Cylinder, Plane, Quad
  prefab_path    (opt) str   - prefab asset path e.g. Assets/Prefabs/Enemy.prefab
  parent         (opt) str   - parent GameObject name

Returns: {name, instanceID, transform, componentNames}
Errors: NoSceneLoaded, PrefabNotFound, InvalidParent
