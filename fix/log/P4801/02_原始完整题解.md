## 解题思路

给定两个长度均为 $n$ 的完整序列 $p,q$，要求求出：

1. 它们的最长共鸣序列长度；
2. 在所有最长共鸣序列中，输出逐位比较意义下最大的那一个。

### 核心思路

因为 $p,q$ 都是 $1\sim n$ 的完整序列，每个数字只出现一次，所以这道题可以转化为 LIS 问题。

先记：

* $pos_q[x]$ 表示数字 $x$ 在序列 $q$ 中的位置。

把序列 $p$ 映射成一个新数组 $a$：

$$
a_i = pos_q[p_i]
$$

那么：

* 如果 $p$ 中选出一个子序列，它在 $q$ 中也是子序列；
* 等价于这些元素在 $q$ 中的位置严格递增。

因此，原问题就变成了：

* 在数组 $a$ 中求最长严格递增子序列；
* 但最终输出的不是位置，而是对应的数字 $p_i$；
* 并且在所有最长 LIS 对应的共鸣序列中，要选逐位比较意义下最大的那个。

---

### 如何求每个位置作为起点的最长长度

设：

$$
f_i
$$

表示在 $p_i$ 这个元素被选为当前子序列第一个元素时，后面最多还能形成多长的合法共鸣序列长度（包含自己）。

由于要保证在 $q$ 中顺序递增，所以有转移：

$$
f_i = 1 + \max(f_j), \quad j>i,\ a_j>a_i
$$

这就是“从右往左做 LIS”。

可以用树状数组维护“后缀最大值”：

* 从右往左扫描 $p$；
* 对于当前位置 $i$，查询所有 $a_j>a_i$ 的位置中最大的 $f_j$；
* 得到 $f_i$ 后再更新树状数组。

这样就能在 $O(n\log n)$ 内求出所有 $f_i$。

---

### 如何恢复逐位比较意义下最大的答案

设最长长度为 $L$。

把所有数字按它们对应的 $f$ 值分组。
例如某个数字 $x$ 满足：

* 在 $p$ 中位置为 $pos_p[x]$
* 在 $q$ 中位置为 $pos_q[x]$
* 它作为起点能得到的最长长度为 $dp[x]$

那么它就属于第 $dp[x]$ 组。

接下来贪心恢复答案：

* 当前还需要选出长度为 $len$ 的后缀；
* 上一个选中的数字在 $p,q$ 中的位置分别为 $last_p,last_q$；
* 那么当前可选的数字 $x$ 必须满足：

  1. $dp[x]=len$
  2. $pos_p[x]>last_p$
  3. $pos_q[x]>last_q$

只要满足这三个条件，就说明可以把 $x$ 放在当前这一位，并且后面还能继续凑出长度 $len-1$ 的合法答案。

为了让最终序列在逐位比较下最大，当前这一位显然应当选满足条件的**最大数字**。

这一步仍可用树状数组完成：

* 对于当前层 $len$，把所有满足 $pos_p[x]>last_p$ 的数字加入树状数组；
* 树状数组按 $q$ 中位置维护区间最大值；
* 查询所有 $pos_q[x]>last_q$ 的候选里，最大的数字即可。

因为每个数字只会出现在某一层里一次，所有层加起来总共还是 $n$ 个数字，所以总复杂度仍为 $O(n\log n)$。

---

### 实现方法

1. 读入完整序列 $p,q$；
2. 预处理：

   * $pos_p[x]$
   * $pos_q[x]$
3. 将 $p$ 映射为位置数组 $a_i=pos_q[p_i]$；
4. 从右往左用树状数组求每个位置的最长后缀长度；
5. 得到每个数字 $x$ 的 $dp[x]$，并按 $dp[x]$ 分组；
6. 从长度 $L$ 开始逐层贪心，选出当前能选的最大数字；
7. 输出答案。

## 复杂度分析

设单组数据长度为 $n$。

### 时间复杂度

1. 映射与预处理：$O(n)$
2. 求所有 $dp$：每个位置一次查询、一次修改，复杂度 $O(n\log n)$
3. 按层恢复答案：每个数字只会被处理一次，总复杂度 $O(n\log n)$

因此总时间复杂度为：

$$
O(n\log n)
$$

### 空间复杂度

需要存储：

* 两个完整序列；
* 位置数组；
* $dp$ 数组；
* 分组数组；
* 树状数组。

总空间复杂度为：

$$
O(n)
$$

## 代码实现

### Python

