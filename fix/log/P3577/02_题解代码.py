## 解题思路

### 关键观察

数组元素均为正数。这样就可以用**滑动窗口(双指针)**维护当前区间的和：

* 右指针 `r` 向右扩张，把 `a[r]` 加入当前和 `s`；
* 若 `s > k`，不断右移左指针 `l` 并减去 `a[l]`，直到 `s ≤ k`；
* 每次满足 `s ≤ k` 时，用 `r-l+1` 更新答案。

由于每个元素最多被左右指针各访问一次，整体是线性算法。


### 复杂度

* 时间复杂度：`O(n)`（每个元素进出窗口各一次）。
* 空间复杂度：`O(1)`。

## 代码实现

### Python

```python
import sys

def solve():
    data = list(map(int, sys.stdin.read().strip().split()))
    if not data:
        return
    it = iter(data)
    n = next(it)
    k = next(it)
    a = [next(it) for _ in range(n)]

    l = 0           # 左指针
    s = 0           # 当前窗口和
    ans = 0
    for r in range(n):
        s += a[r]                   # 扩张右端
        while s > k and l <= r:     # 超过容量则收缩左端
            s -= a[l]
            l += 1
        if s <= k:                  # 合法窗口更新答案
            ans = max(ans, r - l + 1)
    print(ans)

if __name__ == "__main__":
    solve()
```

### Java

```java
import java.io.*;
import java.util.*;

/** 求和不超过k的最长连续子段长度（滑动窗口） */
public class Main {
    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StringTokenizer st;

        // 读取 n 和 k
        st = new StringTokenizer(br.readLine());
        int n = Integer.parseInt(st.nextToken());
        long k = Long.parseLong(st.nextToken());

        // 读取数组
        st = new StringTokenizer(br.readLine());
        long[] a = new long[n];
        for (int i = 0; i < n; i++) a[i] = Long.parseLong(st.nextToken());

        int l = 0;          // 左指针
        long sum = 0;       // 当前窗口和
        int ans = 0;

        for (int r = 0; r < n; r++) {
            sum += a[r];                // 扩张右端点
            while (sum > k && l <= r) { // 和超过k，缩小左端点
                sum -= a[l++];
            }
            if (sum <= k) {             // 当前窗口合法，尝试更新答案
                ans = Math.max(ans, r - l + 1);
            }
        }
        System.out.println(ans);
    }
}
```

### C++

```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n; long long k;
    if (!(cin >> n >> k)) return 0;
    vector<long long> a(n);
    for (int i = 0; i < n; ++i) cin >> a[i];

    int l = 0;                 // 左指针
    long long s = 0;           // 当前窗口和
    int ans = 0;

    for (int r = 0; r < n; ++r) {
        s += a[r];                         // 加入右端元素
        while (s > k && l <= r) {          // 超容量则移动左端
            s -= a[l++];
        }
        if (s <= k)                        // 合法时更新答案
            ans = max(ans, r - l + 1);
    }
    cout << ans << "\n";
    return 0;
}
```