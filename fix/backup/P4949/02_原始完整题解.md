## 解题思路

构造 $1\sim m$ 的排列，使逆序对恰好为 $t$。

最大逆序对数为 $m(m-1)/2$，题面保证 $t$ 合法。

从大到小贪心：设剩余数字为 $1,\dots,s$。若把最大值 $s$ 放在当前位置，会对后面 $s-1$ 个数各产生一个逆序对。

* 若当前剩余目标 $t \ge s-1$，则放下 $s$，并令 $t \leftarrow t-(s-1)$；
* 否则在剩余 $1,\dots,s$ 上直接构造

$$
[t+1,\ 1,2,\dots,t,\ t+2,\dots,s]。
$$

其中开头的 $t+1$ 恰好贡献 $t$ 个逆序对，其余递增无新逆序对。

## 复杂度分析

每个数入答案一次，单组时间 $O(m)$，空间 $O(m)$。

全体 $\sum m \le 2\times 10^5$，可通过。

## 代码实现

### Python

```python
q = int(input())
for _ in range(q):
    m, t = map(int, input().split())
    out = []
    # 剩余数字 1..s，s 从 m 降到 1
    s = m
    while s >= 1:
        if t >= s - 1 and s > 1:
            # 放下最大值，贡献 s-1 个逆序对
            out.append(s)
            t -= s - 1
            s -= 1
        else:
            # 剩余段一次性构造出恰好 t 个逆序对
            if t == 0:
                out.extend(range(1, s + 1))
            else:
                out.append(t + 1)
                out.extend(range(1, t + 1))
                out.extend(range(t + 2, s + 1))
            break
    print(*out)
```

### Java

```java
import java.io.*;
import java.util.*;

public class Main {
    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int q = Integer.parseInt(br.readLine().trim());
        StringBuilder sb = new StringBuilder();
        while (q-- > 0) {
            StringTokenizer st = new StringTokenizer(br.readLine());
            int m = Integer.parseInt(st.nextToken());
            long t = Long.parseLong(st.nextToken());
            ArrayList<Integer> out = new ArrayList<>();
            int s = m;
            while (s >= 1) {
                if (t >= s - 1 && s > 1) {
                    out.add(s); // 放最大值
                    t -= (s - 1);
                    s--;
                } else {
                    if (t == 0) {
                        for (int i = 1; i <= s; i++) out.add(i);
                    } else {
                        out.add((int) t + 1);
                        for (int i = 1; i <= t; i++) out.add(i);
                        for (int i = (int) t + 2; i <= s; i++) out.add(i);
                    }
                    break;
                }
            }
            for (int i = 0; i < out.size(); i++) {
                if (i > 0) sb.append(' ');
                sb.append(out.get(i));
            }
            sb.append('\n');
        }
        System.out.print(sb);
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
        long long t;
        cin >> m >> t;
        vector<int> out;
        int s = m;
        while (s >= 1) {
            if (t >= s - 1 && s > 1) {
                out.push_back(s); // 放最大值，贡献 s-1
                t -= s - 1;
                --s;
            } else {
                if (t == 0) {
                    for (int i = 1; i <= s; ++i) out.push_back(i);
                } else {
                    out.push_back((int)t + 1);
                    for (int i = 1; i <= t; ++i) out.push_back(i);
                    for (int i = (int)t + 2; i <= s; ++i) out.push_back(i);
                }
                break;
            }
        }
        for (int i = 0; i < (int)out.size(); ++i) {
            if (i) cout << ' ';
            cout << out[i];
        }
        cout << '\n';
    }
    return 0;
}
```
