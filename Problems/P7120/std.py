class Solution:
    def threeDigitEvens(self, digits):
        # cnt[d] 表示数字 d 在数组里出现了几次
        cnt = [0] * 10
        for d in digits:
            cnt[d] += 1

        res = []
        # 百位从 1 开始枚举，天然排除了前导零
        for a in range(1, 10):
            if cnt[a] == 0:
                continue
            # 用掉一个 a（先扣掉，后面还要还回来）
            cnt[a] -= 1
            for b in range(10):
                if cnt[b] == 0:
                    continue
                cnt[b] -= 1
                # 个位只能是偶数，才能保证整个数是偶数
                for c in (0, 2, 4, 6, 8):
                    if cnt[c] == 0:
                        continue
                    # 三个数位都够用，组成一个合法的三位偶数
                    res.append(a * 100 + b * 10 + c)
                # 还回 b，继续试下一个十位
                cnt[b] += 1
            # 还回 a，继续试下一个百位
            cnt[a] += 1

        # 百位、十位、个位都是从小到大枚举的，所以 res 已经是递增顺序，
        # 且每个整数只被枚举一次（数位确定则整数唯一），天然互不相同
        return res


def main():
    # 第一行：数组长度 n
    n = int(input())
    # 第二行：n 个 0~9 的数字
    digits = list(map(int, input().split()))
    ans = Solution().threeDigitEvens(digits)

    # 第一行输出个数 k
    print(len(ans))
    # 只有 k>0 时才输出第二行；k=0 时题面要求只输出一行 0
    if ans:
        print(" ".join(str(x) for x in ans))


if __name__ == "__main__":
    main()
