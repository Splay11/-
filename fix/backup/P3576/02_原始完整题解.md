## 核心思路

只看模 3 的余数即可。一次操作可以把任意位置的数改成 **数组中已存在** 的某个值，因此我们最终能构造的数组，只由当前数组中出现过的“余数集合” `{0,1,2}` 决定。

记是否出现过 `0,1,2` 这三种余数。分类结论：

1. **出现了余数 0**：把所有数都改成那个余数为 0 的值，总和一定是 3 的倍数 → **Yes**。
2. **仅有余数 1**（或仅有余数 2）：只能把所有数都变成余数 1（或 2），此时总和余数为 `n*1 mod 3`（或 `2n mod 3`），
   因而 **当且仅当 `n % 3 == 0` 时为 Yes**，否则 **No**。
3. **同时有余数 1 和 2**：

   * `n = 1` 时只有一个位置，只能是 1 或 2，不可能为 0 → **No**；
   * `n ≥ 2` 时可选出某些个 1 与 2，使得 `1 的个数 ≡ 2 的个数 (mod 3)`，总和模 3 为 0（例如两两配对 1+2=3） → **Yes**。

> 小技巧：一开始可先判 `sum % 3 == 0`，直接输出 **Yes**，其余再按上面规则判断。


## 算法与复杂度

* 遍历一遍统计余数出现情况；若 `sum % 3 == 0` 直接 **Yes**；否则按上面的三条规则判断。
* **时间复杂度**：每组 `O(n)`；
* **空间复杂度**：`O(1)`。


## 参考实现

### Python

```python
# 读取输入并按规则输出
import sys

def solve():
    it = iter(sys.stdin.read().strip().split())
    t = int(next(it))
    out = []
    for _ in range(t):
        n = int(next(it))
        s = 0
        has = [False, False, False]  # 是否出现过余数0/1/2
        for _ in range(n):
            x = int(next(it))
            s += x
            has[x % 3] = True

        # 若已是好数组
        if s % 3 == 0:
            out.append("Yes")
            continue

        # 分类讨论
        if has[0]:
            out.append("Yes")
        else:
            only1 = has[1] and not has[2]
            only2 = has[2] and not has[1]
            if only1 or only2:
                out.append("Yes" if n % 3 == 0 else "No")
            else:
                # 同时有余数1和2
                out.append("No" if n == 1 else "Yes")
    print("\n".join(out))

if __name__ == "__main__":
    solve()
```

### Java

```java
import java.io.*;
import java.util.*;

/** 判定是否能把数组元素和变为3的倍数 */
public class Main {
    public static void main(String[] args) throws Exception {
        // 使用 BufferedReader + StringTokenizer，兼顾可读性与性能
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StringBuilder sb = new StringBuilder();
        StringTokenizer st;

        st = new StringTokenizer(br.readLine());
        int T = Integer.parseInt(st.nextToken());

        for (int tc = 0; tc < T; tc++) {
            // 读取 n
            st = new StringTokenizer(br.readLine());
            int n = Integer.parseInt(st.nextToken());

            // 读取数组
            st = new StringTokenizer(br.readLine());
            long sum = 0;
            boolean[] has = new boolean[3]; // 记录余数出现情况
            for (int i = 0; i < n; i++) {
                long x = Long.parseLong(st.nextToken());
                sum += x;
                has[(int)(x % 3)] = true;
            }

            // 如果已满足
            if (sum % 3 == 0) {
                sb.append("Yes\n");
                continue;
            }

            // 分类判断
            if (has[0]) {
                sb.append("Yes\n");
            } else {
                boolean only1 = has[1] && !has[2];
                boolean only2 = has[2] && !has[1];
                if (only1 || only2) {
                    sb.append(n % 3 == 0 ? "Yes\n" : "No\n");
                } else {
                    sb.append(n == 1 ? "No\n" : "Yes\n");
                }
            }
        }
        System.out.print(sb.toString());
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

    int T; 
    if (!(cin >> T)) return 0;
    while (T--) {
        int n; 
        cin >> n;
        long long sum = 0;
        bool has[3] = {false, false, false}; // 记录余数0/1/2是否出现
        for (int i = 0; i < n; ++i) {
            long long x; 
            cin >> x;
            sum += x;
            has[x % 3] = true;
        }

        // 已经是好数组
        if (sum % 3 == 0) {
            cout << "Yes\n";
            continue;
        }

        // 按三种情况讨论
        if (has[0]) {
            cout << "Yes\n";
        } else {
            bool only1 = has[1] && !has[2];
            bool only2 = has[2] && !has[1];
            if (only1 || only2) {
                cout << (n % 3 == 0 ? "Yes\n" : "No\n");
            } else {
                cout << (n == 1 ? "No\n" : "Yes\n");
            }
        }
    }
    return 0;
}
```