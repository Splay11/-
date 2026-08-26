## 思路

用按值二分在答案范围内搜索。记左右边界为 $l$ 与 $r$。当 $x \ge 2$ 时有 

![image](/file/2/amyBAH2gUNCalbTPk0_-C.png) 

因此可取初始区间 $[l=1,r=\left\lfloor \dfrac{x}{2} \right\rfloor+1]$；当 $x<2$ 时直接返回 $x$。

在循环中取中点

![image](/file/2/LnYSCbB4WbeqnriQdtYjv.png) 

。为了避免中间计算溢出，不直接比较$mid^2$ 与$x$，而是使用等价判断：

* 如果 $mid \le \left\lfloor \dfrac{x}{mid} \right\rfloor$，说明$mid^2 \le x$，可以尝试向右侧扩大，令 $ans = mid$ 且 $l = mid + 1$；
* 否则令 $r = mid - 1$。

循环结束时，$ans$ 即为所求的 $\lfloor \sqrt{x} \rfloor$。

## 正确性说明（简要）

始终保持不变量：当前可行解集合在区间 $[l,r]$ 内，且当判定 $mid \le \left\lfloor \dfrac{x}{mid} \right\rfloor$ 为真时，用 $ans$ 记录下界上的**最大可行值**。二分每步将区间长度至少减半，最终 $l>r$ 时，$ans$ 等于满足 $t^2 \le x$ 的最大整数 $t$，即 $\lfloor \sqrt{x} \rfloor$。


---

# 代码

## C++

```cpp
#include <iostream>
using namespace std;

// 计算并返回 floor(sqrt(x))
// 时间 O(log x)，空间 O(1)
int mysqrt(int x) {
    // 特判：0 和 1 直接返回
    if (x < 2) return x;

    int l = 1;
    // 对于 x>=2，答案不超过 x/2 + 1
    int r = x / 2 + 1;
    int ans = 0;

    while (l <= r) {
        int mid = l + (r - l) / 2; // 防止 (l+r) 溢出
        // 用除法替代 mid*mid <= x 的比较，避免溢出
        if (mid <= x / mid) {
            ans = mid;       // mid 是可行解，记录下来
            l = mid + 1;     // 尝试去更大的部分
        } else {
            r = mid - 1;     // mid 太大，缩到左侧
        }
    }
    return ans;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int x;
    if (cin >> x) {
        cout << mysqrt(x) << '\n';
    }
    return 0;
}
```

## Python

```python
import sys

# 计算并返回 floor(sqrt(x))
# 时间 O(log x)，空间 O(1)
def mysqrt(x: int) -> int:
    # 特判：0 和 1 直接返回
    if x < 2:
        return x

    l, r = 1, x // 2 + 1  # 对于 x>=2，答案不超过 x//2 + 1
    ans = 0

    while l <= r:
        mid = l + (r - l) // 2
        # 用除法避免 mid*mid 的溢出风险（Python 大整数安全，但保持同一思路）
        if mid <= x // mid:
            ans = mid      # 记录当前可行解
            l = mid + 1    # 右移，寻找更大可行值
        else:
            r = mid - 1    # 左移，缩小范围
    return ans

def main():
    data = sys.stdin.read().strip()
    if not data:
        return
    x = int(data)
    print(mysqrt(x))

if __name__ == "__main__":
    main()

```

## Java

```java
import java.io.BufferedReader;
import java.io.InputStreamReader;

public class Main {
    // 计算并返回 floor(sqrt(x))
    // 时间 O(log x)，空间 O(1)
    static int mysqrt(int x) {
        // 特判：0 和 1 直接返回
        if (x < 2) return x;

        int l = 1;
        int r = x / 2 + 1; // 对于 x>=2，答案不超过 x/2 + 1
        int ans = 0;

        while (l <= r) {
            int mid = l + (r - l) / 2; // 防止 (l+r) 溢出
            // 用除法替代 mid*mid <= x 的比较，避免溢出
            if (mid <= x / mid) {
                ans = mid;     // 记录可行解
                l = mid + 1;   // 右侧继续找更大的
            } else {
                r = mid - 1;   // mid 太大，缩到左侧
            }
        }
        return ans;
    }

    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String s = br.readLine();
        if (s != null && !s.trim().isEmpty()) {
            int x = (int) Long.parseLong(s.trim()); // 读入并解析
            System.out.println(mysqrt(x));
        }
    }
}

```