```python
import sys


# 树状数组：维护前缀最大值
class BITMax:
    def __init__(self, n):
        self.n = n
        self.tree = [0] * (n + 2)

    # 单点更新：取最大值
    def update(self, x, val):
        while x <= self.n:
            if val > self.tree[x]:
                self.tree[x] = val
            x += x & -x

    # 查询前缀最大值
    def query(self, x):
        res = 0
        while x > 0:
            if self.tree[x] > res:
                res = self.tree[x]
            x -= x & -x
        return res


# 求逐位比较意义下最大的最长共鸣序列
def solve_case(n, p, q):
    # 记录每个数字在 p 和 q 中的位置
    pos_p = [0] * (n + 1)
    pos_q = [0] * (n + 1)

    for i in range(n):
        pos_p[p[i]] = i + 1
        pos_q[q[i]] = i + 1

    # a[i] 表示 p[i] 在 q 中的位置
    a = [0] * n
    for i in range(n):
        a[i] = pos_q[p[i]]

    # dp_val[x] 表示以数字 x 作为当前起点时，最多能形成的合法长度
    dp_val = [0] * (n + 1)

    # 从右往左做 LIS，树状数组维护“右侧比当前大的位置”的最大 dp
    bit = BITMax(n)
    max_len = 0

    for i in range(n - 1, -1, -1):
        # 把“位置大于 a[i]”的后缀最大值转成前缀查询
        rev = n - a[i] + 1
        best = bit.query(rev - 1)
        cur = best + 1
        dp_val[p[i]] = cur
        bit.update(rev, cur)
        if cur > max_len:
            max_len = cur

    # 按 dp 长度分组
    groups = [[] for _ in range(max_len + 1)]
    for x in range(1, n + 1):
        groups[dp_val[x]].append(x)

    # 贪心恢复逐位比较意义下最大的答案
    ans = []
    last_p = 0
    last_q = 0

    for need in range(max_len, 0, -1):
        bit = BITMax(n)

        # 这一层只需要处理一次，把所有在 p 中位置合法的数字加入树状数组
        for x in groups[need]:
            if pos_p[x] > last_p:
                rev_q = n - pos_q[x] + 1
                bit.update(rev_q, x)

        # 查询所有 pos_q[x] > last_q 的候选中的最大数字
        limit = n - last_q
        choose = bit.query(limit)

        ans.append(choose)
        last_p = pos_p[choose]
        last_q = pos_q[choose]

    return max_len, ans


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    t = data[0]
    idx = 1
    out = []

    for _ in range(t):
        n = data[idx]
        idx += 1

        p = data[idx:idx + n]
        idx += n

        q = data[idx:idx + n]
        idx += n

        k, ans = solve_case(n, p, q)
        out.append(str(k))
        out.append(" ".join(map(str, ans)))

    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    main()
```

### Java

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.StringTokenizer;

public class Main {

    // 读入工具
    static class FastScanner {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StringTokenizer st;

        String next() throws IOException {
            while (st == null || !st.hasMoreTokens()) {
                st = new StringTokenizer(br.readLine());
            }
            return st.nextToken();
        }

        int nextInt() throws IOException {
            return Integer.parseInt(next());
        }
    }

    // 树状数组：维护前缀最大值
    static class BITMax {
        int n;
        int[] tree;

        BITMax(int n) {
            this.n = n;
            this.tree = new int[n + 2];
        }

        // 单点更新：取最大值
        void update(int x, int val) {
            while (x <= n) {
                if (val > tree[x]) {
                    tree[x] = val;
                }
                x += x & -x;
            }
        }

        // 查询前缀最大值
        int query(int x) {
            int res = 0;
            while (x > 0) {
                if (tree[x] > res) {
                    res = tree[x];
                }
                x -= x & -x;
            }
            return res;
        }
    }

    // 返回结果
    static class Result {
        int len;
        int[] seq;

        Result(int len, int[] seq) {
            this.len = len;
            this.seq = seq;
        }
    }

    // 求逐位比较意义下最大的最长共鸣序列
    static Result solveCase(int n, int[] p, int[] q) {
        int[] posP = new int[n + 1];
        int[] posQ = new int[n + 1];

        // 记录数字在 p 中的位置
        for (int i = 1; i <= n; i++) {
            posP[p[i]] = i;
        }

        // 记录数字在 q 中的位置
        for (int i = 1; i <= n; i++) {
            posQ[q[i]] = i;
        }

        // a[i] 表示 p[i] 在 q 中的位置
        int[] a = new int[n + 1];
        for (int i = 1; i <= n; i++) {
            a[i] = posQ[p[i]];
        }

        // dpVal[x] 表示以数字 x 开头时，最长能取多少个
        int[] dpVal = new int[n + 1];
        BITMax bit = new BITMax(n);
        int maxLen = 0;

        // 从右往左求 LIS 的“起点长度”
        for (int i = n; i >= 1; i--) {
            int rev = n - a[i] + 1;
            int best = bit.query(rev - 1);
            int cur = best + 1;
            dpVal[p[i]] = cur;
            bit.update(rev, cur);
            if (cur > maxLen) {
                maxLen = cur;
            }
        }

        // 按 dp 长度分组
        ArrayList<Integer>[] groups = new ArrayList[maxLen + 1];
        for (int i = 1; i <= maxLen; i++) {
            groups[i] = new ArrayList<>();
        }
        for (int x = 1; x <= n; x++) {
            groups[dpVal[x]].add(x);
        }

        // 贪心恢复逐位比较意义下最大的答案
        int[] ans = new int[maxLen];
        int lastP = 0;
        int lastQ = 0;

        for (int need = maxLen, idx = 0; need >= 1; need--, idx++) {
            bit = new BITMax(n);

            // 把当前层中在 p 中位置合法的数字加入树状数组
            for (int x : groups[need]) {
                if (posP[x] > lastP) {
                    int revQ = n - posQ[x] + 1;
                    bit.update(revQ, x);
                }
            }

            // 查询所有 posQ[x] > lastQ 的候选中的最大数字
            int limit = n - lastQ;
            int choose = bit.query(limit);

            ans[idx] = choose;
            lastP = posP[choose];
            lastQ = posQ[choose];
        }

        return new Result(maxLen, ans);
    }

