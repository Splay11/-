def solve(s):
    """按空格切开得到单词，空段丢掉。
    平均长度 = 所有单词字符数之和 / 单词个数，保留两位小数。
    """
    words = s.split()
    # 题面保证至少有一个单词
    total = 0
    for w in words:
        total += len(w)
    avg = total / len(words)
    # 固定两位小数，与样例格式一致
    return "{:.2f}".format(avg)


def main():
    # 一整行就是句子，单词之间可能有多个空格
    s = input()
    print(solve(s))


if __name__ == "__main__":
    main()
