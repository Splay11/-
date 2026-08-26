## 思路

**直接模拟、按段定位（无需整体拼接）**
用一个累加长度的计数器。设累计长度为$acc$，当前枚举的偶数为 $k$，其字符串为 $t$，长度为 $|t|$。从 $k=0$ 开始每次加 $2$：

* 若 $acc+|t|\ge n$，则第 $n$ 个字符就落在当前数字 $t$ 中，其在 $t$ 中的下标（从 $0$ 开始）为 $n-acc-1$，答案为 $t[n-acc-1]$；
* 否则令 $acc\leftarrow acc+|t|$，$k\leftarrow k+2$，继续。

因为只做逐段累加，不需要把前缀整串存下来，空间更省。

---

## C++ 

```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    long long n;
    if (!(cin >> n)) return 0;

    // acc 记录当前已覆盖的总字符数
    long long acc = 0;
    // 从 0 开始枚举偶数，每次 +2
    for (long long k = 0;; k += 2) {
        string t = to_string(k); // 当前偶数的字符串表示
        // 如果加上当前数字的长度就跨过或到达 n，答案在 t 内
        if (acc + (long long)t.size() >= n) {
            // 在 t 中的 0 基下标是 n - acc - 1
            cout << t[n - acc - 1] << "\n";
            break;
        }
        // 否则把 t 的长度计入累计，继续枚举下一个偶数
        acc += (long long)t.size();
    }
    return 0;
}
```

## Python 

```python
# 读取 n
n = int(input().strip())

acc = 0  # 已覆盖的总字符数
k = 0    # 当前偶数

while True:
    t = str(k)  # 当前偶数的字符串
    # 如果加上当前长度已经到达或跨过目标位置
    if acc + len(t) >= n:
        # 在 t 中的 0 基下标为 n - acc - 1
        print(t[n - acc - 1])
        break
    # 否则累加长度，跳到下一个偶数
    acc += len(t)
    k += 2
```

## Java 

```java
import java.io.BufferedReader;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String line = br.readLine();
        long n = Long.parseLong(line.trim());

        long acc = 0; // 已覆盖的总字符数
        for (long k = 0;; k += 2) { // 从 0 开始每次加 2
            String t = Long.toString(k); // 当前偶数的字符串
            // 如果当前数字的字符段覆盖到第 n 位
            if (acc + t.length() >= n) {
                // 0 基下标为 n - acc - 1
                int idx = (int)(n - acc - 1);
                System.out.println(t.charAt(idx));
                break;
            }
            // 否则继续
            acc += t.length();
        }
    }
}
```