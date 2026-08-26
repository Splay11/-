## 核心观察

### 统一“扣减 i 并截到 0”的含义

当编号为 `i` 的人到来时，对所有已成年者的操作等价于：
把他们的当前宝石 `x` 统一替换为 `max(0, x - i)`，而 i 的总收入就是 `sum min(i, x)`。

### “捐献者”视角（关键）

按成年时间升序记为 `p1, p2, …, pn`（对应原编号 `id[t]`），并定义：

* `I[t] = id[t]`（即到来者的“索取额度”）
* `P[t] = I[1] + … + I[t]`（前缀和）

对某个已成年者 `r`，在他成年时拥有的“可被未来人索取”的总额记为 `S[r]`。之后每个更晚到来者 `t > r` 会依次索取 `I[t]`。因此：

* `r` 会**从 t = r+1 开始**，连续向每个事件支付 **完整的 `I[t]`**，直到某次事件 `t*` 首次使得
  `I[r+1] + … + I[t*] >= S[r]`；在 `t*` 这次只支付**剩余的那一小部分**，之后为 0。
* 若直到最后也不够“榨干”他（`P[n] - P[r] < S[r]`），那么他在最终还剩 `S[r] - (P[n] - P[r])`。

于是，**对每个到来事件 `t` 的收入**可拆为两部分：

1. 仍“有余力”的捐献者人数 × `I[t]`
2. 正好在这次 `t` 被榨干的捐献者的“尾款”之和

这就可以用**差分+二分**来线性维护“仍有余力的人数”和“尾款加总”。

## 算法步骤

1. 按 `b` 升序重排，得到时间序 `t = 1..n` 对应的原编号 `id[t]`，以及 `I[t] = id[t]`、`A[t] = a[id[t]]`。
2. 计算 `P[t] = Σ_{k=1..t} I[k]`。
3. 维护两个数组（均对 `t` 索引）：

   * `add[t]`：差分数组，前缀和得到某时刻“仍能支付完整 `I[t]` 的捐献者数量”
   * `part[t]`：在 `t` 时刻收到的“尾款”加总
4. 依次处理 `t = 1..n`：

   * 用 `add` 的前缀和得到 `active`（当前仍有余力的捐献者数）。
   * 本次 `t` 的收入 `gain = I[t] * active + part[t]`。
   * 得到 `S[t] = A[t] + gain`（t 在成为捐献者时的“可被未来索取”的总额）。
   * 设 `remainNeed = P[n] - P[t]`（未来所有人的总索取额）。

     * 若 `S[t] == 0`：他以后贡献为 0，跳过更新。
     * 若 `S[t] <= remainNeed`：用二分在区间 `(t, n]` 找到最小 `u` 使 `P[u] - P[t] >= S[t]`。
       这意味着他在 `t+1..u-1` 都能付满，在 `u` 付“尾款”
       `tail = S[t] - (P[u-1] - P[t])`。
       用差分做：`add[t+1] += 1, add[u] -= 1, part[u] += tail`。
     * 否则：他直到最后都付不完：
       `add[t+1] += 1, add[n+1] -= 1`（`t+1..n` 次都能付满），没有尾款。
5. 全部处理完后，每个 `t` 的最终剩余为
   `ans_t = max(0, S[t] - (P[n] - P[t]))`，再按原编号放回。

### 正确性要点

* 差分 `add` 精确表示“还没被榨干的捐献者区间覆盖次数”，从而 `I[t]*active` 正是满额部分；
* “第一次越界”即 `u` 的二分定位，`part[u]` 累加尾款；
* 每位捐献者的总出资被唯一地分配到一个区间 `t+1..u-1` 的满额与一次 `u` 的尾款（或直到 `n` 都满额），因此合计不重不漏。

### 复杂度分析

* 排序 O(n log n)；每个 `t` 一次二分 O(log n)，其余为 O(1) 差分更新。
* 总时间复杂度 **O(n log n)**，空间 **O(n)**。满足 `n ≤ 2×10^5`。


