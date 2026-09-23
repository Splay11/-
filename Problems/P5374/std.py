def can_reach(n, s, t, a):
    # 物体总数必须对上；最少搬运次数是离开 1 号货位的件数
    if sum(a) != s:
        return False
    mn = s - a[0]
    if t < mn:
        return False
    extra = t - mn
    # 刚好最少次数，无需浪费
    if extra == 0:
        return True
    # 没有货或只有一个货位时，多出来的步数走不了
    if s == 0 or n == 1:
        return False
    # 两个货位只能来回，浪费步数必须是偶数
    if extra % 2 == 0:
        return True
    # 奇数步浪费需要第三个货位绕一下；已经到位时无法只多走 1 步
    if n < 3 or t == 1:
        return False
    return True


def main():
    n, s, t = map(int, input().split())
    a = list(map(int, input().split()))
    if can_reach(n, s, t, a):
        print("Yes")
    else:
        print("No")


if __name__ == "__main__":
    main()
