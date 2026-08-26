## 解题思路

模板字符串 $\textit{pat}$ 中，`?` 表示该位可填任意小写字母；非 `?` 的位必须填指定字母。要求相邻两位的字母不能相等，求总方案数模 $10^9+7$。

采用逐位 DP。维护一个长度为 $26$ 的数组 $f[c]$，表示当前前缀以字符 $c$ 结尾的方案数。

初始化第 $0$ 位：

- 若 $\textit{pat}[0]$ 是 `?`：$f[c] = 1$ 对所有 $c \in [0, 25]$。
- 若 $\textit{pat}[0]$ 固定为某字符 $c_0$：$f[c_0] = 1$，其余为 $0$。

设 $S = \sum_{c} f[c]$ 为当前前缀的总方案数。

对于第 $i$ 位（$i \ge 1$）：

- 若 $\textit{pat}[i]$ 是 `?`：$f[i][c] = S - f[i-1][c]$（不能和上一位同字符）。
- 若 $\textit{pat}[i]$ 固定为某字符 $c_0$：只更新 $f[i][c_0] = S - f[i-1][c_0]$，其余为 $0$。

每步重新计算 $S = \sum_{c} f[i][c]$，若 $S = 0$ 说明无合法方案，可提前结束。

最终答案为 $S$。

## 复杂度分析

设每组测试数据长度为 $m$，所有测试数据长度总和为 $M$。

- 每组扫描 $m$ 个位置，每步枚举 $26$ 个字符更新，时间复杂度 $O(26m)$，总时间复杂度 $O(26M)$。
- 只需两个长为 $26$ 的数组滚动更新，空间复杂度 $O(26) = O(1)$。

## 代码实现

### Python

```python
import sys

MOD = 10 ** 9 + 7

def solve_one(m, pat):
    # 初始化 f[c]：第一位是 '?' 则所有 c 都为 1，否则只有固定字符为 1
    f = [int(pat[0] == '?' or c == ord(pat[0]) - 97) for c in range(26)]
    # 当前前缀总方案数
    total = sum(f) % MOD
    for i in range(1, m):
        nf = [0] * 26  # 下一轮 f
        if pat[i] == '?':
            # 通配符：每个字符 c 不能和上一位相同
            for c in range(26):
                nf[c] = (total - f[c]) % MOD
        else:
            # 固定字符：只更新对应位置
            c0 = ord(pat[i]) - 97
            nf[c0] = (total - f[c0]) % MOD
        f = nf
        # 重新计算总方案数
        total = sum(f) % MOD
        # 无合法方案则提前结束
        if total == 0:
            break
    return total

def main():
    # 快速读取所有输入
    data = sys.stdin.buffer.read().split()
    it = iter(data)
    T = int(next(it))
    out = []
    for _ in range(T):
        m = int(next(it))
        pat = next(it).decode()
        out.append(str(solve_one(m, pat)))
    # 一次性输出所有结果
    sys.stdout.write('\n'.join(out))

if __name__ == '__main__':
    main()
```

### Java

```java
import java.io.*;
import java.util.*;

public class Main {
    static final int MOD = 1000000007;

    static int solveOne(int m, String pat) {
        long[] f = new long[26];
        // 初始化 f[c]：第一位是 '?' 则所有 c 都为 1，否则只有固定字符为 1
        if (pat.charAt(0) == '?') Arrays.fill(f, 1);
        else f[pat.charAt(0) - 'a'] = 1;

        // 当前前缀总方案数
        long total = 0;
        for (long v : f) total = (total + v) % MOD;

        for (int i = 1; i < m; i++) {
            char ch = pat.charAt(i);
            long[] nf = new long[26];  // 下一轮 f
            if (ch == '?') {
                // 通配符：每个字符 c 不能和上一位相同
                for (int c = 0; c < 26; c++)
                    nf[c] = (total - f[c] + MOD) % MOD;
            } else {
                // 固定字符：只更新对应位置
                int c = ch - 'a';
                nf[c] = (total - f[c] + MOD) % MOD;
            }
            f = nf;
            // 重新计算总方案数
            total = 0;
            for (long v : f) total = (total + v) % MOD;
            // 无合法方案则提前结束
            if (total == 0) break;
        }
        return (int) total;
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StringBuilder out = new StringBuilder();
        int T = Integer.parseInt(br.readLine());
        for (int cas = 0; cas < T; cas++) {
            StringTokenizer st = new StringTokenizer(br.readLine());
            int m = Integer.parseInt(st.nextToken());
            String pat = st.nextToken();
            out.append(solveOne(m, pat)).append('\n');
        }
        System.out.print(out.toString());
    }
}
```

### C++

```cpp
#include <iostream>
#include <string>
#include <vector>
using namespace std;

const int MOD = 1000000007;

int solve_one(int m, const string& pat) {
    vector<long long> f(26, 0);
    // 初始化 f[c]：第一位是 '?' 则所有 c 都为 1，否则只有固定字符为 1
    if (pat[0] == '?')
        for (int c = 0; c < 26; ++c) f[c] = 1;
    else
        f[pat[0] - 'a'] = 1;

    // 当前前缀总方案数
    long long total = 0;
    for (int c = 0; c < 26; ++c) total += f[c];
    total %= MOD;

    for (int i = 1; i < m; ++i) {
        vector<long long> nf(26, 0);  // 下一轮 f
        if (pat[i] == '?') {
            // 通配符：每个字符 c 不能和上一位相同
            for (int c = 0; c < 26; ++c)
                nf[c] = (total - f[c] + MOD) % MOD;
        } else {
            // 固定字符：只更新对应位置
            int c = pat[i] - 'a';
            nf[c] = (total - f[c] + MOD) % MOD;
        }
        // 滚动更新
        f.swap(nf);
        // 重新计算总方案数
        total = 0;
        for (int c = 0; c < 26; ++c) total += f[c];
        total %= MOD;
        // 无合法方案则提前结束
        if (total == 0) break;
    }
    return (int)total;
}

int main() {
    // 加速 IO
    ios::sync_with_stdio(false); cin.tie(nullptr);
    int T; cin >> T;
    while (T--) {
        int m; string pat;
        cin >> m >> pat;
        cout << solve_one(m, pat) << '\n';
    }
    return 0;
}
```
