## 解题思路

任务可区分，目标是统计排列中存在前缀和恰好为 $60$ 的个数。总和已固定为 $180$，因此后半段自动为 $120$。

枚举所有子集 $S$：若 $\sum S=60$，则把 $S$ 排在前半段、其余排在后半段，贡献 $|S|! \times (n-|S|)!$。所有这样的子集贡献之和即为答案。输入不合法或没有这样的子集时输出 $0$。

样例 $60,60,60$ 中任意一项单独构成和为 $60$ 的前缀，共 $3!=6$ 种排列。

## 复杂度分析

- 时间复杂度：$O(n\cdot 2^n)$（$n$ 很小）。
- 空间复杂度：$O(n)$。

## 代码实现

### Python

```python
import math
import sys

def solve():
    data = list(map(int, sys.stdin.read().split()))
    if not data:
        print(0)
        return
    n = data[0]
    m = data[1:1 + n]
    if len(m) != n or n <= 0 or sum(m) != 180:
        print(0)
        return
    ans = 0
    for mask in range(1 << n):
        s = 0
        cnt = 0
        for i in range(n):
            if mask >> i & 1:
                s += m[i]
                cnt += 1
        if s == 60:
            ans += math.factorial(cnt) * math.factorial(n - cnt)
    print(ans)

solve()
```

### Java

```java
import java.util.*;
public class Main {
    static long fact(int x) {
        long r = 1;
        for (int i = 2; i <= x; i++) r *= i;
        return r;
    }
    public static void main(String[] args) {
        Scanner cin = new Scanner(System.in);
        if (!cin.hasNextInt()) {
            System.out.println(0);
            return;
        }
        int n = cin.nextInt();
        int[] m = new int[n];
        int sum = 0;
        for (int i = 0; i < n; i++) {
            m[i] = cin.nextInt();
            sum += m[i];
        }
        if (n <= 0 || sum != 180) {
            System.out.println(0);
            return;
        }
        long ans = 0;
        for (int mask = 0; mask < (1 << n); mask++) {
            int s = 0, cnt = 0;
            for (int i = 0; i < n; i++) {
                if (((mask >> i) & 1) == 1) {
                    s += m[i];
                    cnt++;
                }
            }
            if (s == 60) ans += fact(cnt) * fact(n - cnt);
        }
        System.out.println(ans);
    }
}
```

### C++

```cpp
#include <bits/stdc++.h>
using namespace std;
long long fact(int x) {
    long long r = 1;
    for (int i = 2; i <= x; ++i) r *= i;
    return r;
}
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    if (!(cin >> n)) {
        cout << 0 << '\n';
        return 0;
    }
    vector<int> m(n);
    int sum = 0;
    for (int i = 0; i < n; ++i) {
        cin >> m[i];
        sum += m[i];
    }
    if (n <= 0 || sum != 180) {
        cout << 0 << '\n';
        return 0;
    }
    long long ans = 0;
    for (int mask = 0; mask < (1 << n); ++mask) {
        int s = 0, cnt = 0;
        for (int i = 0; i < n; ++i) if (mask >> i & 1) {
            s += m[i];
            ++cnt;
        }
        if (s == 60) ans += fact(cnt) * fact(n - cnt);
    }
    cout << ans << '\n';
    return 0;
}
```
