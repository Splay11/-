# 思路

关键观察：将区间右端点从 $i-1$ 扩展到 $i$ 时，任何以 $i$ 结尾的子区间的按位或，要么等于 $a_i$，要么是某个以前缀结尾的按位或再与 $a_i$ 做一次 $|$。并且按位或只会“开新位”不会关掉已有位，因此对于固定右端点 $i$，不同的“以 $i$ 结尾的子区间按位或结果”的种类数是有限的，至多与二进制位数相关。由于 $a_i\le 10^9$，二进制位数 $B\le 31$，所以每个位置最多保留 $O(B)$ 个不同的结果。

做法（在线去重）：

* 维护两个集合：

  * $S_{\text{prev}}$：所有“以前一个位置结尾”的按位或结果集合；
  * $S_{\text{cur}}$：所有“以当前位置 $i$ 结尾”的按位或结果集合。
* 转移：

  * 把 $a_i$ 加入 $S_{\text{cur}}$；
  * 对 $v\in S_{\text{prev}}$，把 $v|a_i$ 加入 $S_{\text{cur}}$；
* 用一个全局集合 $S_{\text{all}}$ 收集所有出现过的值；每轮把 $S_{\text{cur}}$ 并入 $S_{\text{all}}$；最后答案是 $|S_{\text{all}}|$。
* 由于每轮 $|S_{\text{prev}}|,|S_{\text{cur}}|\le O(B)$，整体时间为 $O(nB)$，这里 $B\le 31$，可过 $n$ 达到 $10^5$ 的数据。

---

# 正确性证明

用数学归纳法证明：对每个位置 $i$，$S_{\text{cur}}$ 正好等于“所有以 $i$ 结尾子区间的按位或结果”的集合。

* 基础：$i=1$ 时，唯一的以 $1$ 结尾子区间是 $[1,1]$，其按位或为 $a_1$，算法构造 $S_{\text{cur}}={a_1}$，成立。
* 归纳：假设对 $i-1$ 成立，考虑以 $i$ 结尾的任意子区间 $[l,i]$。

  * 若 $l=i$，其值为 $a_i$，被加入。
  * 若 $l<i$，则 $[l,i]$ 的值等于 $([l,i-1])|a_i$，而 $[l,i-1]$ 的值在归纳假设下必在 $S_{\text{prev}}$，因此 $([l,i-1])|a_i$ 会被加入 $S_{\text{cur}}$。
    反之，$S_{\text{cur}}$ 中每个元素要么是 $a_i$，要么是某个以 $i-1$ 结尾子区间值再与 $a_i$ 做 $|$，都对应某个以 $i$ 结尾子区间。于是二者相等。
    将所有 $i$ 的 $S_{\text{cur}}$ 并入 $S_{\text{all}}$，正是全部子区间的值集合，因此答案为 $|S_{\text{all}}|$。

# C++ 

```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    if (!(cin >> n)) return 0;
    vector<int> a(n);
    for (int i = 0; i < n; ++i) cin >> a[i];

    // S_prev: 以前一个位置结尾的按位或结果集合
    // S_cur : 以当前位置结尾的按位或结果集合
    // S_all : 全部出现过的按位或结果（全局去重）
    unordered_set<int> S_prev, S_cur, S_all;
    S_prev.reserve(64);
    S_cur.reserve(64);
    S_all.reserve((size_t)min<long long>(1e6, 1LL * n * 32));

    for (int x : a) {
        S_cur.clear();

        // 以 x 单独成段
        S_cur.insert(x);

        // 由前一轮的结果延伸到当前位置
        for (int v : S_prev) {
            S_cur.insert(v | x);
        }

        // 并入全局集合
        for (int v : S_cur) S_all.insert(v);

        // 下一轮
        S_prev = S_cur; // 规模至多约 31，拷贝成本很低
    }

    cout << S_all.size() << "\n";
    return 0;
}
```
# Python 

```python
import sys

def main():
    data = sys.stdin.read().strip().split()
    if not data:
        return
    it = iter(data)
    n = int(next(it))
    a = [int(next(it)) for _ in range(n)]

    # S_prev: 以前一个位置结尾的按位或集合
    # S_all : 全局去重集合
    S_prev = set()
    S_all = set()

    for x in a:
        # 以当前位置结尾的集合
        S_cur = {x}  # 单独成段
        for v in S_prev:
            S_cur.add(v | x)  # 延伸
        S_all |= S_cur       # 并入全局
        S_prev = S_cur       # 下一轮

    print(len(S_all))

if __name__ == "__main__":
    main()
```
# Java 

```java
import java.io.*;
import java.util.*;

public class Main {
    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String s = br.readLine();
        if (s == null || s.isEmpty()) return;
        int n = Integer.parseInt(s.trim());

        StringTokenizer st = new StringTokenizer(br.readLine());
        int[] a = new int[n];
        for (int i = 0; i < n; i++) a[i] = Integer.parseInt(st.nextToken());

        // S_prev: 以前一个位置结尾的按位或集合
        // S_all : 全局去重集合
        HashSet<Integer> S_prev = new HashSet<>();
        HashSet<Integer> S_all  = new HashSet<>();

        for (int x : a) {
            // 以当前位置结尾的集合（用临时集合，避免边遍历边修改）
            HashSet<Integer> S_cur = new HashSet<>();
            S_cur.add(x); // 单独成段
            for (int v : S_prev) {
                S_cur.add(v | x); // 延伸
            }
            S_all.addAll(S_cur);
            S_prev = S_cur; // 下一轮
        }

        System.out.println(S_all.size());
    }
}
```