## 解题思路

失败的试切没有任何收益，却会让刀具耐久 $s$ 永久减 $1$，因此最优策略里不会去做注定失败的试切。问题转化为：选出尽可能多的工件，并安排试切顺序，使得第 $j$ 次成功时当前耐久仍不低于该工件硬度，即：

$$
s - (j - 1) \ge h_i
$$

越硬的工件越应更早试切。于是将硬度从大到小排序，再依次判断能否成功。

设当前已成功 $cnt$ 次，则下一次试切时的耐久为 $s - cnt$。对当前硬度 $h_i$：

* 若 $s - cnt \ge h_i$，则成功，$cnt$ 加 $1$；
* 否则该工件过硬，且后面工件硬度只会更小，跳过它是合理的。

贪心正确性：先处理更硬的工件。若它能成功，优先成功它不会劣于先做更软的；若它不能成功，之后耐久只会更低，它也不可能再成功，可直接跳过。最终 $cnt$ 即为最多成功次数。

## 复杂度分析

设单组工件数为 $m$。排序 $O(m\log m)$，再线性扫描 $O(m)$，单组为 $O(m\log m)$。全体用例 $m$ 合计不超过 $2\times 10^5$，总时间 $O(\sum m\log m)$，空间 $O(m)$。

## 代码实现

### Python

```python
q = int(input())
for _ in range(q):
    m, s = map(int, input().split())
    h = list(map(int, input().split()))
    # 硬度从大到小：优先尝试更硬的工件
    h.sort(reverse=True)
    cnt = 0
    for x in h:
        # 已成功 cnt 次，当前耐久为 s - cnt
        if s - cnt >= x:
            cnt += 1
    print(cnt)
```

### Java

```java
import java.io.*;
import java.util.*;

public class Main {
    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int q = Integer.parseInt(br.readLine().trim());
        StringBuilder out = new StringBuilder();
        while (q-- > 0) {
            StringTokenizer st = new StringTokenizer(br.readLine());
            int m = Integer.parseInt(st.nextToken());
            long s = Long.parseLong(st.nextToken());
            Integer[] h = new Integer[m];
            st = new StringTokenizer(br.readLine());
            for (int i = 0; i < m; i++) h[i] = Integer.parseInt(st.nextToken());
            // 硬度从大到小：优先尝试更硬的工件
            Arrays.sort(h, Collections.reverseOrder());
            int cnt = 0;
            for (int x : h) {
                // 已成功 cnt 次，当前耐久为 s - cnt
                if (s - cnt >= x) cnt++;
            }
            out.append(cnt).append('\n');
        }
        System.out.print(out);
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
    int q;
    cin >> q;
    while (q--) {
        int m;
        long long s;
        cin >> m >> s;
        vector<long long> h(m);
        for (int i = 0; i < m; ++i) cin >> h[i];
        // 硬度从大到小：优先尝试更硬的工件
        sort(h.begin(), h.end(), greater<long long>());
        int cnt = 0;
        for (long long x : h) {
            // 已成功 cnt 次，当前耐久为 s - cnt
            if (s - cnt >= x) ++cnt;
        }
        cout << cnt << '\n';
    }
    return 0;
}
```