## 代码

### Python

```python
import sys

def main():
    data = list(map(int, sys.stdin.read().strip().split()))
    it = iter(data)
    n = next(it)
    a = [0] + [next(it) for _ in range(n)]  # 1-based
    b = [0] + [next(it) for _ in range(n)]  # 1-based

    # 按成年时间升序得到时间序 id[t]
    ids = list(range(1, n + 1))
    ids.sort(key=lambda x: b[x])

    I = [0] * (n + 1)      # I[t] = 原编号（索取额度）
    A = [0] * (n + 1)      # A[t] = 对应的 a
    pos2id = [0] * (n + 1) # t -> 原编号
    for t in range(1, n + 1):
        idx = ids[t - 1]
        I[t] = idx
        A[t] = a[idx]
        pos2id[t] = idx

    # 前缀和 P
    P = [0] * (n + 1)
    for t in range(1, n + 1):
        P[t] = P[t - 1] + I[t]

    add = [0] * (n + 3)   # 差分：活跃捐献者计数
    part = [0] * (n + 3)  # 尾款加总
    active = 0
    S = [0] * (n + 1)     # 每个 t 在成为捐献者时的“可被未来索取”的总额

    for t in range(1, n + 1):
        # 更新活跃人数
        active += add[t]
        # 本次收入 = 满额部分 + 尾款部分
        gain = I[t] * active + part[t]
        S[t] = A[t] + gain

        if S[t] == 0:
            continue

        remain_need = P[n] - P[t]
        if S[t] <= remain_need:
            # 二分找到首次越界的 u
            lo, hi = t + 1, n
            u = n + 1
            while lo <= hi:
                mid = (lo + hi) // 2
                if P[mid] - P[t] >= S[t]:
                    u = mid
                    hi = mid - 1
                else:
                    lo = mid + 1
            # 区间 t+1..u-1 满额，u 处尾款
            add[t + 1] += 1
            add[u] -= 1
            tail = S[t] - (P[u - 1] - P[t])
            part[u] += tail
        else:
            # 直到最后都付不完：t+1..n 都满额
            add[t + 1] += 1
            add[n + 1] -= 1

    # 计算最终剩余，并按原编号输出
    ans = [0] * (n + 1)
    for t in range(1, n + 1):
        remain = S[t] - (P[n] - P[t])
        if remain < 0:
            remain = 0
        ans[pos2id[t]] = remain

    print(' '.join(str(ans[i]) for i in range(1, n + 1)))

if __name__ == "__main__":
    main()
```

### C++

```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    if (!(cin >> n)) return 0;
    vector<long long> a(n + 1), b(n + 1);
    for (int i = 1; i <= n; ++i) cin >> a[i];
    for (int i = 1; i <= n; ++i) cin >> b[i];

    // 按成年时间升序
    vector<int> ids(n);
    iota(ids.begin(), ids.end(), 1);
    sort(ids.begin(), ids.end(), [&](int x, int y){ return b[x] < b[y]; });

    vector<long long> I(n + 1), A(n + 1), P(n + 1, 0);
    vector<int> pos2id(n + 1);
    for (int t = 1; t <= n; ++t) {
        int idx = ids[t - 1];
        I[t] = idx;       // 索取额度 = 原编号
        A[t] = a[idx];
        pos2id[t] = idx;
        P[t] = P[t - 1] + I[t];
    }

    vector<long long> add(n + 3, 0), part(n + 3, 0), S(n + 1, 0);
    long long active = 0;

    for (int t = 1; t <= n; ++t) {
        active += add[t];                       // 活跃捐献者人数
        long long gain = I[t] * active + part[t]; // 本次收入
        S[t] = A[t] + gain;

        if (S[t] == 0) continue;

        long long remainNeed = P[n] - P[t];
        if (S[t] <= remainNeed) {
            // 二分首个 u 使 P[u]-P[t] >= S[t]
            int lo = t + 1, hi = n, u = n + 1;
            while (lo <= hi) {
                int mid = (lo + hi) >> 1;
                if (P[mid] - P[t] >= S[t]) { u = mid; hi = mid - 1; }
                else lo = mid + 1;
            }
            add[t + 1] += 1;
            add[u] -= 1;
            long long tail = S[t] - (P[u - 1] - P[t]); // 尾款
            part[u] += tail;
        } else {
            add[t + 1] += 1;
            add[n + 1] -= 1;
        }
    }

    vector<long long> ans(n + 1, 0);
    for (int t = 1; t <= n; ++t) {
        long long remain = S[t] - (P[n] - P[t]);
        if (remain < 0) remain = 0;
        ans[pos2id[t]] = remain;
    }

    for (int i = 1; i <= n; ++i) {
        if (i > 1) cout << ' ';
        cout << ans[i];
    }
    cout << '\n';
    return 0;
}
```

