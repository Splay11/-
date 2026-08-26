## 解题思路

枚举所有可能的方向 $(d_x,d_y,d_z)$。

其中 $d_x,d_y,d_z \in {-1,0,1}$，且不能同时为 $0$，一共有 $26$ 个方向。

对于某个方向：

如果某一维的步长为 $1$，起点这一维只能是 $0$；

如果某一维的步长为 $-1$，起点这一维只能是 $n-1$；

如果某一维的步长为 $0$，起点这一维可以是 $0$ 到 $n-1$ 的任意值。

这样可以保证从起点走 $n$ 步时，始终在立方体内部。

对每个合法起点，计算这条长度为 $n$ 的直线权值和，并更新最大值即可。

该方法本质是枚举方向和起点，属于暴力枚举，但由于合法直线数量只有 $O(n^2)$ 级别，每条线长度为 $n$，因此总复杂度可以接受。

## 复杂度分析

时间复杂度：$O(n^3)$。

空间复杂度：$O(n^3)$，用于存储整个立方体网格。

## 代码实现

### Python

```python
import sys

def max_line_sum(n, a):
    ans = -10**30

    # 枚举所有方向
    for dx in (-1, 0, 1):
        for dy in (-1, 0, 1):
            for dz in (-1, 0, 1):
                if dx == 0 and dy == 0 and dz == 0:
                    continue

                # 根据方向确定合法起点范围
                xs = [0] if dx == 1 else ([n - 1] if dx == -1 else range(n))
                ys = [0] if dy == 1 else ([n - 1] if dy == -1 else range(n))
                zs = [0] if dz == 1 else ([n - 1] if dz == -1 else range(n))

                # 枚举所有合法起点
                for x0 in xs:
                    for y0 in ys:
                        for z0 in zs:
                            s = 0
                            x, y, z = x0, y0, z0

                            # 沿当前方向走 n 个格子
                            for _ in range(n):
                                s += a[x][y][z]
                                x += dx
                                y += dy
                                z += dz

                            ans = max(ans, s)

    return ans

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    n = data[0]
    a = [[[0] * n for _ in range(n)] for _ in range(n)]

    idx = 1
    # 输入顺序：按 z 层，每层 n 行，每行 n 个数
    for z in range(n):
        for x in range(n):
            for y in range(n):
                a[x][y][z] = data[idx]
                idx += 1

    print(max_line_sum(n, a))

if __name__ == "__main__":
    main()
```

### Java

```java
import java.io.*;
import java.util.*;

public class Main {
    // 计算所有合法直线中的最大权值和
    static long maxLineSum(int n, int[][][] a) {
        long ans = Long.MIN_VALUE;

        // 枚举所有方向
        for (int dx = -1; dx <= 1; dx++) {
            for (int dy = -1; dy <= 1; dy++) {
                for (int dz = -1; dz <= 1; dz++) {
                    if (dx == 0 && dy == 0 && dz == 0) {
                        continue;
                    }

                    // 根据方向确定起点范围
                    int xs = (dx == 0) ? 0 : (dx == 1 ? 0 : n - 1);
                    int xe = (dx == 0) ? n - 1 : xs;
                    int ys = (dy == 0) ? 0 : (dy == 1 ? 0 : n - 1);
                    int ye = (dy == 0) ? n - 1 : ys;
                    int zs = (dz == 0) ? 0 : (dz == 1 ? 0 : n - 1);
                    int ze = (dz == 0) ? n - 1 : zs;

                    // 枚举所有合法起点
                    for (int x0 = xs; x0 <= xe; x0++) {
                        for (int y0 = ys; y0 <= ye; y0++) {
                            for (int z0 = zs; z0 <= ze; z0++) {
                                long sum = 0;
                                int x = x0, y = y0, z = z0;

                                // 沿当前方向走 n 个格子
                                for (int k = 0; k < n; k++) {
                                    sum += a[x][y][z];
                                    x += dx;
                                    y += dy;
                                    z += dz;
                                }

                                if (sum > ans) {
                                    ans = sum;
                                }
                            }
                        }
                    }
                }
            }
        }

        return ans;
    }

    public static void main(String[] args) throws Exception {
        FastScanner fs = new FastScanner(System.in);
        int n = fs.nextInt();

        int[][][] a = new int[n][n][n];

        // 输入顺序：按 z 层，每层 n 行，每行 n 个数
        for (int z = 0; z < n; z++) {
            for (int x = 0; x < n; x++) {
                for (int y = 0; y < n; y++) {
                    a[x][y][z] = fs.nextInt();
                }
            }
        }

        System.out.println(maxLineSum(n, a));
    }

    // 数据量较大，使用简单快读
    static class FastScanner {
        private final InputStream in;
        private final byte[] buffer = new byte[1 << 16];
        private int ptr = 0, len = 0;

        FastScanner(InputStream is) {
            in = is;
        }

        private int read() throws IOException {
            if (ptr >= len) {
                len = in.read(buffer);
                ptr = 0;
                if (len <= 0) {
                    return -1;
                }
            }
            return buffer[ptr++];
        }

        int nextInt() throws IOException {
            int c;
            do {
                c = read();
            } while (c <= ' ');

            int sign = 1;
            if (c == '-') {
                sign = -1;
                c = read();
            }

            int val = 0;
            while (c > ' ') {
                val = val * 10 + c - '0';
                c = read();
            }

            return val * sign;
        }
    }
}
```

### C++

```cpp
#include <bits/stdc++.h>
using namespace std;

// 计算所有合法直线中的最大权值和
long long maxLineSum(int n, vector<vector<vector<int>>>& a) {
    long long ans = LLONG_MIN;

    // 枚举所有方向
    for (int dx = -1; dx <= 1; dx++) {
        for (int dy = -1; dy <= 1; dy++) {
            for (int dz = -1; dz <= 1; dz++) {
                if (dx == 0 && dy == 0 && dz == 0) {
                    continue;
                }

                // 根据方向确定起点范围
                int xs = (dx == 0) ? 0 : (dx == 1 ? 0 : n - 1);
                int xe = (dx == 0) ? n - 1 : xs;
                int ys = (dy == 0) ? 0 : (dy == 1 ? 0 : n - 1);
                int ye = (dy == 0) ? n - 1 : ys;
                int zs = (dz == 0) ? 0 : (dz == 1 ? 0 : n - 1);
                int ze = (dz == 0) ? n - 1 : zs;

                // 枚举所有合法起点
                for (int x0 = xs; x0 <= xe; x0++) {
                    for (int y0 = ys; y0 <= ye; y0++) {
                        for (int z0 = zs; z0 <= ze; z0++) {
                            long long sum = 0;
                            int x = x0, y = y0, z = z0;

                            // 沿当前方向走 n 个格子
                            for (int k = 0; k < n; k++) {
                                sum += a[x][y][z];
                                x += dx;
                                y += dy;
                                z += dz;
                            }

                            ans = max(ans, sum);
                        }
                    }
                }
            }
        }
    }

    return ans;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    cin >> n;

    vector<vector<vector<int>>> a(n, vector<vector<int>>(n, vector<int>(n)));

    // 输入顺序：按 z 层，每层 n 行，每行 n 个数
    for (int z = 0; z < n; z++) {
        for (int x = 0; x < n; x++) {
            for (int y = 0; y < n; y++) {
                cin >> a[x][y][z];
            }
        }
    }

    cout << maxLineSum(n, a) << '\n';

    return 0;
}
```