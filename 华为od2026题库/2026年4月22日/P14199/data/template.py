import sys

line = sys.stdin.read().strip()
if len(line) >= 2 and line[0] == '"' and line[-1] == '"':
    line = line[1:-1]

ans = Solution().timeClassification(line)
print("[" + ",".join(map(str, ans)) + "]")
