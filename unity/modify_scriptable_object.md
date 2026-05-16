# property paths are serialized field names — use exact C# field names
python modify_scriptable_object.py <path> <field=value> [field=value ...]
path:str    asset path e.g. Assets/Sleds/Data/BasicSleds.asset
field=value  e.g. baseMoveSpeed=8.0 jumpHeight=3.0 rotationSpeed=90
# value types: float int bool string  auto-detected from string
→ results[{propertyPath ok message}]
! PropertyNotFound TypeMismatch
