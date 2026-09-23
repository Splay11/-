def can_reduce(vals):
    lo = min(vals)
    hi = max(vals)
    seen = [False] * (hi - lo + 1)
    for x in vals:
        seen[x - lo] = True
    for flag in seen:
        if not flag:
            return False
    return True


k = int(input())
for _ in range(k):
    n = int(input())
    vals = list(map(int, input().split()))
    print("YES" if can_reduce(vals) else "NO")
