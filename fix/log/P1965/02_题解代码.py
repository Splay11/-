## 思路：动态规划

考虑dp[i][g]含义为前i个数，恰好将g个0变成1的最大价值.

转移为：考虑枚举最后一段连续1的位置：

case1:考虑最后连续1以i结尾，dp[i][g] = dp[j - 1][g - zero_count(arr[j:i+1])] + (j - i + 1)^2 , 

> 这里枚举j从i到1，zero_count(arr[j:i+1])表示j到i之间0的个数，我们需要把他们全部变为1

case2:考虑最后连续1不以i结尾，dp[i][g] = dp[i - 1][g]

> 这里枚举g即可。


## 代码

### python
```python
# 输入n和k，分别表示字符串的长度和最多可以将多少个0变为1
n, k = map(int, input().split())
# 输入字符串s
s = input()

# 初始化动态规划数组dp
# dp[i][g]表示前i个数，恰好将g个0变成1的最大价值
dp = [[0] * (k + 1) for _ in range(n + 1)]
# dp[0][k]初始化为0，表示没有数时的价值为0
dp[0][k] = 0

# 遍历每一个位置
for i in range(1, n + 1):
    zero_cnt = 0  # 统计当前连续1段中0的数量
    # 从当前i位置向前遍历
    for j in range(i, 0, -1):
        # 如果当前位置是'0'，增加0的计数
        if s[j - 1] == '0':
            zero_cnt += 1
        # 如果0的数量超过k，结束当前循环
        if zero_cnt - 1 > k:
            break
        # 遍历所有可能的g，从当前的zero_cnt到k
        for g in range(zero_cnt, k + 1):
            length = i - j + 1  # 当前段的长度
            # 更新dp[i][g]，选择最大价值
            dp[i][g] = max(dp[i][g], dp[j - 1][g - zero_cnt] + length * length)
    
    # 更新dp[i][g]，考虑不以i结尾的情况
    for g in range(k + 1):
        dp[i][g] = max(dp[i][g], dp[i - 1][g])

# 输出最终结果，前n个数，恰好将k个0变为1的最大价值
print(dp[n][k])
```

OJ会员可以通过点击题目上方《已通过》查看其他通过代码来学习。