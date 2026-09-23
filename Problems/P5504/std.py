from collections import deque


def sliding_max_1d(arr, k):
    # 单调双端队列求一维窗口最大值
    n = len(arr)
    res = [0] * (n - k + 1)
    dq = deque()
    for i in range(n):
        while dq and arr[dq[-1]] <= arr[i]:
            dq.pop()
        dq.append(i)
        if dq[0] <= i - k:
            dq.popleft()
        if i >= k - 1:
            res[i - k + 1] = arr[dq[0]]
    return res


def window_max(mat, k):
    n = len(mat)
    m = len(mat[0])
    # 先对每一行做长度为 k 的滑动窗口最大值
    row_max = [sliding_max_1d(mat[i], k) for i in range(n)]
    # 再对每一列做长度为 k 的滑动窗口最大值
    cols = m - k + 1
    rows = n - k + 1
    ans = [[0] * cols for _ in range(rows)]
    for j in range(cols):
        col = [row_max[i][j] for i in range(n)]
        col_res = sliding_max_1d(col, k)
        for i in range(rows):
            ans[i][j] = col_res[i]
    return ans


def main():
    n, m, k = map(int, input().split())
    mat = []
    for _ in range(n):
        mat.append(list(map(int, input().split())))
    ans = window_max(mat, k)
    for row in ans:
        print(" ".join(str(x) for x in row))


if __name__ == "__main__":
    main()
