## 解题思路

先固定一个失灵字母 $c$，考虑有多少个原始字符串删除所有 $c$ 后可以得到 $s$。

如果 $s$ 中已经出现了字母 $c$，那么这种情况不可能。因为键盘中字母 $c$ 失灵，原始字符串中所有的 $c$ 都不会被输入，所以最终得到的 $s$ 中不可能含有 $c$。

因此，只有没有出现在 $s$ 中的字母才可能是失灵字母。

接下来考虑固定一个没有出现在 $s$ 中的字母 $c$。

原始字符串可以看成是在 $s$ 的字符之间，以及字符串两端插入若干个 $c$：

$s_1,s_2\cdots_n$

由于原始字符串中任意相邻两个字符都不相同，所以：

1. 每个空位最多只能插入一个 $c$，否则会出现相邻的 $cc$。
2. 字符串两端的空位可以选择插入或不插入 $c$，各有 $2$ 种选择。
3. 对于中间位置 $s_i$ 和 $s_{i+1}$：

   * 如果 $s_i = s_{i+1}$，那么必须插入一个 $c$，否则原始字符串中会有相邻相同字符。
   * 如果 $s_i \ne s_{i+1}$，那么可以插入或不插入 $c$，有 $2$ 种选择。

设 $diff$ 表示 $s$ 中相邻两个字符不同的位置数量，即：

$$
diff = |{i \mid 1 \le i < n,\ s_i \ne s_{i+1}}|
$$

那么对于每一个没有在 $s$ 中出现的失灵字母 $c$，可构造的原始字符串数量为：

$$
2^{diff + 2}
$$

其中 $+2$ 来自字符串首尾两个空位。

设 $kind$ 表示 $s$ 中出现过的不同字母数量，那么可能作为失灵字母的数量为：

$$
26 - kind
$$

所以答案为：

$$
(26 - kind) \times 2^{diff + 2} \bmod (10^9 + 7)
$$

实现时，对于每组数据：

1. 扫描字符串，统计出现过的字母种类数。
2. 扫描相邻字符，统计 $diff$。
3. 使用预处理好的 $2^k$ 数组计算答案。

## 复杂度分析

设所有测试数据的字符串总长度为 $S$。

每个字符串只需要线性扫描一次，因此时间复杂度为：

$$
O(S)
$$

预处理 $2^k$ 的范围最多到最大字符串长度加 $2$，复杂度为：

$$
O(n_{\max})
$$

总时间复杂度为：

$$
O(S + n_{\max})
$$

空间上主要使用幂数组，大小为最大字符串长度加 $2$，因此空间复杂度为：

$$
O(n_{\max})
$$

复杂度满足题目要求。

## 代码实现

### Python

```python
import sys

MOD = 10 ** 9 + 7


def calc(s, pow2):
    # 记录每个字母是否在 s 中出现过
    vis = [False] * 26

    # 统计 s 中不同字母的数量
    kind = 0
    for ch in s:
        x = ord(ch) - ord('a')
        if not vis[x]:
            vis[x] = True
            kind += 1

    # 统计相邻字符不同的位置数量
    diff = 0
    for i in range(len(s) - 1):
        if s[i] != s[i + 1]:
            diff += 1

    # 只有没有出现在 s 中的字母才可能是失灵字母
    miss = 26 - kind

    # 每个可行失灵字母对应 2^(diff + 2) 种原始字符串
    return miss * pow2[diff + 2] % MOD


def main():
    data = sys.stdin.read().split()
    t = int(data[0])

    arr = []
    max_n = 0
    idx = 1

    # 读取所有测试数据，顺便记录最大长度
    for _ in range(t):
        n = int(data[idx])
        s = data[idx + 1]
        idx += 2
        arr.append(s)
        if n > max_n:
            max_n = n

    # 预处理 2 的幂
    pow2 = [1] * (max_n + 3)
    for i in range(1, max_n + 3):
        pow2[i] = pow2[i - 1] * 2 % MOD

    ans = []
    for s in arr:
        ans.append(str(calc(s, pow2)))

    print("\n".join(ans))


if __name__ == "__main__":
    main()
```

### Java

```java
import java.io.*;
import java.util.*;

public class Main {
    static final long MOD = 1000000007L;

    static long calc(String s, long[] pow2) {
        // 记录每个字母是否在 s 中出现过
        boolean[] vis = new boolean[26];

        // 统计 s 中不同字母的数量
        int kind = 0;
        for (int i = 0; i < s.length(); i++) {
            int x = s.charAt(i) - 'a';
            if (!vis[x]) {
                vis[x] = true;
                kind++;
            }
        }

        // 统计相邻字符不同的位置数量
        int diff = 0;
        for (int i = 0; i + 1 < s.length(); i++) {
            if (s.charAt(i) != s.charAt(i + 1)) {
                diff++;
            }
        }

        // 只有没有出现在 s 中的字母才可能是失灵字母
        int miss = 26 - kind;

        // 每个可行失灵字母对应 2^(diff + 2) 种原始字符串
        return miss * pow2[diff + 2] % MOD;
    }

    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));

        int t = Integer.parseInt(br.readLine());
        String[] arr = new String[t];

        int maxN = 0;

        // 读取所有测试数据，顺便记录最大长度
        for (int i = 0; i < t; i++) {
            int n = Integer.parseInt(br.readLine());
            String s = br.readLine();
            arr[i] = s;
            if (n > maxN) {
                maxN = n;
            }
        }

        // 预处理 2 的幂
        long[] pow2 = new long[maxN + 3];
        pow2[0] = 1;
        for (int i = 1; i < pow2.length; i++) {
            pow2[i] = pow2[i - 1] * 2 % MOD;
        }

        StringBuilder sb = new StringBuilder();

        for (int i = 0; i < t; i++) {
            sb.append(calc(arr[i], pow2)).append('\n');
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

long long calc(const string& s, const vector<long long>& pow2) {
    // 记录每个字母是否在 s 中出现过
    vector<int> vis(26, 0);

    // 统计 s 中不同字母的数量
    int kind = 0;
    for (char ch : s) {
        int x = ch - 'a';
        if (!vis[x]) {
            vis[x] = 1;
            kind++;
        }
    }

    // 统计相邻字符不同的位置数量
    int diff = 0;
    for (int i = 0; i + 1 < (int)s.size(); i++) {
        if (s[i] != s[i + 1]) {
            diff++;
        }
    }

    // 只有没有出现在 s 中的字母才可能是失灵字母
    int miss = 26 - kind;

    // 每个可行失灵字母对应 2^(diff + 2) 种原始字符串
    return miss * pow2[diff + 2] % MOD;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int T;
    cin >> T;

    vector<string> arr(T);
    int maxN = 0;

    // 读取所有测试数据，顺便记录最大长度
    for (int i = 0; i < T; i++) {
        int n;
        string s;
        cin >> n >> s;
        arr[i] = s;
        maxN = max(maxN, n);
    }

    // 预处理 2 的幂
    vector<long long> pow2(maxN + 3, 1);
    for (int i = 1; i < (int)pow2.size(); i++) {
        pow2[i] = pow2[i - 1] * 2 % MOD;
    }

    for (int i = 0; i < T; i++) {
        cout << calc(arr[i], pow2) << '\n';
    }

    return 0;
}
```