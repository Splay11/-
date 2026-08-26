## 解题思路

给定一个固定的交替串 `s=1010...`（长度为 `n`），每次操作任选一个相邻位置 `i`，若 `s[i] != s[i+1]` 就能删除这两位并得到积分 `a[i]`。题目特别强调**数组 `a` 在整个过程中不变**，每次选择第 `i` 位都获得同一个 `a[i]`，可以重复选择同一个下标（只要当时还满足 `i < len(s)`）。

### 关键性质

1. **始终可选**：交替串删除任意相邻一对后仍是交替串，因此每一步对所有 `1..len(s)-1` 的 `i` 都满足 `s[i] != s[i+1]`。
2. **步数固定**：每次删去 2 个字符，直到长度 ≤ 1，因此操作次数固定为
   `m = ⌊n/2⌋`。
3. **可选区间单调缩小**：第 1 步可选下标为 `1..(n-1)`，第 2 步为 `1..(n-3)`，……，第 `k` 步为
   `1..(n-1-2(k-1))`。注意数组 `a` 固定不变，且**允许重复选同一下标**。

于是问题变为：进行 `m` 次选择，第 `k` 次只能从前缀 `1..r_k`（`r_k = n-1-2(k-1)`）里取一个值 `a[i]`，并求所有步次得分之和的最大/最小值。

### 贪心 + 前缀极值

因为后续允许的集合始终是**当前集合的子集**（前缀长度减少 2），当前不取前缀最优只会让之后更难弥补。因此每一步的最优选择是：

* 最大值：在当下允许前缀里选**前缀最大值**；
* 最小值：在当下允许前缀里选**前缀最小值**。

令

* `preMax[i] = max(a1..ai)`
* `preMin[i] = min(a1..ai)`

则答案为

* `Max = Σ preMax[r]`，`r` 依次取 `n-1, n-3, ..., (n%2==0 ? 1 : 2)`
* `Min = Σ preMin[r]`，同样的 `r` 序列。

## 复杂度分析

* 预处理前缀最大/最小：`O(n)`
* 枚举需要的 `m = ⌊n/2⌋` 个前缀点：`O(m)`
  整体 `O(n)` 时间，`O(n)` 额外空间。对所有测试用例满足 `∑n ≤ 2×10^6` 的限制。

## 代码实现

### Python

```python
import sys

def solve_case(n, a):
    # 计算前缀最大与前缀最小
    preMax = [0] * (n)
    preMin = [0] * (n)
    cur_max = -10**19
    cur_min = 10**19
    for i in range(1, n):  # i 对应前缀长度 i，使用 a[i-1]
        v = a[i - 1]
        if v > cur_max:
            cur_max = v
        if v < cur_min:
            cur_min = v
        preMax[i] = cur_max
        preMin[i] = cur_min

    # 累加 r = n-1, n-3, ...
    max_sum = 0
    min_sum = 0
    r = n - 1
    while r >= 1:
        max_sum += preMax[r]
        min_sum += preMin[r]
        r -= 2
    return max_sum, min_sum

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    it = iter(data)
    T = next(it)
    out_lines = []
    for _ in range(T):
        n = next(it)
        a = [next(it) for _ in range(n - 1)]
        mx, mn = solve_case(n, a)
        out_lines.append(f"{mx} {mn}")
    sys.stdout.write("\n".join(out_lines))

if __name__ == "__main__":
    main()
```

### Java

```java
import java.io.*;
import java.util.*;

/* ACM 风格：主函数处理输入输出，核心逻辑写成外部静态函数，类名 Main */
public class Main {

    // 计算一个用例的答案：返回 [maxSum, minSum]
    static long[] solveCase(int n, int[] a) {
        long[] preMax = new long[n];
        long[] preMin = new long[n];
        long curMax = Long.MIN_VALUE / 4;
        long curMin = Long.MAX_VALUE / 4;
        for (int i = 1; i <= n - 1; i++) {           // 前缀长度 i
            int v = a[i - 1];
            if (v > curMax) curMax = v;              // 维护前缀最大
            if (v < curMin) curMin = v;              // 维护前缀最小
            preMax[i] = curMax;
            preMin[i] = curMin;
        }
        long maxSum = 0, minSum = 0;
        for (int r = n - 1; r >= 1; r -= 2) {        // 依次取 n-1, n-3, ...
            maxSum += preMax[r];
            minSum += preMin[r];
        }
        return new long[]{maxSum, minSum};
    }

    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StringBuilder out = new StringBuilder();
        int T = Integer.parseInt(br.readLine().trim());
        for (int tc = 0; tc < T; tc++) {
            int n = Integer.parseInt(br.readLine().trim());
            int need = n - 1;
            int[] a = new int[need];
            int idx = 0;
            // 按空白分隔读取 n-1 个整数
            while (idx < need) {
                String line = br.readLine();
                if (line == null || line.isEmpty()) continue;
                String[] parts = line.trim().split("\\s+");
                for (String s : parts) {
                    if (s.isEmpty()) continue;
                    a[idx++] = Integer.parseInt(s);
                    if (idx == need) break;
                }
            }
            long[] ans = solveCase(n, a);
            out.append(ans[0]).append(' ').append(ans[1]).append('\n');
        }
        System.out.print(out.toString());
    }
}
```

### C++

```cpp
#include <bits/stdc++.h>
using namespace std;

/* 计算一个用例的答案：返回 {maxSum, minSum} */
pair<long long, long long> solve_case(int n, const vector<int>& a) {
    vector<long long> preMax(n, LLONG_MIN / 4);
    vector<long long> preMin(n, LLONG_MAX / 4);

    long long curMax = LLONG_MIN / 4;
    long long curMin = LLONG_MAX / 4;
    // 前缀极值
    for (int i = 1; i <= n - 1; ++i) {
        int v = a[i - 1];
        if (v > curMax) curMax = v;   // 维护前缀最大
        if (v < curMin) curMin = v;   // 维护前缀最小
        preMax[i] = curMax;
        preMin[i] = curMin;
    }

    long long maxSum = 0, minSum = 0;
    // r 依次为 n-1, n-3, ...
    for (int r = n - 1; r >= 1; r -= 2) {
        maxSum += preMax[r];
        minSum += preMin[r];
    }
    return {maxSum, minSum};
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int T; 
    if (!(cin >> T)) return 0;
    while (T--) {
        int n; 
        cin >> n;
        vector<int> a(n - 1);
        for (int i = 0; i < n - 1; ++i) cin >> a[i];

        auto ans = solve_case(n, a);
        cout << ans.first << ' ' << ans.second << "\n";
    }
    return 0;
}
```