# -*- coding: utf-8 -*-


def max_fluctuation(n: int, v: list[int]) -> int:
    # 整段作为唯一子段即可达到上界 (max-min)*n
    return (max(v) - min(v)) * n


def main() -> None:
    n = int(input())
    v = list(map(int, input().split()))
    print(max_fluctuation(n, v))


if __name__ == "__main__":
    main()
