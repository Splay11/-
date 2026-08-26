## 解题思路

1. 题意要求的是最长的连续子数组 $[l,r]$，使得区间内每一对相邻元素的差的绝对值都不超过阈值 $d$。等价于：在序列上从左到右走，只要 $|a_{i+1}-a_i|\le d$ 就可以把 $a_{i+1}$ 接在当前段末尾，否则必须从 $a_{i+1}$ 重新开始一段。
2. 因为“能否延伸”只与**上一项**有关，具有无后效性，不需要动态规划或数据结构，单次线性扫描即可。
3. 维护当前段长度 `cur`：若 $|a_i-a_{i-1}|\le d$ 则 `cur += 1`，否则 `cur = 1`（新段至少包含当前点）。答案为扫描过程中 `cur` 的最大值。注意 $n\ge 1$ 时答案至少为 $1$。
4. 多组测试数据下，题目保证所有组的 $n$ 之和不超过 $2\times 10^5$，因此对每组做 $O(n)$ 扫描，总时间 $O(\sum n)$，可以通过。

## 复杂度分析

* 时间复杂度：$O(\sum n)$，与所有测试点的 $n$ 之和线性相关。
* 空间复杂度：$O(n)$，存放当前组的数组 $a$（也可边读边算，降至 $O(1)$ 额外空间，但实现上保留数组更清晰）。

## 代码实现

### Python

```python
import sys


def max_stable_len(n, d, a):
    # 从左到右扫描：相邻差不超过 d 则延伸当前段，否则重置为 1（单点段）
    ans = 1
    cur = 1
    for i in range(1, n):
        if abs(a[i] - a[i - 1]) <= d:
            cur += 1
        else:
            cur = 1
        if cur > ans:
            ans = cur
    return ans


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(newline="\n")
    t = int(input())
    for _ in range(t):
        n_d = input().split()
        n = int(n_d[0])
        d = int(n_d[1])
        a = list(map(int, input().split()))
        print(max_stable_len(n, d, a))


if __name__ == "__main__":
    main()
```

### Java

```java
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.util.StringTokenizer;

public class Main {
    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int T = Integer.parseInt(br.readLine().trim());
        StringBuilder out = new StringBuilder();
        while (T-- > 0) {
            StringTokenizer st = new StringTokenizer(br.readLine());
            int n = Integer.parseInt(st.nextToken());
            long d = Long.parseLong(st.nextToken());
            long[] a = new long[n];
            st = new StringTokenizer(br.readLine());
            for (int i = 0; i < n; ++i) {
                a[i] = Long.parseLong(st.nextToken());
            }
            int ans = 1;
            int cur = 1;
            for (int i = 1; i < n; ++i) {
                long diff = a[i] - a[i - 1];
                if (diff < 0) {
                    diff = -diff;
                }
                if (diff <= d) {
                    ++cur;
                } else {
                    cur = 1;
                }
                if (cur > ans) {
                    ans = cur;
                }
            }
            out.append(ans).append('\n');
        }
        System.out.print(out.toString());
    }
}
```

### C++

```cpp
#include <bits/stdc++.h>
using namespace std;

using int64 = long long;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int T;
    cin >> T;
    while (T--) {
        int n;
        int64 d;
        cin >> n >> d;
        vector<int64> a(n);
        for (int i = 0; i < n; ++i) {
            cin >> a[i];
        }
        int ans = 1;
        int cur = 1;
        for (int i = 1; i < n; ++i) {
            int64 diff = a[i] - a[i - 1];
            if (diff < 0) {
                diff = -diff;
            }
            if (diff <= d) {
                ++cur;
            } else {
                cur = 1;
            }
            if (cur > ans) {
                ans = cur;
            }
        }
        cout << ans << '\n';
    }
    return 0;
}
```