## 解题思路

初始时 $a=1$，每次按如下规则更新：

$$
a \leftarrow (a \cdot k)\bmod m
$$

要求在无限次执行更新的过程中，$a$ 一共会取到多少个不同的值。

### 核心思路

由于每次更新后，$a$ 的取值一定在区间 $[0,m-1]$ 内，因此总状态数最多只有 $m$ 个。

也就是说，序列：

$$
1,\ (1\cdot k)\bmod m,\ (((1\cdot k)\bmod m)\cdot k)\bmod m,\ \cdots
$$

最多走 $m+1$ 步，就一定会出现某个值重复。一旦某个值重复，之后的变化过程也会完全重复，因此后面不会再产生新的值。

所以这道题可以直接按题意模拟：

1. 用一个布尔数组 `visited` 记录某个值是否已经出现过。
2. 初始时 $a=1$。
3. 只要当前 $a$ 没出现过，就：

   * 标记它已出现；
   * 答案加一；
   * 更新 $a=(a\cdot k)\bmod m$。
4. 当发现当前 $a$ 已经出现过时，说明进入循环，结束即可。


## 复杂度分析

设一共访问了 $t$ 个不同的值，则有 $t\le m$。

* 时间复杂度：$O(m)$
* 空间复杂度：$O(m)$

## 代码实现

### Python

```python
def count_distinct_values(k, m):
    # visited[x] 表示值 x 是否已经出现过
    visited = [False] * m

    # 初始值 a = 1
    a = 1
    ans = 0

    # 当当前值没有出现过时，继续模拟
    while not visited[a]:
        # 标记当前值已出现
        visited[a] = True

        # 不同值个数加一
        ans += 1

        # 按题意更新 a
        a = (a * k) % m

    return ans


def main():
    # 读取输入
    k, m = map(int, input().split())

    # 调用函数并输出答案
    print(count_distinct_values(k, m))


if __name__ == "__main__":
    main()
```

### Java

```java
import java.util.Scanner;

public class Main {
    public static int countDistinctValues(int k, int m) {
        // visited[x] 表示值 x 是否已经出现过
        boolean[] visited = new boolean[m];

        // 初始值 a = 1
        int a = 1;
        int ans = 0;

        // 当当前值没有出现过时，继续模拟
        while (!visited[a]) {
            // 标记当前值已出现
            visited[a] = true;

            // 不同值个数加一
            ans++;

            // 按题意更新 a
            // 这里先转成 long，避免乘法过程中的整型风险
            a = (int) ((long) a * k % m);
        }

        return ans;
    }

    public static void main(String[] args) {
        // 按数据范围，Scanner 足够使用
        Scanner sc = new Scanner(System.in);

        // 读取输入
        int k = sc.nextInt();
        int m = sc.nextInt();

        // 调用函数并输出答案
        System.out.println(countDistinctValues(k, m));

        sc.close();
    }
}
```

### C++

```cpp
#include <iostream>
#include <vector>
using namespace std;

int countDistinctValues(int k, int m) {
    // visited[x] 表示值 x 是否已经出现过
    vector<bool> visited(m, false);

    // 初始值 a = 1
    int a = 1;
    int ans = 0;

    // 当当前值没有出现过时，继续模拟
    while (!visited[a]) {
        // 标记当前值已出现
        visited[a] = true;

        // 不同值个数加一
        ans++;

        // 按题意更新 a
        // 这里使用 long long，避免乘法过程中的整型风险
        a = (int)((1LL * a * k) % m);
    }

    return ans;
}

int main() {
    // 读取输入
    int k, m;
    cin >> k >> m;

    // 调用函数并输出答案
    cout << countDistinctValues(k, m) << '\n';

    return 0;
}
```