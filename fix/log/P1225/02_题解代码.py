MOD = 10**9 + 7
n = int(input())
a = list(map(int, input().split()))
ans = 0
for x in a:
    ans = (ans + x * (x + 1) // 2) % MOD
for i in range(n):
    ok = True
    for j in range(i + 2, n, 2):
        mid = (i + j) // 2
        # check a[i+1..j-1] is palindrome as sequence — expand step by step
        k = (j - i) // 2
        for t in range(1, k):
            if a[i + t] != a[j - t]:
                ok = False
                break
        if not ok:
            break
        ans = (ans + min(a[i], a[j])) % MOD
print(ans)
