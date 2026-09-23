# 二分消费轮次：每轮全体减 q，被点中的再多减 p-q


def enough(times, heat, center, ambient):
    """times 轮是否够把所有积压清到不超过 0。"""
    extra = center - ambient
    need = 0
    # 先按顺带消费 times 轮，剩下的必须靠主消费补
    cooled = ambient * times
    for w in heat:
        rest = w - cooled
        if rest > 0:
            # 向上取整：还要做主消费多少轮
            need += (rest + extra - 1) // extra
            if need > times:
                return False
    return True


def min_starts(heat, center, ambient):
    """最少轮次。下界按全点在积压最大的主题上，上界按只靠顺带消费。"""
    lo = 0
    hi = 0
    for w in heat:
        # 就算每轮都点它，也至少要 ceil(w/p) 轮
        need_center = (w + center - 1) // center
        if need_center > lo:
            lo = need_center
        # 从不点它、只吃顺带消费，ceil(w/q) 轮一定够
        need_amb = (w + ambient - 1) // ambient
        if need_amb > hi:
            hi = need_amb
    while lo < hi:
        mid = (lo + hi) // 2
        if enough(mid, heat, center, ambient):
            hi = mid
        else:
            lo = mid + 1
    return lo


def main():
    # 四级协议：第一行主题数，第二行 p q，第三行全部积压
    m = int(input())
    p, q = map(int, input().split())
    w = list(map(int, input().split()))
    print(min_starts(w, p, q))


if __name__ == "__main__":
    main()
