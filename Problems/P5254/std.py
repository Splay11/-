def count_triples(n):
    ans = 0
    # 枚举非降的 x、y，由异或还原 z
    for x in range(1, n + 1):
        for y in range(x, n + 1):
            z = x ^ y
            if y <= z <= n and x + y > z:
                ans += 1
    return ans


n = int(input())
print(count_triples(n))
