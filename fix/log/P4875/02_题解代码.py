## 解题思路

本题可以使用动态规划。

由于信号串只包含 `0` 和 `1`，我们从左到右处理信号串，维护当前最后一段字符的信息。

设：

* $odd[c]$ 表示当前最后一段字符为 $c$，且这一段长度为奇数的方案数；
* $even[c]$ 表示当前最后一段字符为 $c$，且这一段长度为偶数的方案数。

其中 $c=0$ 表示 `0`，$c=1$ 表示 `1`。

处理下一个字符时：

* 如果新字符和上一位相同，那么当前段长度增加 $1$，奇偶性翻转；
* 如果新字符和上一位不同，那么上一段必须已经是奇数长度，才能开启新的一段，新段长度为 $1$，也是奇数。

因此转移为：

* 继续相同字符：

  * $odd[c] \rightarrow even[c]$
  * $even[c] \rightarrow odd[c]$
* 切换字符：

  * 只能从 $odd[1-c]$ 转移到 $odd[c]$

最后答案为：

$$odd[0]+odd[1]$$

因为最终最后一段也必须是奇数长度。

## 复杂度分析

对于每个字符，只需要枚举 `0` 和 `1` 两种情况。

- 时间复杂度：$O(n)$
- 空间复杂度：$O(1)$

所有测试数据的 $n$ 之和不超过 $2 \times 10^5$，复杂度完全满足要求。

## 代码实现

### Python

```python
MOD = 10 ** 9 + 7


# 计算补全方案数：动态规划，维护最后一段信号字符及其长度的奇偶性
def count_ways(s):
    # odd[c]：最后一段字符为 c，且长度为奇数的方案数
    # even[c]：最后一段字符为 c，且长度为偶数的方案数
    odd = [0, 0]
    even = [0, 0]

    # 初始化第一个字符
    for c in range(2):
        ch = '0' if c == 0 else '1'
        if s[0] == '?' or s[0] == ch:
            odd[c] = 1

    # 从第二个字符开始动态规划
    for i in range(1, len(s)):
        new_odd = [0, 0]
        new_even = [0, 0]

        for c in range(2):
            ch = '0' if c == 0 else '1'
            if s[i] != '?' and s[i] != ch:
                continue

            # 继续放相同字符：当前段长度奇偶性翻转
            new_odd[c] = (new_odd[c] + even[c]) % MOD
            new_even[c] = (new_even[c] + odd[c]) % MOD

            # 放不同字符：上一段必须是奇数长度才能开启新段
            new_odd[c] = (new_odd[c] + odd[c ^ 1]) % MOD

        odd, even = new_odd, new_even

    # 最后一段必须是奇数长度
    return (odd[0] + odd[1]) % MOD


def main():
    t = int(input())
    ans = []

    for _ in range(t):
        n = int(input())
        s = input().strip()
        ans.append(str(count_ways(s)))

    print("\n".join(ans))


if __name__ == "__main__":
    main()
```

### Java

```java
import java.io.BufferedReader;
import java.io.InputStreamReader;

public class Main {
    static final long MOD = 1000000007L;

    // 计算补全方案数：动态规划，维护最后一段信号字符及其长度的奇偶性
    static long countWays(String s) {
        // odd[c]：最后一段字符为 c，且长度为奇数的方案数
        // even[c]：最后一段字符为 c，且长度为偶数的方案数
        long[] odd = new long[2];
        long[] even = new long[2];

        // 初始化第一个字符
        for (int c = 0; c < 2; c++) {
            char ch = c == 0 ? '0' : '1';
            if (s.charAt(0) == '?' || s.charAt(0) == ch) {
                odd[c] = 1;
            }
        }

        // 从第二个字符开始动态规划
        for (int i = 1; i < s.length(); i++) {
            long[] newOdd = new long[2];
            long[] newEven = new long[2];

            for (int c = 0; c < 2; c++) {
                char ch = c == 0 ? '0' : '1';
                if (s.charAt(i) != '?' && s.charAt(i) != ch) {
                    continue;
                }

                // 继续放相同字符：当前段长度奇偶性翻转
                newOdd[c] = (newOdd[c] + even[c]) % MOD;
                newEven[c] = (newEven[c] + odd[c]) % MOD;

                // 放不同字符：上一段必须是奇数长度才能开启新段
                newOdd[c] = (newOdd[c] + odd[c ^ 1]) % MOD;
            }

            odd = newOdd;
            even = newEven;
        }

        // 最后一段必须是奇数长度
        return (odd[0] + odd[1]) % MOD;
    }

    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StringBuilder sb = new StringBuilder();

        int T = Integer.parseInt(br.readLine().trim());

        for (int tc = 0; tc < T; tc++) {
            int n = Integer.parseInt(br.readLine().trim());
            String s = br.readLine().trim();

            sb.append(countWays(s)).append('\n');
        }

        System.out.print(sb.toString());
    }
}
```

### C++

```cpp
#include <bits/stdc++.h>
using namespace std;

const long long MOD = 1000000007LL;

// 计算补全方案数：动态规划，维护最后一段信号字符及其长度的奇偶性
long long countWays(const string& s) {
    // odd[c]：最后一段字符为 c，且长度为奇数的方案数
    // even[c]：最后一段字符为 c，且长度为偶数的方案数
    long long odd[2] = {0, 0};
    long long even[2] = {0, 0};

    // 初始化第一个字符
    for (int c = 0; c < 2; c++) {
        char ch = c == 0 ? '0' : '1';
        if (s[0] == '?' || s[0] == ch) {
            odd[c] = 1;
        }
    }

    // 从第二个字符开始动态规划
    for (int i = 1; i < (int)s.size(); i++) {
        long long newOdd[2] = {0, 0};
        long long newEven[2] = {0, 0};

        for (int c = 0; c < 2; c++) {
            char ch = c == 0 ? '0' : '1';
            if (s[i] != '?' && s[i] != ch) {
                continue;
            }

            // 继续放相同字符：当前段长度奇偶性翻转
            newOdd[c] = (newOdd[c] + even[c]) % MOD;
            newEven[c] = (newEven[c] + odd[c]) % MOD;

            // 放不同字符：上一段必须是奇数长度才能开启新段
            newOdd[c] = (newOdd[c] + odd[c ^ 1]) % MOD;
        }

        for (int c = 0; c < 2; c++) {
            odd[c] = newOdd[c];
            even[c] = newEven[c];
        }
    }

    // 最后一段必须是奇数长度
    return (odd[0] + odd[1]) % MOD;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int T;
    cin >> T;

    while (T--) {
        int n;
        string s;
        cin >> n >> s;

        cout << countWays(s) << '\n';
    }

    return 0;
}
```