## 解题思路

* 本题是一个典型的**可行性判定 + 贪心构造**问题。
  记每个元素必须在区间 $[l,r]$ 内，数组长度为 $n$，目标总和为 $m$。
* **可行性判定**：数组元素之和的最小/最大可能值分别为

  $$
  S_{\min}=n\cdot l,\quad S_{\max}=n\cdot r.
  $$

  只有当 $S_{\min}\le m\le S_{\max}$ 时才有解，否则无解（输出 $r+1$）。
* **构造算法（贪心）**：

  1. 先令所有元素为 $l$，此时总和为 $S_{\min}$，剩余需要补到 $m$ 的量为 $\text{rem}=m-S_{\min}$（此时 $\text{rem}\ge 0$）。
  2. 从前到后依次把每个元素在不超过上界 $r$ 的前提下尽量增大：对第 $i$ 个元素，最多还能增加 $(r-l)$，实际增加 $\text{add}=\min(\text{rem},\, r-l)$，更新元素并减少 $\text{rem}$。
  3. 遍历结束 $\text{rem}$ 一定为 0，得到任意一组可行解。
* 该贪心等价于把“剩余增量”平均地、但**不强求完全平均**地往各位置“倒水”，保证区间约束并满足总和。

## 复杂度分析

* 单组构造只需一次线性遍历并输出：时间复杂度 $O(n)$。所有测试的 $n$ 之和不超过 $2\times 10^5$，总体可承受。
* 仅用到当前行的增量与输出数组：空间复杂度 $O(n)$（若边构造边输出，也可视为 $O(1)$ 额外空间）。

## 代码实现

### Python

```python
import sys

# 外部函数：根据 n, m, l, r 构造解；若无解返回 None
def build_array(n: int, m: int, l: int, r: int):
    smin = n * l
    smax = n * r
    if m < smin or m > smax:
        return None  # 无解
    a = [l] * n  # 先全置为下界
    rem = m - smin
    if rem == 0:
        return a
    cap = r - l  # 每个位置最多还能增加的量
    for i in range(n):
        if rem == 0:
            break
        add = cap if rem >= cap else rem  # 本位能加的增量
        a[i] += add
        rem -= add
    return a  # 此时 rem 必为 0

def main():
    data = sys.stdin.read().strip().split()
    t = int(data[0])
    idx = 1
    out_lines = []
    for _ in range(t):
        n = int(data[idx]); m = int(data[idx+1]); l = int(data[idx+2]); r = int(data[idx+3])
        idx += 4
        ans = build_array(n, m, l, r)
        if ans is None:
            out_lines.append(str(r + 1))  # 无解输出 r+1
        else:
            out_lines.append(' '.join(map(str, ans)))  # 输出任意一种可行解
    sys.stdout.write('\n'.join(out_lines))

if __name__ == "__main__":
    main()
```

### Java

```java
import java.util.*;

public class Main {
    // 外部函数：构造解，若无解返回 null
    public static long[] buildArray(int n, long m, long l, long r) {
        long smin = (long) n * l;
        long smax = (long) n * r;
        if (m < smin || m > smax) return null; // 无解

        long[] a = new long[n];
        Arrays.fill(a, l); // 先全置为下界
        long rem = m - smin;
        if (rem == 0) return a;

        long cap = r - l; // 每个位置最多还能增加的量
        for (int i = 0; i < n && rem > 0; i++) {
            long add = Math.min(rem, cap);
            a[i] += add;
            rem -= add;
        }
        return a; // 此时 rem 必为 0
    }

    public static void main(String[] args) {
        // 数据范围不大，使用 Scanner 即可
        Scanner sc = new Scanner(System.in);
        if (!sc.hasNextInt()) {
            sc.close();
            return;
        }
        int T = sc.nextInt();
        StringBuilder sb = new StringBuilder();
        for (int tc = 0; tc < T; tc++) {
            int n = sc.nextInt();
            long m = sc.nextLong();
            long l = sc.nextLong();
            long r = sc.nextLong();

            long[] ans = buildArray(n, m, l, r);
            if (ans == null) {
                sb.append(r + 1).append('\n'); // 无解输出 r+1
            } else {
                for (int i = 0; i < n; i++) {
                    if (i > 0) sb.append(' ');
                    sb.append(ans[i]);
                }
                sb.append('\n');
            }
        }
        System.out.print(sb.toString());
        sc.close();
    }
}
```

### C++

```cpp
#include <bits/stdc++.h>
using namespace std;

// 外部函数：构造解；若无解返回空向量（用 size==0 表示）
vector<long long> buildArray(int n, long long m, long long l, long long r) {
    long long smin = 1LL * n * l;
    long long smax = 1LL * n * r;
    if (m < smin || m > smax) return {}; // 无解

    vector<long long> a(n, l); // 先全置为下界
    long long rem = m - smin;
    if (rem == 0) return a;

    long long cap = r - l; // 每个位置最多还能增加的量
    for (int i = 0; i < n && rem > 0; ++i) {
        long long add = min(rem, cap);
        a[i] += add;
        rem -= add;
    }
    return a; // 此时 rem 必为 0
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int T;
    if (!(cin >> T)) return 0;
    while (T--) {
        int n;
        long long m, l, r;
        cin >> n >> m >> l >> r;

        vector<long long> ans = buildArray(n, m, l, r);
        if (ans.empty()) {
            cout << (r + 1) << '\n'; // 无解输出 r+1
        } else {
            for (int i = 0; i < n; ++i) {
                if (i) cout << ' ';
                cout << ans[i];
            }
            cout << '\n';
        }
    }
    return 0;
}
```