## 解题思路

设字符串为 $s$，若 $i<j$ 且 $s_i>s_j$，则 $(i,j)$ 是一个不稳定对。题目本质上就是：

* 先求字符串原本的逆序对数量；
* 再考虑一次操作对逆序对数量的影响，求最大增量。

### 核心思路

一次操作选择 $i<j$，将：

* $s_i$ 变成它的下一个字母；
* $s_j$ 变成它的上一个字母。

设原字符串的不稳定值为 $\text{inv}$，操作后的增量为 $\Delta$，则答案为：

$$
\text{inv} + \max(0,\Delta)
$$

因此重点就是如何高效求出一次操作的最大增量。



### 1. 把一次操作的影响拆开

假设位置 $i$ 的字符为 $x$，位置 $j$ 的字符为 $y$。

记：

* $A_i$：只把位置 $i$ 的字符做“后移一个字母”时，对总不稳定值的变化量；
* $B_j$：只把位置 $j$ 的字符做“前移一个字母”时，对总不稳定值的变化量。

如果简单把它们相加，会把 $(i,j)$ 这一对的影响算错一次，因此还需要一个修正项。

于是一次操作 $(i,j)$ 的总增量为：

$$
A_i + B_j + C(x,y)
$$

其中 $C(x,y)$ 只和原来的两个字符有关，表示二者这一对的修正量。



### 2. 如何计算 $A_i$

设当前位置字符为 $c$。

当 $c$ 变成下一个字母时，只会影响与它相关的所有对：

* 左边位置 $k<i$：原来判断 $s_k>c$，现在判断 $s_k>\text{next}(c)$；
* 右边位置 $k>i$：原来判断 $c>s_k$，现在判断 $\text{next}(c)>s_k$。

分情况讨论。

#### 情况一：$c\neq z$

此时 $c \to c+1$。

* 左边能少贡献多少？

  只有左边那些恰好等于 $c+1$ 的字符，原来满足 $s_k>c$，现在不满足 $s_k>c+1$，所以减少：

  $$
  \text{prefix}[c+1]
  $$

* 右边能多贡献多少？

  只有右边那些恰好等于 $c$ 的字符，原来 $c\not>s_k$，现在 $c+1>s_k$，所以增加：

  $$
  \text{suffix}[c]
  $$

所以：

$$
A_i=-\text{prefix}[c+1]+\text{suffix}[c]
$$

#### 情况二：$c=z$

此时 $z \to a$，是循环变化。

* 左边：原来判断 $s_k>z$ 永远为假，现在判断 $s_k>a$，只有不是 $a$ 的字符都满足，所以增加

  $$
  (i-1)-\text{prefix}[a]
  $$

* 右边：原来判断 $z>s_k$，除去 $z$ 外都成立；现在判断 $a>s_k$ 永远为假，所以减少

  $$
  (n-i)-\text{suffix}[z]
  $$

因此：

$$
A_i=((i-1)-\text{prefix}[a]) - ((n-i)-\text{suffix}[z])
$$

这里的 $\text{prefix}[x]$ 表示位置 $i$ 左边字符 $x$ 的个数，$\text{suffix}[x]$ 表示位置 $i$ 右边字符 $x$ 的个数。



### 3. 如何计算 $B_j$

同理，设当前位置字符为 $c$，现在要把它变成前一个字母。

#### 情况一：$c\neq a$

此时 $c \to c-1$。

* 左边：判断从 $s_k>c$ 变成 $s_k>c-1$，恰好多出左边等于 $c$ 的字符，所以增加

  $$
  \text{prefix}[c]
  $$

* 右边：判断从 $c>s_k$ 变成 $c-1>s_k$，恰好少掉右边等于 $c-1$ 的字符，所以减少

  $$
  \text{suffix}[c-1]
  $$

所以：

$$
B_j=\text{prefix}[c]-\text{suffix}[c-1]
$$

#### 情况二：$c=a$

此时 $a \to z$。

* 左边：原来判断 $s_k>a$，不是 $a$ 的都成立；现在判断 $s_k>z$ 永远为假，所以减少

  $$
  (j-1)-\text{prefix}[a]
  $$

* 右边：原来判断 $a>s_k$ 永远为假；现在判断 $z>s_k$，除去 $z$ 外都成立，所以增加

  $$
  (n-j)-\text{suffix}[z]
  $$

因此：

$$
B_j=-((j-1)-\text{prefix}[a]) + ((n-j)-\text{suffix}[z])
$$



