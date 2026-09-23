# 功能函数：给定 n, l, r，返回最少与最多水果个数；不可满足返回 None
def solve_case(n, l, r):
    # 计算向上取整和向下取整
    k_min = (l + n - 1) // n          # ceil(l / n)
    k_max = r // n                    # floor(r / n)
    if k_min > k_max:
        return None
    return k_min, k_max

def main():
    import sys
    data = list(map(int, sys.stdin.read().strip().split()))
    if not data:
        return
    t = data[0]
    idx = 1
    out_lines = []
    for _ in range(t):
        n, l, r = data[idx], data[idx + 1], data[idx + 2]
        idx += 3
        ans = solve_case(n, l, r)
        if ans is None:
            out_lines.append("-1")
        else:
            out_lines.append(f"{ans[0]} {ans[1]}")
    print("\n".join(out_lines))

if __name__ == "__main__":
    main()
