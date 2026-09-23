import ast
import sys

line = sys.stdin.read()
if not line.strip():
    raise SystemExit(0)
commands = ast.literal_eval(line.strip("\r\n"))
ans = Solution().processPacketCommands(commands)
print("[" + ",".join(str(x) for x in ans) + "]")
