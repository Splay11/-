def count_runs(xs):
    # 工位留在原位，不相邻的同值不会贴合，答案就是极大等值段的段数
    if not xs:
        return 0
    runs = 1
    for i in range(1, len(xs)):
        # 和左边零件个数不同，就必须新开一次勾取
        if xs[i] != xs[i - 1]:
            runs += 1
    return runs


def solve_cases(cases):
    # 每组询问单独数段，互不影响
    return [count_runs(xs) for xs in cases]


def main():
    # 首行是询问条数，随后每行先是工位数，再跟各工位零件个数
    q = int(input())
    cases = []
    for _ in range(q):
        row = list(map(int, input().split()))
        m = row[0]
        cases.append(row[1:1 + m])
    ans = solve_cases(cases)
    # 全部答案写在同一行，空格分隔
    print(" ".join(str(x) for x in ans))


if __name__ == "__main__":
    main()
