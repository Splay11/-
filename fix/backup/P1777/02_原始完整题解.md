## 解题思路

使用线性扫描和二分查找判断两条异常规则。

对于每名选手，设其通过的最大题目编号为 $p$。由于难度数组单调不降，因此该选手通过的最高难度为 $a_p$。

对于规则一，只需要检查难度不超过：

$$
a_p-500
$$

的所有题目是否都被通过。

使用二分查找找到最大的前缀长度 $t$，使得：

$$
a_i\le a_p-500,\quad 1\le i\le t
$$

也就是说，编号为 $1$ 到 $t$ 的题目都必须被该选手通过。

因为同一名选手不会重复通过同一道题，所以只需要统计其通过的题目中有多少个编号不超过 $t$：

* 如果数量等于 $t$，说明前 $t$ 道题全部通过，不违反规则一。
* 如果数量小于 $t$，说明至少漏掉一道难度不超过 $a_p-500$ 的题目，违反规则一。

这是充分且必要的。因为对于任意其他已通过题目，其难度都不超过 $a_p$，对应需要检查的低难度题目集合一定包含在前 $t$ 道题中。

对于规则二，按照通过顺序扫描数组 $C_j$。如果存在相邻两个题目编号满足：

$$
|c_{j,k+1}-c_{j,k}|\ge r
$$

则该选手成绩异常。

因此，每名选手的处理过程如下：

1. 扫描通过记录，求出最大题目编号，同时检查相邻题目编号之差。
2. 如果违反规则二，直接判定为异常。
3. 对 $a_p-500$ 进行二分查找，得到必须全部通过的前缀长度 $t$。
4. 统计通过记录中编号不超过 $t$ 的题目数量，判断是否违反规则一。

## 复杂度分析

设所有选手通过题目的总数为：

$$
S=\sum_{j=1}^{m}b_j
$$

每名选手需要进行一次线性扫描和一次二分查找，时间复杂度为：

$$
O(b_j+\log n)
$$

总时间复杂度为：

$$
O(n+S+m\log n)
$$

根据题目限制，$S\le 2\times 10^5$，该复杂度可以通过。

除难度数组和当前选手的通过记录外，不需要额外的大型数据结构，空间复杂度为：

$$
O(n+\max b_j)
$$

## 代码实现

### Python

```python
import sys
from bisect import bisect_right


def is_abnormal(a, r, passed):
    """判断一名选手的成绩是否异常"""
    max_index = 0

    # 检查规则二，同时求通过的最大题目编号
    for i in range(len(passed)):
        max_index = max(max_index, passed[i])

        if i > 0 and abs(passed[i] - passed[i - 1]) >= r:
            return True

    # 找到难度不超过最高难度减 500 的题目数量
    limit = a[max_index - 1] - 500
    prefix_length = bisect_right(a, limit)

    # 统计前 prefix_length 道题中通过了多少道
    passed_count = 0
    for problem in passed:
        if problem <= prefix_length:
            passed_count += 1

    # 前缀中的题目没有全部通过，则违反规则一
    return passed_count < prefix_length


def main():
    input = sys.stdin.buffer.readline

    n, r = map(int, input().split())
    a = list(map(int, input().split()))

    m = int(input())
    answer = 0

    for _ in range(m):
        b = int(input())
        passed = list(map(int, input().split()))

        if is_abnormal(a, r, passed):
            answer += 1

    print(answer)


if __name__ == "__main__":
    main()
```

### Java

```java
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.StringTokenizer;

public class Main {

    // 使用二分查找求小于等于 target 的元素数量
    static int upperBound(long[] a, long target) {
        int left = 0;
        int right = a.length;

        while (left < right) {
            int mid = left + (right - left) / 2;

            if (a[mid] <= target) {
                left = mid + 1;
            } else {
                right = mid;
            }
        }

        return left;
    }

    // 判断一名选手的成绩是否异常
    static boolean isAbnormal(long[] a, int r, int[] passed) {
        int maxIndex = 0;

        // 检查规则二，同时求通过的最大题目编号
        for (int i = 0; i < passed.length; i++) {
            maxIndex = Math.max(maxIndex, passed[i]);

            if (i > 0 && Math.abs(passed[i] - passed[i - 1]) >= r) {
                return true;
            }
        }

        // 求出必须全部通过的题目前缀长度
        long limit = a[maxIndex - 1] - 500;
        int prefixLength = upperBound(a, limit);

        // 统计前缀中的已通过题目数量
        int passedCount = 0;

        for (int problem : passed) {
            if (problem <= prefixLength) {
                passedCount++;
            }
        }

        // 前缀没有全部通过，则违反规则一
        return passedCount < prefixLength;
    }

    public static void main(String[] args) throws Exception {
        TokenReader reader = new TokenReader();

        int n = reader.nextInt();
        int r = reader.nextInt();

        long[] a = new long[n];
        for (int i = 0; i < n; i++) {
            a[i] = reader.nextLong();
        }

        int m = reader.nextInt();
        int answer = 0;

        for (int i = 0; i < m; i++) {
            int b = reader.nextInt();
            int[] passed = new int[b];

            for (int j = 0; j < b; j++) {
                passed[j] = reader.nextInt();
            }

            if (isAbnormal(a, r, passed)) {
                answer++;
            }
        }

        System.out.println(answer);
    }

    // 基于 BufferedReader 的普通分词输入
    static class TokenReader {
        private final BufferedReader reader =
                new BufferedReader(new InputStreamReader(System.in));
        private StringTokenizer tokenizer;

        String next() throws IOException {
            while (tokenizer == null || !tokenizer.hasMoreTokens()) {
                tokenizer = new StringTokenizer(reader.readLine());
            }
            return tokenizer.nextToken();
        }

        int nextInt() throws IOException {
            return Integer.parseInt(next());
        }

        long nextLong() throws IOException {
            return Long.parseLong(next());
        }
    }
}
```

### C++

```cpp
#include <iostream>
#include <vector>
#include <algorithm>
#include <cstdlib>
using namespace std;

// 判断一名选手的成绩是否异常
bool isAbnormal(const vector<long long>& a, int r,
                const vector<int>& passed) {
    int maxIndex = 0;

    // 检查规则二，同时求通过的最大题目编号
    for (int i = 0; i < static_cast<int>(passed.size()); i++) {
        maxIndex = max(maxIndex, passed[i]);

        if (i > 0 && abs(passed[i] - passed[i - 1]) >= r) {
            return true;
        }
    }

    // 求出难度不超过最高难度减 500 的题目数量
    long long limit = a[maxIndex - 1] - 500;
    int prefixLength =
        upper_bound(a.begin(), a.end(), limit) - a.begin();

    // 统计前缀中的已通过题目数量
    int passedCount = 0;

    for (int problem : passed) {
        if (problem <= prefixLength) {
            passedCount++;
        }
    }

    // 前缀没有全部通过，则违反规则一
    return passedCount < prefixLength;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, r;
    cin >> n >> r;

    vector<long long> a(n);
    for (int i = 0; i < n; i++) {
        cin >> a[i];
    }

    int m;
    cin >> m;

    int answer = 0;

    for (int i = 0; i < m; i++) {
        int b;
        cin >> b;

        vector<int> passed(b);
        for (int j = 0; j < b; j++) {
            cin >> passed[j];
        }

        if (isAbnormal(a, r, passed)) {
            answer++;
        }
    }

    cout << answer << '\n';

    return 0;
}
```