### 4. 修正项 $C(x,y)$

设：

* $x'=\text{next}(x)$
* $y'=\text{prev}(y)$

对于这一对 $(i,j)$，原本贡献是：

$$
[x>y]
$$

操作后贡献是：

$$
[x'>y']
$$

而 $A_i+B_j$ 中已经分别把这一对按“只改左端点”“只改右端点”各算了一次，因此修正项为：

$$
C(x,y)=[x'>y']-[x'>y]-[x>y']+[x>y]
$$

其中 $[P]$ 表示命题 $P$ 成立时为 $1$，否则为 $0$。

由于字母只有 $26$ 种，$C(x,y)$ 可以预处理成一个 $26\times26$ 的表。



### 5. 如何在线性时间求最优操作

我们要求：

$$
\max_{i<j}{A_i+B_j+C(s_i,s_j)}
$$

若直接枚举 $(i,j)$ 会超时。

注意到：

* $B_j$ 只和位置 $j$ 有关；
* $C(s_i,s_j)$ 只和两个字符种类有关；
* $A_i$ 只和位置 $i$ 有关。

因此当我们从左到右枚举右端点 $j$ 时，只需要知道左边每种字符作为左端点时，$A_i$ 的最大值。

设：

$$
best[x] = \max(A_i)
$$

其中位置 $i<j$ 且 $s_i=x$。

那么对于当前右端点 $j$，最优左端点带来的增量就是：

$$
\max_x { best[x] + C(x,s_j) } + B_j
$$

因为字母只有 $26$ 种，所以枚举 $x$ 的代价是常数级，整组数据总复杂度就是线性的。



### 实现方法

整体流程如下：

1. 先求原字符串的不稳定值 $\text{inv}$；
2. 再扫描一遍字符串，利用前缀计数和总计数计算出每个位置的 $A_i,B_i$；
3. 预处理 $26\times26$ 的修正表 $C$；
4. 从左到右枚举右端点 $j$：

   * 用左边已经出现过的位置更新 `best`
   * 枚举 $26$ 种左端点字符，求当前能得到的最大增量
5. 最终答案为：

   $$
   \text{inv}+\max(0,\text{最大增量})
   $$



## 复杂度分析

### 时间复杂度

设单组字符串长度为 $n$。

* 计算原始不稳定值：$O(26n)$
* 计算每个位置的 $A_i,B_i$：$O(n)$
* 扫描求最优操作：每个位置枚举 $26$ 个字母，复杂度 $O(26n)$

因此总时间复杂度为：

$$
O(26n)
$$

由于 $26$ 是常数，所以也可以视为：

$$
O(n)
$$

在所有测试数据总长度不超过 $2\times 10^5$ 的条件下，完全可行。

### 空间复杂度

只使用了若干长度为 $n$ 的数组以及若干长度为 $26$ 的计数数组，因此空间复杂度为：

$$
O(n)
$$



## 代码实现

### Python

