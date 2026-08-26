## 解题思路

从 $a$ 变到 $b$，每次可加一个 $2^i$。要操作次数最少，等价于用最少的 $2$ 的幂次凑出差值 $\textit{diff}=b-a$。

任何正整数可以唯一地表示成二进制，即 $2$ 的幂次的和。要让用的项数最少，直接用 $b-a$ 的二进制表示，所需 $2^i$ 的个数等于 $\textit{diff}$ 的二进制中 $1$ 的个数。

因此答案 $= \operatorname{popcount}(b-a)$。

## 复杂度分析

设测试数据组数为 $T$。

- 每组 popcount 是 $O(1)$，总时间复杂度 $O(T)$。
- 只需常数个变量，空间复杂度 $O(1)$。

## 代码实现

### Python

```python
import sys

def solve():
    # 快速读取所有输入
    data = sys.stdin.buffer.read().split()
    it = iter(data)
    T = int(next(it))
    out = []
    for _ in range(T):
        a = int(next(it))
        b = int(next(it))
        # 答案 = b - a 的二进制中 1 的个数
        out.append(str((b - a).bit_count()))
    # 一次性输出所有结果
    sys.stdout.write('\n'.join(out))

if __name__ == '__main__':
    solve()
```

### Java

```java
import java.io.*;
import java.util.*;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        PrintWriter out = new PrintWriter(new BufferedOutputStream(System.out));
        int T = Integer.parseInt(br.readLine());
        while (T-- > 0) {
            StringTokenizer st = new StringTokenizer(br.readLine());
            long a = Long.parseLong(st.nextToken());
            long b = Long.parseLong(st.nextToken());
            // 答案 = b - a 的二进制中 1 的个数
            out.println(Long.bitCount(b - a));
        }
        out.flush();
    }
}
```

### C++

```cpp
#include <iostream>
using namespace std;

int main() {
    // 加速 IO
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int T;
    cin >> T;
    while (T--) {
        long long a, b;
        cin >> a >> b;
        // 答案 = b - a 的二进制中 1 的个数
        cout << __builtin_popcountll((unsigned long long)(b - a)) << '\n';
    }
    return 0;
}
```
