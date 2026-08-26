## 解题思路

一次操作可以交换 $a_i$ 和 $a_{i+k}$，所以一个位置上的数只能在和它下标同余的那一组里移动。

也就是说，数组会被分成若干组：

* 第 $1, 1+k, 1+2k, \dots$ 个位置是一组
* 第 $2, 2+k, 2+2k, \dots$ 个位置是一组
* $\dots$
* 第 $k$ 组同理

同一组内可以通过多次交换实现任意排列。因为这一组本质上是一条链，相邻交换可以得到该组元素的任意顺序。

题目要求最终数组字典序最大。
那么对于每一组，应该使用贪心策略：

* 把这一组里的所有数取出来
* 按从大到小排序
* 再按该组位置从前到后依次放回去

这样能保证每个位置都尽量大，从而得到整体字典序最大的数组。

这里用到的核心算法是：

* 按下标对 $k$ 分组
* 对每组做降序排序
* 贪心回填

## 复杂度分析

设数组长度为 $n$。

把元素按模 $k$ 分组后，每个元素只会进入某一组一次，回填一次。所有组排序的总元素个数也是 $n$，因此总时间复杂度为：

$$
O(n \log n)
$$

空间复杂度为：

$$
O(n)
$$

这个复杂度对于题目的数据范围是合适的。

## 代码实现

### Python

```python
import sys


# 求字典序最大的数组
def solve_case(n, k, arr):
    groups = [[] for _ in range(k)]

    # 按下标分组，这里使用 0 下标，按 i % k 分组
    for i in range(n):
        groups[i % k].append(arr[i])

    # 每组降序排序
    for i in range(k):
        groups[i].sort(reverse=True)

    # 记录每组当前取到哪个元素
    idx = [0] * k
    res = [0] * n

    # 按原位置顺序回填，每次放当前组最大的剩余元素
    for i in range(n):
        g = i % k
        res[i] = groups[g][idx[g]]
        idx[g] += 1

    return res


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    t = data[0]
    p = 1
    ans = []

    for _ in range(t):
        n = data[p]
        k = data[p + 1]
        p += 2
        arr = data[p:p + n]
        p += n

        res = solve_case(n, k, arr)
        ans.append(" ".join(map(str, res)))

    sys.stdout.write("\n".join(ans))


if __name__ == "__main__":
    main()
```

### Java

```java
import java.io.*;
import java.util.*;


public class Main {

    // 求字典序最大的数组
    static int[] solveCase(int n, int k, int[] arr) {
        ArrayList<Integer>[] groups = new ArrayList[k];
        for (int i = 0; i < k; i++) {
            groups[i] = new ArrayList<>();
        }

        // 按下标分组
        for (int i = 0; i < n; i++) {
            groups[i % k].add(arr[i]);
        }

        // 每组降序排序
        for (int i = 0; i < k; i++) {
            groups[i].sort(Collections.reverseOrder());
        }

        int[] idx = new int[k];
        int[] res = new int[n];

        // 按位置顺序回填
        for (int i = 0; i < n; i++) {
            int g = i % k;
            res[i] = groups[g].get(idx[g]);
            idx[g]++;
        }

        return res;
    }

    public static void main(String[] args) throws Exception {
        FastScanner fs = new FastScanner(System.in);
        StringBuilder sb = new StringBuilder();

        int t = fs.nextInt();
        while (t-- > 0) {
            int n = fs.nextInt();
            int k = fs.nextInt();

            int[] arr = new int[n];
            for (int i = 0; i < n; i++) {
                arr[i] = fs.nextInt();
            }

            int[] res = solveCase(n, k, arr);

            for (int i = 0; i < n; i++) {
                if (i > 0) sb.append(' ');
                sb.append(res[i]);
            }
            sb.append('\n');
        }

        System.out.print(sb.toString());
    }

    // 由于数据较大，使用较快的输入方式
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
                if (len <= 0) return -1;
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


// 求字典序最大的数组
vector<long long> solve_case(int n, int k, const vector<long long>& arr) {
    vector<vector<long long>> groups(k);

    // 按下标分组
    for (int i = 0; i < n; i++) {
        groups[i % k].push_back(arr[i]);
    }

    // 每组降序排序
    for (int i = 0; i < k; i++) {
        sort(groups[i].begin(), groups[i].end(), greater<long long>());
    }

    vector<int> idx(k, 0);
    vector<long long> res(n);

    // 按位置顺序回填
    for (int i = 0; i < n; i++) {
        int g = i % k;
        res[i] = groups[g][idx[g]];
        idx[g]++;
    }

    return res;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int T;
    cin >> T;

    while (T--) {
        int n, k;
        cin >> n >> k;

        vector<long long> arr(n);
        for (int i = 0; i < n; i++) {
            cin >> arr[i];
        }

        vector<long long> res = solve_case(n, k, arr);

        for (int i = 0; i < n; i++) {
            if (i) cout << ' ';
            cout << res[i];
        }
        cout << '\n';
    }

    return 0;
}
```