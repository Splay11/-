n, q = map(int, input().split())
s = list(input().strip())
for _ in range(q):
    l, r = map(int, input().split())
    for i in range(r, l - 1, -1):
        s.insert(i, s[i - 1])
print(''.join(s))
