def solve_one(length, tag):
    # rightCnt 统计当前位右侧尚未处理的原标签字符数量
    right_cnt = [0] * 26
    for ch in tag:
        right_cnt[ord(ch) - ord('a')] += 1

    # leftCnt 统计左侧已校正完成的最终字符数量
    left_cnt = [0] * 26

    ans = []

    for ch in tag:
        idx = ord(ch) - ord('a')

        # 当前字符不再属于右侧，先从右侧计数中删去
        right_cnt[idx] -= 1

        # leftCnt：左侧最终字符中等于当前 glyph 的个数
        left_cnt_val = left_cnt[idx]

        # rightCnt：右侧原串中等于当前 glyph 的个数
        right_cnt_val = right_cnt[idx]

        # 两侧计数相等则轮询到下一个小写字母
        if left_cnt_val == right_cnt_val:
            new_idx = (idx + 1) % 26
        else:
            new_idx = idx

        ans.append(chr(new_idx + ord('a')))
        left_cnt[new_idx] += 1

    return ''.join(ans)


def main():
    tc = int(input())
    for _ in range(tc):
        length = int(input())
        tag = input().strip()
        print(solve_one(length, tag))


if __name__ == "__main__":
    main()
