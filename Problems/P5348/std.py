from collections import Counter

WAN = "123456789"
TONG = "abcdefghi"
TIAO = "ABCDEFGHI"
ALL = WAN + TONG + TIAO
SUIT = {ch: i for i, group in enumerate((WAN, TONG, TIAO)) for ch in group}


def next_in_suit(ch, step):
    # 同一门里往后数 step 张，跨出门就没有顺子
    for group in (WAN, TONG, TIAO):
        pos = group.find(ch)
        if pos >= 0:
            nxt = pos + step
            if 0 <= nxt < 9:
                return group[nxt]
            return None
    return None


def suit_count(cnt):
    # 统计手里实际出现了几门花色
    used = [0, 0, 0]
    for ch, c in cnt.items():
        if c > 0:
            used[SUIT[ch]] = 1
    return sum(used)


def try_melds(cnt):
    # 把剩下的牌拆成若干顺子或刻子，必须拆空
    first = None
    for t in ALL:
        if cnt[t] > 0:
            first = t
            break
    if first is None:
        return True
    # 先试刻子：三张相同
    if cnt[first] >= 3:
        cnt[first] -= 3
        if try_melds(cnt):
            cnt[first] += 3
            return True
        cnt[first] += 3
    # 再试顺子：同一门连续三张
    a = next_in_suit(first, 1)
    b = next_in_suit(first, 2)
    if a is not None and b is not None and cnt[a] > 0 and cnt[b] > 0:
        cnt[first] -= 1
        cnt[a] -= 1
        cnt[b] -= 1
        if try_melds(cnt):
            cnt[first] += 1
            cnt[a] += 1
            cnt[b] += 1
            return True
        cnt[first] += 1
        cnt[a] += 1
        cnt[b] += 1
    return False


def can_hu(cnt):
    # 14 张、缺一门，并且能拆成 k 组面子加一对将
    if sum(cnt.values()) != 14:
        return False
    if not (1 <= suit_count(cnt) <= 2):
        return False
    for t in ALL:
        if cnt[t] >= 2:
            cnt[t] -= 2
            ok = try_melds(cnt)
            cnt[t] += 2
            if ok:
                return True
    return False


def winning_tiles(hand):
    # 枚举所有还能再摸的牌面，收集能胡的那些
    cnt = Counter(hand)
    ans = []
    for t in ALL:
        if cnt[t] >= 4:
            continue
        cnt[t] += 1
        if can_hu(cnt):
            ans.append(t)
        cnt[t] -= 1
    if not ans:
        return "-1"
    return "".join(sorted(ans))


def main():
    s = input().strip()
    print(winning_tiles(s))


if __name__ == "__main__":
    main()
