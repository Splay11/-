## 解题思路

使用贪心算法，从第 $1$ 盏灯依次处理到第 $n$ 盏灯。

设 $x_i$ 表示第 $i$ 个开关是否被按下：

* 第 $1$ 盏灯只受开关 $1$ 影响，因此必须满足：

$$
x_1=a_1
$$

* 对于第 $i$ 盏灯，它会受到开关 $i-1$ 和开关 $i$ 的影响，因此必须满足：

$$
a_i \oplus x_{i-1} \oplus x_i=0
$$

所以：

$$
x_i=a_i \oplus x_{i-1}
$$

从左向右计算每个 $x_i$，统计其中值为 $1$ 的数量即可。

这种选择是唯一的：处理第 $i$ 盏灯时，之后只有第 $i$ 个开关还能改变它的状态，因此是否按下第 $i$ 个开关已经被强制确定。故得到的操作次数一定是最少操作次数。

该过程也可以理解为计算数组的前缀异或，并统计前缀异或为 $1$ 的位置数量。

## 复杂度分析

每组数据只需要遍历一次数组：

* 时间复杂度：$O(n)$
* 额外空间复杂度：$O(1)$

所有测试数据的 $n$ 之和不超过 $2\times 10^5$，复杂度满足要求。

## 代码实现

### Python

```python
import sys


def min_operations(a):
    answer = 0
    previous = 0

    for state in a:
        # 当前开关是否需要按下
        current = state ^ previous
        answer += current
        previous = current

    return answer


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    index = 0
    test_count = data[index]
    index += 1
    answers = []

    for _ in range(test_count):
        n = data[index]
        index += 1

        # 输入当前测试数据
        a = data[index:index + n]
        index += n

        answers.append(str(min_operations(a)))

    sys.stdout.write("\n".join(answers))


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
        int answer = 0;
        int previous = 0;

        for (int state : a) {
            // 当前开关是否需要按下
            int current = state ^ previous;
            answer += current;
            previous = current;
        }

        return answer;
    }

    public static void main(String[] args) throws Exception {
        StreamTokenizer input =
                new StreamTokenizer(new BufferedReader(new InputStreamReader(System.in)));

        input.nextToken();
        int testCount = (int) input.nval;
        StringBuilder output = new StringBuilder();

        for (int test = 0; test < testCount; test++) {
            input.nextToken();
            int n = (int) input.nval;
            int[] a = new int[n];

            // 输入当前测试数据
            for (int i = 0; i < n; i++) {
                input.nextToken();
                a[i] = (int) input.nval;
            }

            output.append(minOperations(a)).append('\n');
        }

        System.out.print(output);
    }
}
```

### C++

```cpp
#include <iostream>
#include <vector>
using namespace std;

int minOperations(const vector<int>& a) {
    int answer = 0;
    int previous = 0;

    for (int state : a) {
        // 当前开关是否需要按下
        int current = state ^ previous;
        answer += current;
        previous = current;
    }

    return answer;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int testCount;
    cin >> testCount;

    while (testCount--) {
        int n;
        cin >> n;

        vector<int> a(n);

        // 输入当前测试数据
        for (int i = 0; i < n; i++) {
            cin >> a[i];
        }

        cout << minOperations(a) << '\n';
    }

    return 0;
}
```