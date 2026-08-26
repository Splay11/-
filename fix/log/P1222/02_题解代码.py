n, m = map(int, input().split())
g = [input().strip() for _ in range(n)]
ans = 0
need = set("you")
for i in range(n - 1):
    for j in range(m - 1):
        cells = {g[i][j], g[i][j+1], g[i+1][j], g[i+1][j+1]}
        if need <= cells:
            ans += 1
print(ans)
