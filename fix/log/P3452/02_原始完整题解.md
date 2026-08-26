## 思路

核心贪心：在从左到右构造答案时，每一步决定放当前剩余数中 **最大** 或 **最小** 的一个。

* 设当前可用的数是区间 ${L,L+1,\dots,R}$（初始 $L=1,R=n$）。
* 若把 $R$ 放在当前位置，它会与之后剩下的 $R-L$ 个更小的数各形成 $1$ 个逆序对，因此本步能额外贡献 $R-L$ 个逆序对。
* 若把 $L$ 放在当前位置，本步不增加新的逆序对（因为后面剩下的都不小于 $L$）。

于是每一步贪心选择：

* 如果 $k\ge R-L$，就放 $R$，并令 $k\leftarrow k-(R-L)$，再令 $R\leftarrow R-1$；
* 否则放 $L$，令 $L\leftarrow L+1$。
* 重复 $n$ 次即可。

### 正确性说明（简述）

在某一步，当前位置最多只能“买到” $R-L$ 个逆序对（把当前最大 $R$ 放到最前面）。当 $k\ge R-L$ 时，**一定可以**并且**应该**立即买满这 $R-L$ 个，因为把 $R$留到更后面并不会产生更多的逆序对收益；当 $k< R-L$ 时，则应放 $L$，把“购买逆序对”的机会留给后面若干次，用未来若干次各付出 $1$ 的方式累计凑到恰好 $k$。因此该贪心在每一步都最优，最终能精确达到目标 $k$。

## C++ 

```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    long long n, k;
    if (!(cin >> n >> k)) return 0;

    vector<long long> ans;
    ans.reserve(n);

    long long L = 1, R = n; // 当前可用数字区间 [L, R]
    for (long long i = 0; i < n; ++i) {
        // 若把 R 放在当前位置，可以贡献 (R - L) 个逆序对
        if (k >= (R - L)) {
            ans.push_back(R); // 放最大值
            k -= (R - L);     // 购买 (R - L) 个逆序对
            --R;              // 缩小右端
        } else {
            ans.push_back(L); // 放最小值，本步不增加逆序对
            ++L;              // 缩小左端
        }
    }

    // 输出答案
    for (int i = 0; i < (int)ans.size(); ++i) {
        if (i) cout << ' ';
        cout << ans[i];
    }
    cout << '\n';
    return 0;
}
```
## Python 

```python
import sys

def main():
    data = sys.stdin.read().strip().split()
    if not data:
        return
    n = int(data[0])
    k = int(data[1])

    # 双指针：当前可用的最小和最大
    L, R = 1, n
    ans = []

    for _ in range(n):
        # 若把 R 放在当前位置，可贡献 (R - L) 个逆序对
        if k >= (R - L):
            ans.append(R)   # 放最大值，尽量买满这一位能买到的逆序对
            k -= (R - L)
            R -= 1
        else:
            ans.append(L)   # 放最小值，本步不增加逆序对
            L += 1

    print(' '.join(map(str, ans)))

if __name__ == "__main__":
    main()
```
## Java 

```java
import java.io.*;
import java.util.*;

public class Main {
    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String[] tk = br.readLine().trim().split("\\s+");
        int n = Integer.parseInt(tk[0]);
        long k = Long.parseLong(tk[1]); // k 可能较大，使用 long

        List<Integer> ans = new ArrayList<>(n);
        int L = 1, R = n; // 当前可用数字区间 [L, R]

        for (int i = 0; i < n; i++) {
            // 若把 R 放在当前位置，可贡献 (R - L) 个逆序对
            if (k >= (long)(R - L)) {
                ans.add(R);             // 放最大值
                k -= (R - L);           // 购买 (R - L) 个逆序对
                R--;                    // 缩小右端
            } else {
                ans.add(L);             // 放最小值
                L++;                    // 缩小左端
            }
        }

        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < ans.size(); i++) {
            if (i > 0) sb.append(' ');
            sb.append(ans.get(i));
        }
        System.out.println(sb.toString());
    }
}
```