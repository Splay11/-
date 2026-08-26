## 解题思路

使用动态规划。

设 $dp[i]$ 表示当前剩下前 $i$ 个魔法段时，将所有魔法段剪掉所需的最少操作次数。

对于前 $i$ 个魔法段，记录：

* 魔法硬度最大值最靠后的下标 $maxPos$；
* 魔法硬度最小值最靠后的下标 $minPos$。

选择最大硬度的魔法段后，会剪掉从 $maxPos$ 到 $i$ 的所有魔法段，剩下前 $maxPos-1$ 个魔法段。

选择最小硬度的魔法段后，会剪掉从 $minPos$ 到 $i$ 的所有魔法段，剩下前 $minPos-1$ 个魔法段。

因此状态转移为：

$$
dp[i]=1+\min(dp[maxPos-1],dp[minPos-1])
$$

从左到右扫描数组。由于存在多个最大值或最小值时必须选择距离开头最远的一个，所以：

* 当前值大于等于最大值时，更新 $maxPos$；
* 当前值小于等于最小值时，更新 $minPos$。

最终答案为 $dp[n]$。

## 复杂度分析

每个魔法段只处理一次，时间复杂度为 $O(n)$。

使用数组保存所有动态规划状态，空间复杂度为 $O(n)$。

## 代码实现

### Python

```python
import sys


def min_operations(a):
    n = len(a)
    dp = [0] * (n + 1)

    max_value = a[0]
    min_value = a[0]
    max_pos = 1
    min_pos = 1

    for i in range(1, n + 1):
        value = a[i - 1]

        # 使用大于等于，保证记录最靠后的最大值
        if value >= max_value:
            max_value = value
            max_pos = i

        # 使用小于等于，保证记录最靠后的最小值
        if value <= min_value:
            min_value = value
            min_pos = i

        # 分别选择最大值或最小值进行状态转移
        dp[i] = 1 + min(dp[max_pos - 1], dp[min_pos - 1])

    return dp[n]


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    index = 0

    t = data[index]
    index += 1
    answers = []

    for _ in range(t):
        n = data[index]
        index += 1

        a = data[index:index + n]
        index += n

        answers.append(str(min_operations(a)))

    print("\n".join(answers))


if __name__ == "__main__":
    main()
```

### Java

```java
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.StreamTokenizer;

public class Main {

    public static int minOperations(int[] a) {
        int n = a.length;
        int[] dp = new int[n + 1];

        int maxValue = a[0];
        int minValue = a[0];
        int maxPos = 1;
        int minPos = 1;

        for (int i = 1; i <= n; i++) {
            int value = a[i - 1];

            // 使用大于等于，保证记录最靠后的最大值
            if (value >= maxValue) {
                maxValue = value;
                maxPos = i;
            }

            // 使用小于等于，保证记录最靠后的最小值
            if (value <= minValue) {
                minValue = value;
                minPos = i;
            }

            // 分别选择最大值或最小值进行状态转移
            dp[i] = 1 + Math.min(dp[maxPos - 1], dp[minPos - 1]);
        }

        return dp[n];
    }

    public static void main(String[] args) throws Exception {
        StreamTokenizer input = new StreamTokenizer(
                new BufferedReader(new InputStreamReader(System.in))
        );

        input.nextToken();
        int t = (int) input.nval;

        StringBuilder answer = new StringBuilder();

        for (int test = 0; test < t; test++) {
            input.nextToken();
            int n = (int) input.nval;

            int[] a = new int[n];

            for (int i = 0; i < n; i++) {
                input.nextToken();
                a[i] = (int) input.nval;
            }

            answer.append(minOperations(a)).append('\n');
        }

        System.out.print(answer);
    }
}
```

### C++

```cpp
#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;


int minOperations(const vector<int>& a) {
    int n = a.size();
    vector<int> dp(n + 1, 0);

    int maxValue = a[0];
    int minValue = a[0];
    int maxPos = 1;
    int minPos = 1;

    for (int i = 1; i <= n; i++) {
        int value = a[i - 1];

        // 使用大于等于，保证记录最靠后的最大值
        if (value >= maxValue) {
            maxValue = value;
            maxPos = i;
        }

        // 使用小于等于，保证记录最靠后的最小值
        if (value <= minValue) {
            minValue = value;
            minPos = i;
        }

        // 分别选择最大值或最小值进行状态转移
        dp[i] = 1 + min(dp[maxPos - 1], dp[minPos - 1]);
    }

    return dp[n];
}


int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int t;
    cin >> t;

    while (t--) {
        int n;
        cin >> n;

        vector<int> a(n);
        for (int i = 0; i < n; i++) {
            cin >> a[i];
        }

        cout << minOperations(a) << '\n';
    }

    return 0;
}
```