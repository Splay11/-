import sys
sys.setrecursionlimit(10000)
n, L, R = map(int, input().split())
s = input().strip()
g = [[] for _ in range(n)]
for _ in range(n - 1):
    u, v = map(int, input().split())
    u -= 1; v -= 1
    g[u].append(v); g[v].append(u)
ans = 0
def dfs(u, p, val, edges):
    global ans
    if edges >= 1 and L <= val <= R:
        ans += 1
    if val > R and val > 0:
        return
    for v in g[u]:
        if v == p: continue
        nval = val * 2 + (1 if s[v] == '1' else 0)
        dfs(v, u, nval, edges + 1)
for i in range(n):
    dfs(i, -1, 1 if s[i] == '1' else 0, 0)
print(ans)
