import sys
import ast
import json

def main():
    data = sys.stdin.read().strip()
    command = ast.literal_eval(data) if data else []
    ans = Solution().execute_command(command)
    print(json.dumps(ans, ensure_ascii=False, separators=(',', ':')), end="")

main()
