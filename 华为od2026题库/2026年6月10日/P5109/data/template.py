import ast
import sys


def parse_two_quoted_strings(line: str):
    line = line.strip("\r\n")
    if not line:
        raise SystemExit(0)
    resA, resB = ast.literal_eval("[" + line + "]")
    return resA, resB


line = sys.stdin.read()
resA, resB = parse_two_quoted_strings(line)
ans = Solution().minDistinctAfterSwap(resA, resB)
print(ans)
