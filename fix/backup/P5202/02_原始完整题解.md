## 解题思路

使用前缀和与双指针滑动窗口。

将原序列复制一遍，得到长度至少为 $2n-1$ 的序列。定义前缀余数：

$$
P_0=0
$$

$$
P_i=\left(\sum_{j=1}^{i}a_{(j-1)\bmod n+1}\right)\bmod M
$$

对于起点 $s$，第 $t$ 步的轨迹值为：

$$
S_t=(P_{s+t-1}-P_{s-1})\bmod M
$$

对于任意两个步数 $x$ 和 $y$：

$$
S_x=S_y
$$

当且仅当：

$$
P_{s+x-1}=P_{s+y-1}
$$

因为两边同时减去了相同的 $P_{s-1}$。

因此，起点 $s$ 的游走长度 $L_s$，等于序列：

$$
P_s,P_{s+1},\dots,P_{s+n-1}
$$

从左端开始的最长无重复前缀长度。

使用双指针维护一个无重复窗口 $[left,right]$：

* 集合中保存 $P_{left},P_{left+1},\dots,P_{right}$。
* 对于每个 $left$，不断向右扩展 $right$。
* 扩展时要求 $right+1\le left+n-1$，保证游走长度不超过 $n$。
* 如果下一个前缀余数已经存在于集合中，则不能继续扩展。
* 此时：

$$
L_{left}=right-left+1
$$

* 统计答案后，将 $P_{left}$ 从集合中删除，再处理下一个起点。

双指针中的 $right$ 始终单调向右移动，因此所有位置只会加入和删除集合常数次。

答案最大可能达到 $n^2$，需要使用 $64$ 位整数保存。

## 复杂度分析

对于每组测试数据：

* 构造双倍前缀余数的时间复杂度为 $O(n)$。
* 双指针扫描的时间复杂度为 $O(n)$。
* 总时间复杂度为 $O(n)$。
* 前缀数组和集合的空间复杂度为 $O(n)$。

由于所有测试数据的 $n$ 之和不超过 $2\times 10^5$，该复杂度可以通过。

## 代码实现

### Python

```python
import sys


def solve_case(n, m, a):
    # prefix[i] 表示双倍序列前 i 个数之和对 m 取模
    prefix = [0] * (2 * n)

    # 实际只需要计算到下标 2n-1
    for i in range(1, 2 * n):
        prefix[i] = (prefix[i - 1] + a[(i - 1) % n]) % m

    seen = set()
    right = 0
    answer = 0

    # 枚举每一个起点
    for left in range(1, n + 1):
        limit = left + n - 1

        # 保证窗口内余数互不相同，并且长度不超过 n
        while right + 1 <= limit and prefix[right + 1] not in seen:
            right += 1
            seen.add(prefix[right])

        # 当前窗口长度就是该起点的游走长度
        answer += right - left + 1

        # 左端点右移，删除离开窗口的余数
        if left <= right:
            seen.remove(prefix[left])

    return answer


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    index = 0

    t = data[index]
    index += 1

    result = []

    for _ in range(t):
        n = data[index]
        m = data[index + 1]
        index += 2

        a = data[index:index + n]
        index += n

        result.append(str(solve_case(n, m, a)))

    sys.stdout.write("\n".join(result))


if __name__ == "__main__":
    main()
```

### Java

```java
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.StreamTokenizer;
import java.util.HashSet;

public class Main {

    static long solveCase(int n, int m, long[] a) {
        int[] prefix = new int[2 * n];

        // 构造双倍序列的前缀余数
        // 实际只需要计算到下标 2n-1
        for (int i = 1; i < 2 * n; i++) {
            long value = a[(i - 1) % n] % m;

            // Java 对负数取模可能得到负数，需要调整
            if (value < 0) {
                value += m;
            }

            prefix[i] = (int) ((prefix[i - 1] + value) % m);
        }

        HashSet<Integer> seen = new HashSet<>();
        int right = 0;
        long answer = 0;

        // 枚举每一个起点
        for (int left = 1; left <= n; left++) {
            int limit = left + n - 1;

            // 保证窗口内余数互不相同，并且长度不超过 n
            while (right + 1 <= limit
                    && !seen.contains(prefix[right + 1])) {
                right++;
                seen.add(prefix[right]);
            }

            // 当前窗口长度就是该起点的游走长度
            answer += right - left + 1L;

            // 左端点右移，删除离开窗口的余数
            if (left <= right) {
                seen.remove(prefix[left]);
            }
        }

        return answer;
    }

    public static void main(String[] args) throws Exception {
        StreamTokenizer input = new StreamTokenizer(
                new BufferedReader(new InputStreamReader(System.in))
        );

        input.nextToken();
        int t = (int) input.nval;

        StringBuilder output = new StringBuilder();

        for (int testCase = 0; testCase < t; testCase++) {
            input.nextToken();
            int n = (int) input.nval;

            input.nextToken();
            int m = (int) input.nval;

            long[] a = new long[n];

            for (int i = 0; i < n; i++) {
                input.nextToken();
                a[i] = (long) input.nval;
            }

            output.append(solveCase(n, m, a)).append('\n');
        }

        System.out.print(output);
    }
}
```

### C++

```cpp
#include <iostream>
#include <vector>
#include <unordered_set>
using namespace std;

long long solveCase(int n, int m, const vector<long long>& a) {
    vector<int> prefix(2 * n, 0);

    // 构造双倍序列的前缀余数
    // 实际只需要计算到下标 2n-1
    for (int i = 1; i < 2 * n; i++) {
        long long value = a[(i - 1) % n] % m;

        // C++ 对负数取模可能得到负数，需要调整
        if (value < 0) {
            value += m;
        }

        prefix[i] = (prefix[i - 1] + value) % m;
    }

    unordered_set<int> seen;
    seen.reserve(2 * n + 1);

    int right = 0;
    long long answer = 0;

    // 枚举每一个起点
    for (int left = 1; left <= n; left++) {
        int limit = left + n - 1;

        // 保证窗口内余数互不相同，并且长度不超过 n
        while (right + 1 <= limit
               && seen.find(prefix[right + 1]) == seen.end()) {
            right++;
            seen.insert(prefix[right]);
        }

        // 当前窗口长度就是该起点的游走长度
        answer += right - left + 1LL;

        // 左端点右移，删除离开窗口的余数
        if (left <= right) {
            seen.erase(prefix[left]);
        }
    }

    return answer;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int T;
    cin >> T;

    while (T--) {
        int n, m;
        cin >> n >> m;

        vector<long long> a(n);

        for (int i = 0; i < n; i++) {
            cin >> a[i];
        }

        cout << solveCase(n, m, a) << '\n';
    }

    return 0;
}
```