def min_hedge(m: int) -> int:
    # 取 y=floor(m/2) 时对冲值最小：y XOR (m-y)
    return (m // 2) ^ ((m + 1) // 2)


def main() -> None:
    n = int(input())
    for _ in range(n):
        m = int(input())
        print(min_hedge(m))


if __name__ == "__main__":
    main()