```python
import sys


# 计算单组测试数据的答案
def solve_one(n, s):
    # 将字符转成 0~25，便于计算
    a = [ord(ch) - ord('a') for ch in s]

    # 统计每种字符的总出现次数
    total = [0] * 26
    for c in a:
        total[c] += 1

    # A[i]：只把第 i 个字符后移一个字母时的增量
    # B[i]：只把第 i 个字符前移一个字母时的增量
    A = [0] * n
    B = [0] * n

    # 计算原始不稳定值
    inv = 0
    pre = [0] * 26
    seen = 0

    for i in range(n):
        c = a[i]

        # 当前位置左边比它大的字符个数，就是新增的不稳定对数量
        not_greater = 0
        for x in range(c + 1):
            not_greater += pre[x]
        inv += seen - not_greater

        # 前缀长度和后缀长度
        prefix_len = i
        suffix_len = n - i - 1

        # 计算 A[i]
        if c < 25:
            # 非 z，后移到 c+1
            suffix_c = total[c] - pre[c] - 1
            A[i] = -pre[c + 1] + suffix_c
        else:
            # z -> a
            suffix_z = total[25] - pre[25] - 1
            A[i] = (prefix_len - pre[0]) - (suffix_len - suffix_z)

        # 计算 B[i]
        if c > 0:
            # 非 a，前移到 c-1
            suffix_prev = total[c - 1] - pre[c - 1]
            B[i] = pre[c] - suffix_prev
        else:
            # a -> z
            suffix_z = total[25] - pre[25]
            B[i] = -(prefix_len - pre[0]) + (suffix_len - suffix_z)

        # 更新前缀计数
        pre[c] += 1
        seen += 1

    # 预处理修正项 C[x][y]
    C = [[0] * 26 for _ in range(26)]
    for x in range(26):
        nx = (x + 1) % 26
        for y in range(26):
            py = (y - 1 + 26) % 26

            old_val = 1 if x > y else 0
            left_only = 1 if nx > y else 0
            right_only = 1 if x > py else 0
            new_val = 1 if nx > py else 0

            C[x][y] = new_val - left_only - right_only + old_val

    # best[ch]：左边所有字符等于 ch 的位置中，A[i] 的最大值
    NEG = -10 ** 18
    best = [NEG] * 26

    # 最优增量，允许不操作，所以初始为 0
    best_delta = 0

    # 枚举右端点 j
    for j in range(n):
        y = a[j]

        # 枚举左端点字符种类
        cur = NEG
        for x in range(26):
            if best[x] != NEG:
                value = best[x] + C[x][y]
                if value > cur:
                    cur = value

        if cur != NEG:
            candidate = cur + B[j]
            if candidate > best_delta:
                best_delta = candidate

        # 当前点作为未来某个操作的左端点
        if A[j] > best[y]:
            best[y] = A[j]

    return inv + best_delta


def main():
    input = sys.stdin.readline
    T = int(input().strip())
    ans = []

    for _ in range(T):
        n = int(input().strip())
        s = input().strip()
        ans.append(str(solve_one(n, s)))

    print("\n".join(ans))


if __name__ == "__main__":
    main()
```

### Java

```java
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.IOException;


public class Main {

    // 计算单组测试数据的答案
    static long solveOne(int n, String s) {
        // 将字符串转成 0~25 的整数数组
        int[] a = new int[n];
        for (int i = 0; i < n; i++) {
            a[i] = s.charAt(i) - 'a';
        }

        // 统计每种字符总出现次数
        int[] total = new int[26];
        for (int i = 0; i < n; i++) {
            total[a[i]]++;
        }

        // A[i]：只把第 i 个字符后移一个字母时的增量
        // B[i]：只把第 i 个字符前移一个字母时的增量
        long[] A = new long[n];
        long[] B = new long[n];

        // 计算原始不稳定值
        long inv = 0;
        int[] pre = new int[26];
        int seen = 0;

        for (int i = 0; i < n; i++) {
            int c = a[i];

            // 统计左边小于等于当前字符的个数
            int notGreater = 0;
            for (int x = 0; x <= c; x++) {
                notGreater += pre[x];
            }
            // 左边总数减去小于等于当前字符的个数，就是左边比它大的个数
            inv += (long) seen - notGreater;

            int prefixLen = i;
            int suffixLen = n - i - 1;

            // 计算 A[i]
            if (c < 25) {
                // 非 z，后移到 c+1
                int suffixC = total[c] - pre[c] - 1;
                A[i] = -pre[c + 1] + suffixC;
            } else {
                // z -> a
                int suffixZ = total[25] - pre[25] - 1;
                A[i] = (long) (prefixLen - pre[0]) - (suffixLen - suffixZ);
            }

            // 计算 B[i]
            if (c > 0) {
                // 非 a，前移到 c-1
                int suffixPrev = total[c - 1] - pre[c - 1];
                B[i] = pre[c] - suffixPrev;
            } else {
                // a -> z
                int suffixZ = total[25] - pre[25];
                B[i] = -(long) (prefixLen - pre[0]) + (suffixLen - suffixZ);
            }

            // 更新前缀计数
            pre[c]++;
            seen++;
        }

        // 预处理修正项 C[x][y]
        int[][] C = new int[26][26];
        for (int x = 0; x < 26; x++) {
            int nx = (x + 1) % 26;
            for (int y = 0; y < 26; y++) {
                int py = (y - 1 + 26) % 26;

                int oldVal = x > y ? 1 : 0;
                int leftOnly = nx > y ? 1 : 0;
                int rightOnly = x > py ? 1 : 0;
                int newVal = nx > py ? 1 : 0;

                C[x][y] = newVal - leftOnly - rightOnly + oldVal;
            }
        }

        // best[ch]：左边字符等于 ch 的位置中，A[i] 的最大值
        long NEG = -(long) 4e18;
        long[] best = new long[26];
        for (int i = 0; i < 26; i++) {
            best[i] = NEG;
        }

        // 最优增量，允许不操作，所以初始为 0
        long bestDelta = 0;

        // 枚举右端点 j
        for (int j = 0; j < n; j++) {
            int y = a[j];

            long cur = NEG;
            for (int x = 0; x < 26; x++) {
                if (best[x] != NEG) {
                    long value = best[x] + C[x][y];
                    if (value > cur) {
                        cur = value;
                    }
                }
            }

            if (cur != NEG) {
                long candidate = cur + B[j];
                if (candidate > bestDelta) {
                    bestDelta = candidate;
                }
            }

            // 当前点作为未来某个操作的左端点
            if (A[j] > best[y]) {
                best[y] = A[j];
            }
        }

        return inv + bestDelta;
    }

    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int T = Integer.parseInt(br.readLine().trim());
        StringBuilder sb = new StringBuilder();

        while (T-- > 0) {
            int n = Integer.parseInt(br.readLine().trim());
            String s = br.readLine().trim();
            sb.append(solveOne(n, s)).append('\n');
        }

        System.out.print(sb.toString());
    }
}
```

