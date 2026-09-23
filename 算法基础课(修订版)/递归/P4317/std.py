def comb(digits):
    # 电话按键映射
    mp = {
        '2': "abc", '3': "def", '4': "ghi", '5': "jkl",
        '6': "mno", '7': "pqrs", '8': "tuv", '9': "wxyz"
    }
    res = []
    n = len(digits)
    if n == 0:
        return res

    # 回溯函数
    def dfs(idx, path):
        if idx == n:
            res.append("".join(path))
            return
        for ch in mp[digits[idx]]:
            path.append(ch)       # 选择
            dfs(idx+1, path)      # 递归
            path.pop()            # 撤销

    dfs(0, [])
    return res

# 示例
if __name__ == "__main__":
    s = input().strip()
    for out in comb(s):
        print(out)
