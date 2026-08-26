## 解题思路

先固定一个位置 $i$，思考哪些包含 $i$ 的连续子区间 $[l\dots r]$ 会让 $a_i$ 恰好成为该区间的中位数。

### 关键性质转化

设当前子区间中：

* 比 $a_i$ 小的数有 $x$ 个；
* 比 $a_i$ 大的数有 $y$ 个。

因为原数组是一个排列，所以区间内元素互不相同，且一定包含 $a_i$ 本身，因此区间长度为：

$$
x+y+1
$$

而 $a_i$ 排序后的位置就是第 $x+1$ 个。

题目规定中位数是排序后第

$$
\left\lceil \frac{len+1}{2}\right\rceil
$$

个元素，所以要让 $a_i$ 成为中位数，必须满足：

$$
x+1=\left\lceil \frac{x+y+2}{2}\right\rceil
$$

把奇偶分开看更直观：

* 当区间长度为奇数时，设长度为 $2k+1$，则中位数是第 $k+1$ 个，所以必须有
  $$
  x=k,\ y=k
  $$
  即
  $$
  x=y
  $$

* 当区间长度为偶数时，设长度为 $2k$，则中位数是第 $k+1$ 个，所以必须有
  $$
  x=k,\ y=k-1
  $$
  即
  $$
  x=y+1
  $$

因此，$a_i$ 成为区间中位数的充要条件是：

$$
x-y\in{0,1}
$$



### 转化为区间和问题

对于固定位置 $i$，定义相对 $a_i$ 的贡献值：

* 若 $a_j<a_i$，记为 $+1$；
* 若 $a_j>a_i$，记为 $-1$；
* $j=i$ 不参与统计。

那么对于任意包含 $i$ 的区间 $[l\dots r]$，其两侧所有元素的贡献和恰好就是：

$$
x-y
$$

于是问题转化为：

> 对于每个位置 $i$，统计多少个包含 $i$ 的区间，使得两侧贡献和属于 ${0,1}$。



### 如何高效统计

固定中心位置 $i$ 后，把区间拆成左右两部分：

* 左边部分为 $[l\dots i-1]$
* 右边部分为 $[i+1\dots r]$

设：

* 左边贡献和为 $L$
* 右边贡献和为 $R$

则总贡献和为：

$$
L+R
$$

我们需要满足：

$$
L+R=0 \quad 或 \quad L+R=1
$$

也就是：

$$
L=-R \quad 或 \quad L=1-R
$$

#### 具体做法

对于固定的 $i$：

1. 从 $i-1$ 向左枚举左端点，计算所有可能的左侧贡献和 $L$，统计每个和出现了多少次；
2. 再从 $i$ 向右枚举右端点：

   * 当右端点为 $i$ 时，表示右侧为空，$R=0$；
   * 每往右扩展一个元素，就更新一次 $R$；
3. 对于当前 $R$，答案增加：
   $$
   \text{cnt}[-R]+\text{cnt}[1-R]
   $$
   其中 $\text{cnt}[s]$ 表示左侧贡献和等于 $s$ 的方案数。

注意左侧也允许为空，所以一开始要把左侧和为 $0$ 的情况记一次。


## 复杂度分析

对于每个位置 $i$：

* 向左枚举一次，复杂度为 $O(n)$；
* 向右枚举一次，复杂度为 $O(n)$。

因此单个位置的复杂度为 $O(n)$，总复杂度为：

$$
O(n^2)
$$

题目保证所有测试数据的 $n$ 之和不超过 $5000$，所以总复杂度至多约为：

$$
O(5000^2)
$$

完全可以通过。

空间复杂度方面，计数数组大小为 $O(n)$，因此空间复杂度为：

$$
O(n)
$$

## 代码实现

### Python

```python
import sys


def solve_case(n, a):
    # ans[i] 表示第 i 个位置作为中位数的连续子区间个数
    ans = [0] * n

    # 贡献和的范围在 [-n, n]，开一个足够大的数组做计数
    offset = n + 2
    size = 2 * n + 5

    # 依次枚举每个位置作为中心
    for i in range(n):
        cnt = [0] * size

        # 左侧为空时，左侧贡献和为 0，这是一种合法情况
        cnt[offset] = 1

        # 从 i-1 向左枚举，统计所有左侧贡献和出现次数
        cur = 0
        for l in range(i - 1, -1, -1):
            if a[l] < a[i]:
                cur += 1
            else:
                cur -= 1
            cnt[cur + offset] += 1

        # 从 i 开始向右枚举，r=i 表示右侧为空
        cur = 0
        for r in range(i, n):
            if r > i:
                if a[r] < a[i]:
                    cur += 1
                else:
                    cur -= 1

            # 需要满足 left_sum + cur == 0 或 1
            ans[i] += cnt[-cur + offset] + cnt[1 - cur + offset]

    return ans


def main():
    data = list(map(int, sys.stdin.read().split()))
    t = data[0]
    idx = 1
    out = []

    for _ in range(t):
        n = data[idx]
        idx += 1
        a = data[idx:idx + n]
        idx += n

        res = solve_case(n, a)
        out.append(" ".join(map(str, res)))

    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    main()
```

