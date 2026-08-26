# 题解

## 题面描述

给定一个长度为 $n$ 的数组 $\{a_1, a_2, \dots, a_n\}$，定义数对 $\{x, y\}$ 为一对“好数”，当且仅当 $x, y, x \oplus y$ 这三个数能够作为三条边，构成一个非退化的三角形。

求有多少对下标 $(i, j)$ 满足 $1 \le i < j \le n$，且 $\{a_i, a_j\}$ 是一对“好数”。

其中，$\oplus$ 表示按位异或操作。

- $1 \le n \le 10^5$
- $1 \le a_i \le 1000$

## 思路

1. 由于 $a_i \le 1000$，值域较小，可以先统计数组中每个数出现的频次 $cnt[v]$。
2. 枚举所有可能的值对 $(u, v)$，其中 $1 \le u \le v \le 1000$，若 $cnt[u] > 0$ 且 $cnt[v] > 0$，判断 $\{u, v\}$ 是否为“好数”。
3. 若 $u < v$ 并且是好数，则贡献 $cnt[u] \times cnt[v]$ 对；若 $u = v$，则贡献 $cnt[u] \times (cnt[u] - 1) / 2$ 对。
4. 最终累加所有贡献。

时间复杂度：值域 $\le 1000$，枚举 $O(1000^2)$，在允许范围内。


## 代码分析

- 使用大小为 $1001$ 的数组 `cnt` 统计频次。
- 双重循环枚举 $u, v$，判断三角形条件：
  - $u + v > (u \oplus v)$
  - $u + (u \oplus v) > v$
  - $v + (u \oplus v) > u$
- 根据 $u < v$ 或 $u = v$ 分别计算贡献。


# C++
```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;
    vector<int> cnt(1001, 0);
    for (int i = 0, x; i < n; i++) {
        cin >> x;
        cnt[x]++;
    }

    long long ans = 0;
    // 枚举所有可能的值对 (u, v)
    for (int u = 1; u <= 1000; u++) {
        if (cnt[u] == 0) continue;
        for (int v = u; v <= 1000; v++) {
            if (cnt[v] == 0) continue;
            int w = u ^ v;  // 异或结果
            // 三角形三边条件
            if (u + v > w && u + w > v && v + w > u) {
                if (u < v) {
                    ans += 1LL * cnt[u] * cnt[v];
                } else { // u == v
                    ans += 1LL * cnt[u] * (cnt[u] - 1) / 2;
                }
            }
        }
    }
    cout << ans << "\n";
    return 0;
}
```


# Python
```python
import sys

# 读取输入
n = int(sys.stdin.readline())
cnt = [0] * 1001
for x in map(int, sys.stdin.readline().split()):
    cnt[x] += 1

ans = 0
# 枚举所有可能的值对
for u in range(1, 1001):
    if cnt[u] == 0:
        continue
    for v in range(u, 1001):
        if cnt[v] == 0:
            continue
        w = u ^ v  # 异或
        # 判断是否能构成非退化三角形
        if u + v > w and u + w > v and v + w > u:
            if u < v:
                ans += cnt[u] * cnt[v]
            else:
                ans += cnt[u] * (cnt[u] - 1) // 2

print(ans)
```

# Java
```java
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.IOException;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int n = Integer.parseInt(br.readLine());
        int[] cnt = new int[1001];
        String[] parts = br.readLine().split(" ");
        for (String p : parts) {
            cnt[Integer.parseInt(p)]++;
        }

        long ans = 0;
        // 枚举所有可能的值对 (u, v)
        for (int u = 1; u <= 1000; u++) {
            if (cnt[u] == 0) continue;
            for (int v = u; v <= 1000; v++) {
                if (cnt[v] == 0) continue;
                int w = u ^ v;  // 异或
                // 判断三角形条件
                if (u + v > w && u + w > v && v + w > u) {
                    if (u < v) {
                        ans += (long) cnt[u] * cnt[v];
                    } else {
                        ans += (long) cnt[u] * (cnt[u] - 1) / 2;
                    }
                }
            }
        }

        System.out.println(ans);
    }
}
```