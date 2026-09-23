def solve(s):
    """统计每个字符出现次数。
    先按次数从高到低、次数相同再按字符本身排序，保证三语言输出一致。
    同一字符必须连在一起输出。
    """
    cnt = {}
    for ch in s:
        cnt[ch] = cnt.get(ch, 0) + 1
    items = list(cnt.items())
    # 次数高的在前；次数相同按字符 ASCII 从小到大，便于对拍
    items.sort(key=lambda x: (-x[1], x[0]))
    parts = []
    for ch, c in items:
        parts.append(ch * c)
    return "".join(parts)


def main():
    # 一整行就是 s，含大小写字母和数字
    s = input().strip()
    print(solve(s))


if __name__ == "__main__":
    main()