### Java

```java
import java.io.BufferedInputStream;
import java.util.StringJoiner;

public class Main {

    // 计算一组数据的答案
    public static long[] solveCase(int n, int[] a) {
        // ans[i] 表示第 i 个位置作为中位数的连续子区间个数
        long[] ans = new long[n];

        // 贡献和范围为 [-n, n]
        int offset = n + 2;
        int size = 2 * n + 5;

        // 枚举每个位置作为中心
        for (int i = 0; i < n; i++) {
            int[] cnt = new int[size];

            // 左侧为空，贡献和为 0
            cnt[offset] = 1;

            // 从 i-1 向左枚举，统计左侧贡献和出现次数
            int cur = 0;
            for (int l = i - 1; l >= 0; l--) {
                if (a[l] < a[i]) {
                    cur++;
                } else {
                    cur--;
                }
                cnt[cur + offset]++;
            }

            // 从 i 开始向右枚举，r=i 表示右侧为空
            cur = 0;
            for (int r = i; r < n; r++) {
                if (r > i) {
                    if (a[r] < a[i]) {
                        cur++;
                    } else {
                        cur--;
                    }
                }

                // 统计满足 left_sum + cur == 0 或 1 的方案数
                ans[i] += cnt[-cur + offset];
                ans[i] += cnt[1 - cur + offset];
            }
        }

        return ans;
    }

    public static void main(String[] args) throws Exception {
        FastScanner fs = new FastScanner();

        int T = fs.nextInt();
        StringBuilder sb = new StringBuilder();

        while (T-- > 0) {
            int n = fs.nextInt();
            int[] a = new int[n];
            for (int i = 0; i < n; i++) {
                a[i] = fs.nextInt();
            }

            long[] ans = solveCase(n, a);

            StringJoiner sj = new StringJoiner(" ");
            for (int i = 0; i < n; i++) {
                sj.add(String.valueOf(ans[i]));
            }
            sb.append(sj).append('\n');
        }

        System.out.print(sb.toString());
    }

    // 题目数据范围不大，使用普通输入方式即可
    static class FastScanner {
        private final BufferedInputStream in = new BufferedInputStream(System.in);
        private final byte[] buffer = new byte[1 << 16];
        private int ptr = 0, len = 0;

        private int read() throws Exception {
            if (ptr >= len) {
                len = in.read(buffer);
                ptr = 0;
                if (len <= 0) {
                    return -1;
                }
            }
            return buffer[ptr++];
        }

        int nextInt() throws Exception {
            int c;
            do {
                c = read();
            } while (c <= ' ');

            int sign = 1;
            if (c == '-') {
                sign = -1;
                c = read();
            }

            int val = 0;
            while (c > ' ') {
                val = val * 10 + (c - '0');
                c = read();
            }
            return val * sign;
        }
    }
}
```

### C++

```cpp
#include <iostream>
#include <vector>
using namespace std;

// 计算一组数据的答案
vector<long long> solveCase(int n, const vector<int>& a) {
    // ans[i] 表示第 i 个位置作为中位数的连续子区间个数
    vector<long long> ans(n, 0);

    // 贡献和范围为 [-n, n]
    int offset = n + 2;
    int size = 2 * n + 5;

    // 枚举每个位置作为中心
    for (int i = 0; i < n; i++) {
        vector<int> cnt(size, 0);

        // 左侧为空，贡献和为 0
        cnt[offset] = 1;

        // 从 i-1 向左枚举，统计所有左侧贡献和出现次数
        int cur = 0;
        for (int l = i - 1; l >= 0; l--) {
            if (a[l] < a[i]) {
                cur++;
            } else {
                cur--;
            }
            cnt[cur + offset]++;
        }

        // 从 i 开始向右枚举，r=i 表示右侧为空
        cur = 0;
        for (int r = i; r < n; r++) {
            if (r > i) {
                if (a[r] < a[i]) {
                    cur++;
                } else {
                    cur--;
                }
            }

            // 统计满足 left_sum + cur == 0 或 1 的方案数
            ans[i] += cnt[-cur + offset];
            ans[i] += cnt[1 - cur + offset];
        }
    }

    return ans;
}

int main() {
    int T;
    cin >> T;

    while (T--) {
        int n;
        cin >> n;

        vector<int> a(n);
        for (int i = 0; i < n; i++) {
            cin >> a[i];
        }

        vector<long long> ans = solveCase(n, a);

        for (int i = 0; i < n; i++) {
            if (i) {
                cout << ' ';
            }
            cout << ans[i];
        }
        cout << '\n';
    }

    return 0;
}
```