### Java

```java
import java.io.*;
import java.util.*;

public class Main {
    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in), 1 << 20);
        StringTokenizer st;

        int n = Integer.parseInt(br.readLine().trim());
        long[] a = new long[n + 1];
        long[] b = new long[n + 1];

        st = new StringTokenizer(br.readLine());
        for (int i = 1; i <= n; i++) a[i] = Long.parseLong(st.nextToken());

        st = new StringTokenizer(br.readLine());
        for (int i = 1; i <= n; i++) b[i] = Long.parseLong(st.nextToken());

        // 按成年时间排序得到时间序
        Integer[] ids = new Integer[n];
        for (int i = 0; i < n; i++) ids[i] = i + 1;
        Arrays.sort(ids, Comparator.comparingLong(x -> b[x]));

        long[] I = new long[n + 1];
        long[] A = new long[n + 1];
        int[] pos2id = new int[n + 1];
        long[] P = new long[n + 1];
        for (int t = 1; t <= n; t++) {
            int idx = ids[t - 1];
            I[t] = idx;          // 索取额度 = 原编号
            A[t] = a[idx];
            pos2id[t] = idx;
            P[t] = P[t - 1] + I[t];
        }

        long[] add = new long[n + 3];   // 差分：活跃捐献者人数
        long[] part = new long[n + 3];  // 尾款加总
        long[] S = new long[n + 1];     // 每个 t 的可被未来索取总额
        long active = 0;

        for (int t = 1; t <= n; t++) {
            active += add[t];                        // 当前活跃捐献者数
            long gain = I[t] * active + part[t];    // 本次收入
            S[t] = A[t] + gain;

            if (S[t] == 0) continue;

            long remainNeed = P[n] - P[t];
            if (S[t] <= remainNeed) {
                // 二分查找首次越界 u：P[u]-P[t] >= S[t]
                int lo = t + 1, hi = n, u = n + 1;
                while (lo <= hi) {
                    int mid = (lo + hi) >>> 1;
                    if (P[mid] - P[t] >= S[t]) { u = mid; hi = mid - 1; }
                    else lo = mid + 1;
                }
                add[t + 1] += 1;
                add[u] -= 1;
                long tail = S[t] - (P[u - 1] - P[t]); // 尾款
                part[u] += tail;
            } else {
                add[t + 1] += 1;
                add[n + 1] -= 1;
            }
        }

        long[] ans = new long[n + 1];
        for (int t = 1; t <= n; t++) {
            long remain = S[t] - (P[n] - P[t]);
            if (remain < 0) remain = 0;
            ans[pos2id[t]] = remain;
        }

        StringBuilder sb = new StringBuilder();
        for (int i = 1; i <= n; i++) {
            if (i > 1) sb.append(' ');
            sb.append(ans[i]);
        }
        System.out.println(sb.toString());
    }
}
```