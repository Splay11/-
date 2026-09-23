def solve(words, k):
    """先统计每个单词出现次数，再排序取前 k 个。
    排序关键字：次数从大到小；次数相同则按字典序从小到大。
    """
    cnt = {}
    for w in words:
        cnt[w] = cnt.get(w, 0) + 1
    # -次数保证高频在前，第二个关键字是单词本身的字典序
    items = sorted(cnt.keys(), key=lambda w: (-cnt[w], w))
    return items[:k]


def main():
    # 第一行 n、k，第二行 n 个小写单词
    n, k = map(int, input().split())
    words = input().split()
    ans = solve(words, k)
    print(" ".join(ans))


if __name__ == "__main__":
    main()
