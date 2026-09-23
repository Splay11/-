import sys

# 从字符串中提取所有整数（忽略非数字字符，如逗号、括号）
def extract_ints(s):
    res = []
    cur = 0
    have = False
    for ch in s:
        if ch.isdigit():
            cur = cur * 10 + int(ch)
            have = True
        elif have:
            res.append(cur)
            cur = 0
            have = False
    if have:
        res.append(cur)
    return res

line = sys.stdin.read().strip()

# 提取全部整数：前 3 个为 n, m, w，其余每 3 个为一条路线
a = extract_ints(line)
n, m, w = a[0], a[1], a[2]
roads = []
i = 3
while i + 2 < len(a):
    roads.append([a[i], a[i + 1], a[i + 2]])
    i += 3

result = Solution().minCost(n, m, w, roads)
print(result)
