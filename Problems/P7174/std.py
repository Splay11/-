def solve(prefixes, cards):
    """把所有前缀放进哈希表。
    每个卡号从长到短枚举可能的前缀（最长 20），第一次命中就是最长匹配。
    全部长度都没有命中则是 UNKNOWN。
    """
    mp = {}
    for prefix, bank in prefixes:
        mp[prefix] = bank
    answers = []
    for card in cards:
        ans = "UNKNOWN"
        # 前缀最长只有 20，卡号更短时只枚举到卡号长度
        upper = len(card)
        if upper > 20:
            upper = 20
        L = upper
        while L >= 1:
            pref = card[:L]
            if pref in mp:
                ans = mp[pref]
                break
            L -= 1
        answers.append(ans)
    return answers


def main():
    # 先读 n 条规则，再读 m 个卡号，每个卡号输出一行银行名
    n = int(input())
    prefixes = []
    for _ in range(n):
        parts = input().split()
        prefixes.append((parts[0], parts[1]))
    m = int(input())
    cards = []
    for _ in range(m):
        cards.append(input().strip())
    answers = solve(prefixes, cards)
    for name in answers:
        print(name)


if __name__ == "__main__":
    main()
