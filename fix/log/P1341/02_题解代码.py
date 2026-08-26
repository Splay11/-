from functools import cache

s = input().rstrip()

ls = '([{<'
rs = ')]}>'

@cache
def dfs(l, r):
    if l > r: return 0
    ans = float('inf')
    for i in range(l + 1, r + 1):
        sl = s[l]
        sr = s[i]
        cost = 0
        if sl not in ls and sr not in rs:
            cost = 2
        elif sl not in ls or sr not in rs:
            cost = 1
        elif rs[ls.index(sl)] != sr:
            cost = 1
        ans = min(ans, dfs(l + 1, i - 1) + cost + dfs(i + 1, r))
    return ans
print(dfs(0, len(s) - 1))