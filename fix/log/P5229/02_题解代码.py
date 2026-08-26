## 解题思路

考虑排列中第 $i$ 个位置上的元素 $v_i$。

一个包含位置 $i$ 的子数组，其左端点可以从 $1$ 到 $i$ 中选择，共有 $i$ 种选择；右端点可以从 $i$ 到 $n$ 中选择，共有 $n-i+1$ 种选择。

因此，第 $i$ 个位置会被

$$
i(n-i+1)
$$

个子数组包含。

于是所有非空子数组元素和的总和可以写成

$$
\sum_{i=1}^{n} v_i\cdot i(n-i+1).
$$

问题就转化为了：将排列中的 $1,2,\ldots,n$ 分配给不同的位置，使上式最大。

使用贪心思想和排序不等式可知：

* 权值越大的位置，应该放越大的数字。
* 权值 $i(n-i+1)$ 关于中间位置对称。
* 从数组两端向中间移动时，权值不断增大。

因此不需要真的对位置排序，只需要从两端向中间依次放置较小的数字即可。

维护左右指针 $L,R$ 和当前最小值 $x$：

1. 在位置 $L$ 放入 $x$，然后令 $x$ 增加 $1$。
2. 如果 $L\ne R$，在位置 $R$ 放入新的 $x$，再令 $x$ 增加 $1$。
3. 将 $L$ 右移、$R$ 左移。
4. 重复直到所有位置都被填入。

左右两个对称位置的权值相同，所以同一层的两个数字以什么顺序放置都不会影响答案。

构造完成后，根据

$$
v_i\cdot i(n-i+1)
$$

计算每个位置的贡献，并对 $1000000007$ 取模即可。

## 复杂度分析

只需要从两端向中间构造一次排列，并遍历一次数组计算答案。

时间复杂度为 $O(n)$。

保存构造出的排列需要 $O(n)$ 的空间，因此空间复杂度为 $O(n)$。

## 代码实现

### Python

```python
MOD = 1000000007


def solve(n):
    # 构造最优排列
    p = [0] * n
    left = 0
    right = n - 1
    value = 1

    while left <= right:
        # 较小的数放在当前左端
        p[left] = value
        value += 1

        # 对称位置权值相同
        if left != right:
            p[right] = value
            value += 1

        left += 1
        right -= 1

    # 计算所有位置的总贡献
    ans = 0
    for i in range(n):
        weight = (i + 1) * (n - i)
        ans = (ans + p[i] * weight) % MOD

    return ans, p


def main():
    n = int(input())

    ans, p = solve(n)

    print(ans)
    print(*p)


if __name__ == "__main__":
    main()
```

### Java

```java
import java.util.Scanner;

public class Main {
    static final long MOD = 1000000007L;

    // 构造最优排列，并返回最大总和
    static long solve(int n, int[] p) {
        int left = 0;
        int right = n - 1;
        int value = 1;

        while (left <= right) {
            // 较小的数放在当前左端
            p[left] = value;
            value++;

            // 对称位置的权值相同
            if (left != right) {
                p[right] = value;
                value++;
            }

            left++;
            right--;
        }

        // 计算所有位置的贡献
        long ans = 0;

        for (int i = 0; i < n; i++) {
            long weight = (long) (i + 1) * (n - i);
            ans = (ans + weight % MOD * p[i]) % MOD;
        }

        return ans;
    }

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        int n = scanner.nextInt();
        int[] p = new int[n];

        long ans = solve(n, p);

        System.out.println(ans);

        StringBuilder result = new StringBuilder();
        for (int i = 0; i < n; i++) {
            if (i > 0) {
                result.append(' ');
            }
            result.append(p[i]);
        }

        System.out.println(result);
        scanner.close();
    }
}
```

### C++

```cpp
#include <iostream>
#include <vector>
using namespace std;

const long long MOD = 1000000007LL;

// 构造最优排列，并返回最大总和
long long solve(int n, vector<int>& p) {
    int left = 0;
    int right = n - 1;
    int value = 1;

    while (left <= right) {
        // 较小的数放在当前左端
        p[left] = value;
        value++;

        // 对称位置的权值相同
        if (left != right) {
            p[right] = value;
            value++;
        }

        left++;
        right--;
    }

    // 计算所有位置的贡献
    long long ans = 0;

    for (int i = 0; i < n; i++) {
        long long weight = 1LL * (i + 1) * (n - i);
        ans = (ans + weight % MOD * p[i]) % MOD;
    }

    return ans;
}

int main() {
    int n;
    cin >> n;

    vector<int> p(n);

    long long ans = solve(n, p);

    cout << ans << '\n';

    for (int i = 0; i < n; i++) {
        if (i > 0) {
            cout << ' ';
        }
        cout << p[i];
    }
    cout << '\n';

    return 0;
}
```