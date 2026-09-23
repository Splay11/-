def majority_element(nums):
    """Boyer-Moore 投票：抵消不同元素后，剩下的一定是多数元素（题目保证存在）。"""
    cand = 0
    cnt = 0
    for x in nums:
        # 当前没有候选人，把这个数立为候选人
        if cnt == 0:
            cand = x
            cnt = 1
        elif x == cand:
            # 碰到候选人，票数加一
            cnt += 1
        else:
            # 碰到其他数，互相抵消一票
            cnt -= 1
    # 题目保证多数元素一定存在，抵消结束后候选人就是答案
    return cand


def main():
    # 第一行：数组长度
    n = int(input())
    # 第二行：n 个整数
    nums = list(map(int, input().split()))
    print(majority_element(nums))


if __name__ == "__main__":
    main()
