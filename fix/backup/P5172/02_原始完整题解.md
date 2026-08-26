## 解题思路

核心思路：

路径在确定起点和第一步的步长后，后续经过的下标完全确定。可以根据“下一步应该使用哪个步长”设计两个状态。

设：

* $f_p[i]$ 表示从下标 $i$ 出发，下一步使用步长 $p$ 时，整条路径的价值。
* $f_q[i]$ 表示从下标 $i$ 出发，下一步使用步长 $q$ 时，整条路径的价值。

对于状态 $f_p[i]$：

* 当前下标 $i$ 对应的 $A_i$ 一定会被加入答案。
* 如果 $i+p\le n$，下一步到达 $i+p$，之后应该使用步长 $q$，因此需要加上 $f_q[i+p]$。
* 如果 $i+p>n$，路径直接终止。

所以有：

$$
f_p[i]=A_i+
\begin{cases}
f_q[i+p], & i+p\le n,\
0, & i+p>n.
\end{cases}
$$

同理：

$$
f_q[i]=A_i+
\begin{cases}
f_p[i+q], & i+q\le n,\
0, & i+q>n.
\end{cases}
$$

由于 $p$ 和 $q$ 都是正整数，每次转移都会到达更大的下标，因此不存在环。计算 $f_p[i]$ 和 $f_q[i]$ 时，只会使用下标大于 $i$ 的状态，所以按照下标从 $n$ 到 $1$ 的顺序计算即可。

最终答案为：

$$
\max_{1\le i\le n}\left(f_p[i],f_q[i]\right).
$$

即枚举所有起点，并同时考虑第一步选择 $p$ 或 $q$。

实现方法：

使用两个长度为 $n$ 的数组分别保存 $f_p$ 和 $f_q$。从右向左枚举下标 $i$，根据下一步是否越界完成状态转移，并在计算过程中维护所有状态的最大值。

即使所有 $A_i$ 都是负数，路径也必须按照规则一直行进到无法继续，因此不能将中间状态与 $0$ 取最大值。只有当下一步越界时，后续贡献才为 $0$。

## 复杂度分析

对于每个下标，只计算一次 $f_p[i]$ 和 $f_q[i]$。

时间复杂度为：

$$
O(n)
$$

使用两个长度为 $n$ 的状态数组，空间复杂度为：

$$
O(n)
$$

所有测试数据的 $n$ 之和不超过 $2\times 10^5$，因此该复杂度可以满足要求。

## 代码实现

### Python

```python
import sys


def get_max(n, p, q, a):
    # dp_p[i] 表示从下标 i 出发，下一步使用步长 p 时的路径价值
    # dp_q[i] 表示从下标 i 出发，下一步使用步长 q 时的路径价值
    dp_p = [0] * n
    dp_q = [0] * n

    ans = -10**30

    # 状态只依赖更大的下标，因此从右向左计算
    for i in range(n - 1, -1, -1):
        # 使用步长 p 后，下一步应该使用步长 q
        dp_p[i] = a[i]
        if i + p < n:
            dp_p[i] += dp_q[i + p]

        # 使用步长 q 后，下一步应该使用步长 p
        dp_q[i] = a[i]
        if i + q < n:
            dp_q[i] += dp_p[i + q]

        # 同时考虑两种首步选择
        ans = max(ans, dp_p[i], dp_q[i])

    return ans


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    pos = 0

    t = data[pos]
    pos += 1

    res = []

    for _ in range(t):
        n = data[pos]
        p = data[pos + 1]
        q = data[pos + 2]
        pos += 3

        a = data[pos:pos + n]
        pos += n

        res.append(str(get_max(n, p, q, a)))

    sys.stdout.write("\n".join(res))


if __name__ == "__main__":
    main()
```

### Java

```java
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.StreamTokenizer;

public class Main {
    static long getMax(int n, int p, int q, long[] a) {
        // dpP[i] 表示从下标 i 出发，下一步使用步长 p 时的路径价值
        // dpQ[i] 表示从下标 i 出发，下一步使用步长 q 时的路径价值
        long[] dpP = new long[n];
        long[] dpQ = new long[n];

        long ans = Long.MIN_VALUE;

        // 状态只依赖更大的下标，因此从右向左计算
        for (int i = n - 1; i >= 0; i--) {
            // 使用步长 p 后，下一步应该使用步长 q
            dpP[i] = a[i];
            if (i + p < n) {
                dpP[i] += dpQ[i + p];
            }

            // 使用步长 q 后，下一步应该使用步长 p
            dpQ[i] = a[i];
            if (i + q < n) {
                dpQ[i] += dpP[i + q];
            }

            // 同时考虑两种首步选择
            ans = Math.max(ans, Math.max(dpP[i], dpQ[i]));
        }

        return ans;
    }

    public static void main(String[] args) throws Exception {
        StreamTokenizer in = new StreamTokenizer(
                new BufferedReader(new InputStreamReader(System.in))
        );

        in.nextToken();
        int t = (int) in.nval;

        StringBuilder out = new StringBuilder();

        for (int test = 0; test < t; test++) {
            in.nextToken();
            int n = (int) in.nval;

            in.nextToken();
            int p = (int) in.nval;

            in.nextToken();
            int q = (int) in.nval;

            long[] a = new long[n];

            for (int i = 0; i < n; i++) {
                in.nextToken();
                a[i] = (long) in.nval;
            }

            out.append(getMax(n, p, q, a)).append('\n');
        }

        System.out.print(out);
    }
}
```

### C++

```cpp
#include <bits/stdc++.h>
using namespace std;

long long getMax(int n, int p, int q, const vector<long long>& a) {
    // dpP[i] 表示从下标 i 出发，下一步使用步长 p 时的路径价值
    // dpQ[i] 表示从下标 i 出发，下一步使用步长 q 时的路径价值
    vector<long long> dpP(n);
    vector<long long> dpQ(n);

    long long ans = LLONG_MIN;

    // 状态只依赖更大的下标，因此从右向左计算
    for (int i = n - 1; i >= 0; i--) {
        // 使用步长 p 后，下一步应该使用步长 q
        dpP[i] = a[i];
        if (i + p < n) {
            dpP[i] += dpQ[i + p];
        }

        // 使用步长 q 后，下一步应该使用步长 p
        dpQ[i] = a[i];
        if (i + q < n) {
            dpQ[i] += dpP[i + q];
        }

        // 同时考虑两种首步选择
        ans = max(ans, max(dpP[i], dpQ[i]));
    }

    return ans;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int T;
    cin >> T;

    while (T--) {
        int n, p, q;
        cin >> n >> p >> q;

        vector<long long> a(n);

        for (int i = 0; i < n; i++) {
            cin >> a[i];
        }

        cout << getMax(n, p, q, a) << '\n';
    }

    return 0;
}
```