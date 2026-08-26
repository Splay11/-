## 解题思路

把一个正整数判为“喜欢”，需要同时满足两个条件：

1. 不能被$3$整除；
2. 十进制表示中不能出现数字$3$。

题目要求按升序求第$k$个这样的数。由于$k$最大到$10^{18}$，显然不能暴力枚举。

这里使用的核心算法是：

* 数位动态规划
* 按位构造答案

### 1. 数位状态设计

一个数是否能被$3$整除，只和它各位数字和对$3$取模有关。

所以我们可以设：

* $dp[i][r]$ 表示还要填$i$位，当前前缀对$3$取模为$r$时，最终能组成多少个合法数。

不过实现时更自然的是倒着定义：

* `f[len][mod]`：恰好填满`len`位后，当前数对$3$取模为`mod`的方案数。

因为不能出现数字$3$，可选数字集合为：

* 首位：$[1,2,4,5,6,7,8,9]$
* 非首位：$[0,1,2,4,5,6,7,8,9]$

最后只统计模$3$不为$0$的数。

### 2. 先统计每种长度有多少个合法数

设`cnt[len]`表示恰好`len`位的喜欢的数有多少个。

那么对每个询问的$k$，先从短位数开始减：

* 如果$k > cnt[1]$，则说明答案不在$1$位数里；
* 继续减去$cnt[2]、cnt[3]...$；
* 找到最小的长度`L`，使得第$k$个数在`L`位数中。

### 3. 按位构造第$k$个数

知道答案长度后，从高位到低位依次枚举当前位可以填的数字，按从小到大的顺序尝试。

假设当前前缀模$3$为`cur`，当前尝试填数字`d`，那么新模数为：

$$
nxt = (cur \times 10 + d) \bmod 3
$$

然后统计“后面剩余位数能组成多少个最终合法数”。

* 如果这些方案数小于$k$，说明答案不在这一段里，$k$减掉它；
* 否则这一位就是`d`，继续往后构造。

这样就能直接得到第$k$个喜欢的数。

### 4. 为什么这样构造是升序

对于固定长度的十进制数，按字典序枚举，和按数值升序是一致的。
而我们又是先按长度从小到大处理，所以整体顺序就是题目要求的升序。

## 复杂度分析

预处理的位数很少。因为$k \le 10^{18}$，答案长度不会很长，预处理到$25$位已经足够。

* 预处理时间复杂度：$O(L \times 10 \times 3)$
* 单次询问时间复杂度：$O(L \times 10)$
* 空间复杂度：$O(L \times 3)$

其中$L$表示预处理的最大位数，实际取$25$即可，复杂度完全足够。

## 代码实现

### Python

```python
# 题目功能写在外部函数里

# 预处理最大位数，25足够覆盖本题数据范围
MAX_LEN = 25

# 可选数字
FIRST = [1, 2, 4, 5, 6, 7, 8, 9]
OTHER = [0, 1, 2, 4, 5, 6, 7, 8, 9]

# suf[i][r]：还剩i位要填，当前前缀模3为r时，最终能组成多少个合法数
suf = [[0] * 3 for _ in range(MAX_LEN + 1)]

# 边界：没有位可填时，当前数模3不为0才合法
for r in range(3):
    suf[0][r] = 1 if r != 0 else 0

# 预处理后缀方案数
for i in range(1, MAX_LEN + 1):
    for r in range(3):
        total = 0
        for d in OTHER:
            nr = (r * 10 + d) % 3
            total += suf[i - 1][nr]
        suf[i][r] = total

# cnt[len]：恰好len位的喜欢的数个数
cnt = [0] * (MAX_LEN + 1)
for length in range(1, MAX_LEN + 1):
    total = 0
    for d in FIRST:
        total += suf[length - 1][d % 3]
    cnt[length] = total


def kth_number(k):
    # 先确定答案长度
    length = 1
    while k > cnt[length]:
        k -= cnt[length]
        length += 1

    # 按位构造答案
    ans = []
    cur_mod = 0
    for pos in range(length):
        digits = FIRST if pos == 0 else OTHER
        rest = length - pos - 1
        for d in digits:
            nxt_mod = (cur_mod * 10 + d) % 3
            ways = suf[rest][nxt_mod]
            if k > ways:
                k -= ways
            else:
                ans.append(str(d))
                cur_mod = nxt_mod
                break
    return ''.join(ans)


def main():
    t = int(input())
    for _ in range(t):
        k = int(input())
        print(kth_number(k))


if __name__ == "__main__":
    main()
```

### Java

