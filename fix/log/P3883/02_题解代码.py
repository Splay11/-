## 解题思路

* 比赛为单败淘汰，按当前顺序两两配对，胜者保持相对顺序进入下一轮。设队伍 1 的能力值为 `s1`。
* 第 r 轮（从 1 开始）结束后，区间 `[1, 2^r]` 的冠军一定是该区间内能力值最大的队伍（因为每一场都强者胜出且数值互不相同）。
* 因此，“队伍 1 能赢下前 r 轮” 等价于 `s1 > max(s2, s3, …, s_{2^r})`。
* 于是胜场数就是满足上述不等式的最大 r。
* 实现：一次线性扫描维护前缀最大值 `m = max(s2..si)`，当扫描到位置 `i` 使得 `i+1` 为 2 的幂（即 `2,4,8,...`）时检查 `s1 > m`。若为真则胜场加一并继续，否则立即停止。`n=1` 时无比赛，答案为 0。

## 复杂度分析

* 每个测试用例只需线性扫描一遍数组，并在若干个幂次边界做常数判断。
* 时间复杂度：`O(n)`；空间复杂度：`O(1)`（除输入存储外）。

## 代码实现

### Python

```python
# 题面功能封装在函数中，主函数只负责输入输出
import sys

def wins_count(arr):
    """返回队伍1的胜场数"""
    n = len(arr)
    if n == 1:
        return 0
    s1 = arr[0]
    mx = -1  # 维护 s2..si 的最大值
    ans = 0
    need = 2  # 当前需要检查的边界：2,4,8,...
    for i in range(1, n):
        if arr[i] > mx:
            mx = arr[i]
        if i + 1 == need:    # 到达 2 的幂次边界
            if s1 > mx:
                ans += 1
                need <<= 1   # 转到下一个边界
            else:
                break        # 首次不满足即停止
    return ans

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    it = iter(data)
    T = next(it)
    out = []
    for _ in range(T):
        n = next(it)
        arr = [next(it) for __ in range(n)]
        out.append(str(wins_count(arr)))
    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    main()
```

### Java

```java
// 类名固定为 Main，使用快速输入以适应数据范围
import java.io.*;
import java.util.*;

public class Main {

    // 功能函数：计算队伍1胜场数
    static int winsCount(int[] a) {
        int n = a.length;
        if (n == 1) return 0;
        int s1 = a[0];
        int mx = Integer.MIN_VALUE; // 维护 s2..si 的最大值
        int ans = 0;
        int need = 2;               // 边界：2,4,8,...
        for (int i = 1; i < n; i++) {
            if (a[i] > mx) mx = a[i];
            if (i + 1 == need) {
                if (s1 > mx) {
                    ans++;
                    need <<= 1;
                } else break;
            }
        }
        return ans;
    }

    // 为了效率自写快读
    static class FastScanner {
        private final InputStream in;
        private final byte[] buffer = new byte[1 << 16];
        private int ptr = 0, len = 0;
        FastScanner(InputStream is) { in = is; }
        private int read() throws IOException {
            if (ptr >= len) {
                len = in.read(buffer);
                ptr = 0;
                if (len <= 0) return -1;
            }
            return buffer[ptr++];
        }
        int nextInt() throws IOException {
            int c, sgn = 1, x = 0;
            do { c = read(); } while (c <= ' '); // 跳过空白
            if (c == '-') { sgn = -1; c = read(); }
            while (c > ' ') {
                x = x * 10 + (c - '0');
                c = read();
            }
            return x * sgn;
        }
    }

    public static void main(String[] args) throws Exception {
        FastScanner fs = new FastScanner(System.in);
        StringBuilder sb = new StringBuilder();
        int T = fs.nextInt();
        while (T-- > 0) {
            int n = fs.nextInt();
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = fs.nextInt();
            sb.append(winsCount(a)).append('\n');
        }
        System.out.print(sb.toString());
    }
}
```

### C++

```cpp
// ACM 风格：主函数处理输入输出，功能放在外部函数
#include <bits/stdc++.h>
using namespace std;

// 功能函数：返回队伍1的胜场数
int winsCount(const vector<int>& a) {
    int n = (int)a.size();
    if (n == 1) return 0;
    int s1 = a[0];
    int mx = INT_MIN; // 维护 s2..si 的最大值
    int ans = 0;
    int need = 2;     // 边界：2,4,8,...
    for (int i = 1; i < n; ++i) {
        if (a[i] > mx) mx = a[i];
        if (i + 1 == need) {
            if (s1 > mx) {
                ++ans;
                need <<= 1;
            } else break;
        }
    }
    return ans;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int T;
    if (!(cin >> T)) return 0;
    while (T--) {
        int n; 
        cin >> n;
        vector<int> a(n);
        for (int i = 0; i < n; ++i) cin >> a[i];
        cout << winsCount(a) << "\n";
    }
    return 0;
}
```