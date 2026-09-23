# 按分数升序赋平均名次，再用 Mann-Whitney U 还原 AUC


def auc_from_ranks(labels, scores):
    """
    标签 1 为欺诈，0 为正常。分数越大越像欺诈。
    并列分数占用一段名次区间，区间内每笔都取左右端点的均值。
    """
    m = len(labels)
    # 按下标稳定排序，保证同分时相对顺序确定
    order = sorted(range(m), key=lambda i: scores[i])
    rank = [0.0] * m
    i = 0
    while i < m:
        j = i
        # 向右扩到同一分数的最后一笔
        while j + 1 < m and scores[order[j + 1]] == scores[order[i]]:
            j += 1
        # 名次从 1 起，区间 [i+1, j+1]
        avg = (i + 1 + j + 1) / 2.0
        for k in range(i, j + 1):
            rank[order[k]] = avg
        i = j + 1

    k_pos = 0
    s_pos = 0.0
    for i in range(m):
        if labels[i] == 1:
            k_pos += 1
            s_pos += rank[i]
    k_neg = m - k_pos
    # U 统计量：正类名次和减去「全排在最前」时的最小名次和
    u = s_pos - k_pos * (k_pos + 1) / 2.0
    return u / (k_pos * k_neg)


def main():
    # 四级协议：第一行笔数，第二行标签，第三行风险分
    m = int(input())
    labels = list(map(int, input().split()))
    scores = list(map(float, input().split()))
    auc = auc_from_ranks(labels, scores)
    print("{:.6f}".format(auc))


if __name__ == "__main__":
    main()