    public static void main(String[] args) throws Exception {
        FastScanner fs = new FastScanner();
        StringBuilder sb = new StringBuilder();

        int t = fs.nextInt();
        while (t-- > 0) {
            int n = fs.nextInt();

            int[] p = new int[n + 1];
            int[] q = new int[n + 1];

            for (int i = 1; i <= n; i++) {
                p[i] = fs.nextInt();
            }
            for (int i = 1; i <= n; i++) {
                q[i] = fs.nextInt();
            }

            Result res = solveCase(n, p, q);
            sb.append(res.len).append('\n');
            for (int i = 0; i < res.seq.length; i++) {
                if (i > 0) {
                    sb.append(' ');
                }
                sb.append(res.seq[i]);
            }
            sb.append('\n');
        }

        System.out.print(sb.toString());
    }
}
```

### C++

```cpp
#include <iostream>
#include <vector>
using namespace std;

// 树状数组：维护前缀最大值
class BITMax {
public:
    int n;
    vector<int> tree;

    BITMax(int n) {
        this->n = n;
        tree.assign(n + 2, 0);
    }

    // 单点更新：取最大值
    void update(int x, int val) {
        while (x <= n) {
            if (val > tree[x]) {
                tree[x] = val;
            }
            x += x & -x;
        }
    }

    // 查询前缀最大值
    int query(int x) {
        int res = 0;
        while (x > 0) {
            if (tree[x] > res) {
                res = tree[x];
            }
            x -= x & -x;
        }
        return res;
    }
};

// 求逐位比较意义下最大的最长共鸣序列
pair<int, vector<int>> solve_case(int n, vector<int>& p, vector<int>& q) {
    vector<int> pos_p(n + 1), pos_q(n + 1);

    // 记录数字在 p 和 q 中的位置
    for (int i = 1; i <= n; i++) {
        pos_p[p[i]] = i;
        pos_q[q[i]] = i;
    }

    // a[i] 表示 p[i] 在 q 中的位置
    vector<int> a(n + 1);
    for (int i = 1; i <= n; i++) {
        a[i] = pos_q[p[i]];
    }

    // dp_val[x] 表示以数字 x 开头时，最长能形成的合法长度
    vector<int> dp_val(n + 1, 0);
    BITMax bit(n);
    int max_len = 0;

    // 从右往左求 LIS 的“起点长度”
    for (int i = n; i >= 1; i--) {
        int rev = n - a[i] + 1;
        int best = bit.query(rev - 1);
        int cur = best + 1;
        dp_val[p[i]] = cur;
        bit.update(rev, cur);
        if (cur > max_len) {
            max_len = cur;
        }
    }

    // 按 dp 长度分组
    vector<vector<int>> groups(max_len + 1);
    for (int x = 1; x <= n; x++) {
        groups[dp_val[x]].push_back(x);
    }

    // 贪心恢复逐位比较意义下最大的答案
    vector<int> ans;
    int last_p = 0;
    int last_q = 0;

    for (int need = max_len; need >= 1; need--) {
        BITMax cur_bit(n);

        // 把当前层中在 p 中位置合法的数字加入树状数组
        for (int x : groups[need]) {
            if (pos_p[x] > last_p) {
                int rev_q = n - pos_q[x] + 1;
                cur_bit.update(rev_q, x);
            }
        }

        // 查询所有 pos_q[x] > last_q 的候选中的最大数字
        int limit = n - last_q;
        int choose = cur_bit.query(limit);

        ans.push_back(choose);
        last_p = pos_p[choose];
        last_q = pos_q[choose];
    }

    return {max_len, ans};
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int T;
    cin >> T;

    while (T--) {
        int n;
        cin >> n;

        vector<int> p(n + 1), q(n + 1);
        for (int i = 1; i <= n; i++) {
            cin >> p[i];
        }
        for (int i = 1; i <= n; i++) {
            cin >> q[i];
        }

        pair<int, vector<int>> res = solve_case(n, p, q);

        cout << res.first << '\n';
        for (int i = 0; i < (int)res.second.size(); i++) {
            if (i > 0) {
                cout << ' ';
            }
            cout << res.second[i];
        }
        cout << '\n';
    }

    return 0;
}
```