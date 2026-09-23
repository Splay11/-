import sys

s = sys.stdin.read().strip()

# 兼容输入带双引号的情况，如 "uuuua"
if len(s) >= 2 and s[0] == '"' and s[-1] == '"':
    s = s[1:-1]

ans = Solution().countKeys(s)

sys.stdout.write("[" + ",".join("[" + str(x[0]) + "," + str(x[1]) + "]" for x in ans) + "]")