### C++

```cpp
#include <bits/stdc++.h>
using namespace std;


// 计算单组测试数据的答案
long long solve_one(int n, const string &s) {
    // 将字符串转成 0~25 的整数数组
    vector<int> a(n);
    for (int i = 0; i < n; i++) {
        a[i] = s[i] - 'a';
    }

    // 统计每种字符总出现次数
    vector<int> total(26, 0);
    for (int c : a) {
        total[c]++;
    }

    // A[i]：只把第 i 个字符后移一个字母时的增量
    // B[i]：只把第 i 个字符前移一个字母时的增量
    vector<long long> A(n), B(n);

    // 计算原始不稳定值
    long long inv = 0;
    vector<int> pre(26, 0);
    int seen = 0;

    for (int i = 0; i < n; i++) {
        int c = a[i];

        // 统计左边小于等于当前字符的个数
        int not_greater = 0;
        for (int x = 0; x <= c; x++) {
            not_greater += pre[x];
        }
        // 左边总数减去小于等于当前字符的个数，就是左边比它大的个数
        inv += 1LL * seen - not_greater;

        int prefix_len = i;
        int suffix_len = n - i - 1;

        // 计算 A[i]
        if (c < 25) {
            // 非 z，后移到 c+1
            int suffix_c = total[c] - pre[c] - 1;
            A[i] = -pre[c + 1] + suffix_c;
        } else {
            // z -> a
            int suffix_z = total[25] - pre[25] - 1;
            A[i] = 1LL * (prefix_len - pre[0]) - (suffix_len - suffix_z);
        }

        // 计算 B[i]
        if (c > 0) {
            // 非 a，前移到 c-1
            int suffix_prev = total[c - 1] - pre[c - 1];
            B[i] = pre[c] - suffix_prev;
        } else {
            // a -> z
            int suffix_z = total[25] - pre[25];
            B[i] = -1LL * (prefix_len - pre[0]) + (suffix_len - suffix_z);
        }

        // 更新前缀计数
        pre[c]++;
        seen++;
    }

    // 预处理修正项 C[x][y]
    int C[26][26];
    for (int x = 0; x < 26; x++) {
        int nx = (x + 1) % 26;
        for (int y = 0; y < 26; y++) {
            int py = (y - 1 + 26) % 26;

            int old_val = (x > y ? 1 : 0);
            int left_only = (nx > y ? 1 : 0);
            int right_only = (x > py ? 1 : 0);
            int new_val = (nx > py ? 1 : 0);

            C[x][y] = new_val - left_only - right_only + old_val;
        }
    }

    // best[ch]：左边字符等于 ch 的位置中，A[i] 的最大值
    const long long NEG = -(long long)4e18;
    vector<long long> best(26, NEG);

    // 最优增量，允许不操作，所以初始为 0
    long long best_delta = 0;

    // 枚举右端点 j
    for (int j = 0; j < n; j++) {
        int y = a[j];

        long long cur = NEG;
        for (int x = 0; x < 26; x++) {
            if (best[x] != NEG) {
                long long value = best[x] + C[x][y];
                cur = max(cur, value);
            }
        }

        if (cur != NEG) {
            long long candidate = cur + B[j];
            best_delta = max(best_delta, candidate);
        }

        // 当前点作为未来某个操作的左端点
        best[y] = max(best[y], A[j]);
    }

    return inv + best_delta;
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
        cout << solve_one(n, s) << '\n';
    }

    return 0;
}
```