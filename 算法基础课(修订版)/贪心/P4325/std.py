import sys
import math

def solve_one(a):
    g = 0
    ln = 0
    ans = 0
    for x in a:
        g = math.gcd(g, x)
        ln += 1
        if g <= ln:          # 能切就切
            ans += 1
            g = 0
            ln = 0
    return -1 if ans == 0 else ans

def main():
    data = sys.stdin.read().strip().split()
    it = iter(data)
    T = int(next(it))
    out = []
    for _ in range(T):
        n = int(next(it))
        arr = [int(next(it)) for _ in range(n)]
        out.append(str(solve_one(arr)))
    print("\n".join(out))

if __name__ == "__main__":
    main()
