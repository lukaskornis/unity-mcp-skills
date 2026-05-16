# DESTRUCTIVE — async — checks dependents; use force=true to override
python remove_package.py <package> [force]
package:str  package name e.g. com.unity.cinemachine
force:bool   true to remove even if other packages depend on it
→ name
! PackageNotFound HasDependents