```java
import java.util.Scanner;

public class Main {
    // 预处理最大位数
    static final int MAX_LEN = 25;

    // 首位和其他位可选数字
    static int[] FIRST = {1, 2, 4, 5, 6, 7, 8, 9};
    static int[] OTHER = {0, 1, 2, 4, 5, 6, 7, 8, 9};

    // suf[i][r]：还剩i位要填，当前前缀模3为r时，最终能组成多少个合法数
    static long[][] suf = new long[MAX_LEN + 1][3];

    // cnt[len]：恰好len位的喜欢的数个数
    static long[] cnt = new long[MAX_LEN + 1];

    // 预处理
    static void init() {
        // 边界：没有位可填时，当前数模3不为0才合法
        for (int r = 0; r < 3; r++) {
            suf[0][r] = (r != 0) ? 1 : 0;
        }

        // 预处理后缀方案数
        for (int i = 1; i <= MAX_LEN; i++) {
            for (int r = 0; r < 3; r++) {
                long total = 0;
                for (int d : OTHER) {
                    int nr = (r * 10 + d) % 3;
                    total += suf[i - 1][nr];
                }
                suf[i][r] = total;
            }
        }

        // 统计每种长度的合法数个数
        for (int len = 1; len <= MAX_LEN; len++) {
            long total = 0;
            for (int d : FIRST) {
                total += suf[len - 1][d % 3];
            }
            cnt[len] = total;
        }
    }

    // 求第k个喜欢的数
    static String kthNumber(long k) {
        int len = 1;
        while (k > cnt[len]) {
            k -= cnt[len];
            len++;
        }

        StringBuilder ans = new StringBuilder();
        int curMod = 0;

        // 按位构造答案
        for (int pos = 0; pos < len; pos++) {
            int[] digits = (pos == 0) ? FIRST : OTHER;
            int rest = len - pos - 1;

            for (int d : digits) {
                int nxtMod = (curMod * 10 + d) % 3;
                long ways = suf[rest][nxtMod];

                if (k > ways) {
                    k -= ways;
                } else {
                    ans.append(d);
                    curMod = nxtMod;
                    break;
                }
            }
        }

        return ans.toString();
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        init();

        int t = sc.nextInt();
        while (t-- > 0) {
            long k = sc.nextLong();
            System.out.println(kthNumber(k));
        }
        sc.close();
    }
}
```

### C++

```cpp
#include <iostream>
#include <vector>
#include <string>
using namespace std;

// 预处理最大位数
const int MAX_LEN = 25;

// 首位和其他位可选数字
vector<int> FIRST = {1, 2, 4, 5, 6, 7, 8, 9};
vector<int> OTHER = {0, 1, 2, 4, 5, 6, 7, 8, 9};

// suf[i][r]：还剩i位要填，当前前缀模3为r时，最终能组成多少个合法数
long long suf[MAX_LEN + 1][3];

// cnt[len]：恰好len位的喜欢的数个数
long long cnt[MAX_LEN + 1];

// 预处理
void init() {
    // 边界：没有位可填时，当前数模3不为0才合法
    for (int r = 0; r < 3; r++) {
        suf[0][r] = (r != 0 ? 1 : 0);
    }

    // 预处理后缀方案数
    for (int i = 1; i <= MAX_LEN; i++) {
        for (int r = 0; r < 3; r++) {
            long long total = 0;
            for (int d : OTHER) {
                int nr = (r * 10 + d) % 3;
                total += suf[i - 1][nr];
            }
            suf[i][r] = total;
        }
    }

    // 统计每种长度的合法数个数
    for (int len = 1; len <= MAX_LEN; len++) {
        long long total = 0;
        for (int d : FIRST) {
            total += suf[len - 1][d % 3];
        }
        cnt[len] = total;
    }
}

// 求第k个喜欢的数
string kthNumber(long long k) {
    int len = 1;
    while (k > cnt[len]) {
        k -= cnt[len];
        len++;
    }

    string ans = "";
    int curMod = 0;

    // 按位构造答案
    for (int pos = 0; pos < len; pos++) {
        vector<int>& digits = (pos == 0 ? FIRST : OTHER);
        int rest = len - pos - 1;

        for (int d : digits) {
            int nxtMod = (curMod * 10 + d) % 3;
            long long ways = suf[rest][nxtMod];

            if (k > ways) {
                k -= ways;
            } else {
                ans += char('0' + d);
                curMod = nxtMod;
                break;
            }
        }
    }

    return ans;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    init();

    int t;
    cin >> t;
    while (t--) {
        long long k;
        cin >> k;
        cout << kthNumber(k) << '\n';
    }

    return 0;
}
```