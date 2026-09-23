import math

ODDS = [3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41]


def impossible(n):
    return n <= 9 or n == 11 or n == 13 or n == 17


def solve(n):
    if impossible(n):
        return None
    if n % 2 == 0:
        if n % 6 != 2:
            return (2, 3, n - 5)
        return (3, 4, n - 7)
    for i in range(len(ODDS)):
        a = ODDS[i]
        for j in range(i, len(ODDS)):
            b = ODDS[j]
            if math.gcd(a, b) != 1:
                continue
            c = n - a - b
            if c >= 2 and math.gcd(a, c) == 1 and math.gcd(b, c) == 1:
                return (a, b, c)
    return None


def main():
    q = int(input())
    for _ in range(q):
        n = int(input())
        ans = solve(n)
        if ans is None:
            print(-1)
        else:
            print(ans[0], ans[1], ans[2])


if __name__ == "__main__":
    main()
