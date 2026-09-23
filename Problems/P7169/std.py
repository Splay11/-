def solve(n):
    """埃氏筛：标记所有小于 n 的合数，剩下的就是质数。
    题目要的是严格小于 n 的质数个数，所以筛到 n-1。
    """
    if n <= 2:
        return 0
    is_prime = [True] * n
    is_prime[0] = False
    is_prime[1] = False
    i = 2
    while i * i < n:
        if is_prime[i]:
            j = i * i
            while j < n:
                is_prime[j] = False
                j += i
        i += 1
    ans = 0
    for i in range(2, n):
        if is_prime[i]:
            ans += 1
    return ans


def main():
    # 一行一个非负整数 n
    n = int(input())
    print(solve(n))


if __name__ == "__main__":
    main()
