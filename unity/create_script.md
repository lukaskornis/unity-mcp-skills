# triggers domain reload; Unity MCP will disconnect for ~5s then reconnect
python create_script.py <path> <contents>
path:str      full asset path e.g. Assets/Scripts/MyBehaviour.cs
contents:str  C# source code as a single string
→ uri scheduledRefresh
! PathAlreadyExists CompilationError
