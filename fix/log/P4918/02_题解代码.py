## 解题思路

设导向串 $g$ 中 `L` 的个数为 $cnt$。

结论：起点 $s \le cnt$ 时最终从左侧出界；$s > cnt$ 时从右侧出界。答案为

$$
\underbrace{LL\cdots L}_{cnt\text{ 个}}\underbrace{RR\cdots R}_{L-cnt\text{ 个}}
$$

证明要点：已访问工位始终构成连续区间 $[l,r]$，当前停在 $p$。区间内除 $p$ 外，`L` 个数为 $s-l$，`R` 个数为 $r-s$。

- 左侧出界时当前为 `L` 且 $l=1$，故 $s \le cnt$；
- 右侧出界时当前为 `R` 且 $r=L$，可得 $s > cnt$。

## 复杂度分析

每组统计 `L` 并构造答案，时间 $O(L)$，空间 $O(L)$（输出串）；全体 $\sum L \le 2\times 10^5$。

## 代码实现

### Python

```python
import sys

def solve(L, g):
  cnt = sum(1 for c in g if c == 'L')
  return 'L' * cnt + 'R' * (L - cnt)

q = int(input())
out = []
for _ in range(q):
  L = int(input())
  g = input().strip()
  out.append(solve(L, g))
sys.stdout.write('\n'.join(out))
```

### Java

```java
import java.io.*;

public class Main {
  static String solve(int L, String g) {
    int cnt = 0;
    for (int i = 0; i < L; i++) if (g.charAt(i) == 'L') cnt++;
    return "L".repeat(cnt) + "R".repeat(L - cnt);
  }

  public static void main(String[] args) throws Exception {
    BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
    int q = Integer.parseInt(br.readLine().trim());
    StringBuilder out = new StringBuilder();
    while (q-- > 0) {
      int L = Integer.parseInt(br.readLine().trim());
      String g = br.readLine().trim();
      out.append(solve(L, g)).append('\n');
    }
    System.out.print(out);
  }
}
```

### C++

```cpp
#include <bits/stdc++.h>
using namespace std;

string solve(int L, const string& g) {
    int cnt = 0;
    for (char c : g) if (c == 'L') ++cnt;
    return string(cnt, 'L') + string(L - cnt, 'R');
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int q; cin >> q;
    while (q--) {
        int L; string g;
        cin >> L >> g;
        cout << solve(L, g) << '\n';
    }
    return 0;
}
```