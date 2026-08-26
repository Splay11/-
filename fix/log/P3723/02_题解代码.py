## 解题思路

本题要求判断给定三位整数 $n$ 是否满足 $n=a^3+b^3+c^3$（其中 $a,b,c$ 为百位、十位和个位）。做法是将整数按位拆分后计算立方和并比较。

* 算法范畴：本题属于**数学与模拟/枚举**，不需要使用贪心、动态规划、二分或图论等高级算法。
* 核心思路：

  1. 提取百位 $a=n//100$，十位 $b=(n//10)\%10$，个位 $c=n\%10$。
  2. 计算 $s=a^3+b^3+c^3$。
  3. 若 $s==n$ 输出 `YES`，否则输出 `NO`。
* 实现方法：编写一个判定函数 `is_armstrong(n)`（或同名函数），主函数负责读入并输出结果。

## 复杂度分析

* 时间复杂度：常数级 $O(1)$（仅做若干次算术运算）。
* 空间复杂度：常数级 $O(1)$。

## 代码实现

### Python

```python
# 功能函数：判断三位整数是否为水仙花数
def is_armstrong(n: int) -> bool:
    # 提取各位数字
    a = n // 100           # 百位
    b = (n // 10) % 10     # 十位
    c = n % 10             # 个位
    # 计算各位立方和并比较
    return a**3 + b**3 + c**3 == n

def main():
    # 读取输入（题面保证输入合法且为三位整数）
    n = int(input().strip())
    # 调用判定函数并输出结果
    print("YES" if is_armstrong(n) else "NO")

if __name__ == "__main__":
    main()
```

### Java

```java
import java.util.Scanner;

public class Main {
    // 功能函数：判断三位整数是否为水仙花数
    public static boolean isArmstrong(int n) {
        int a = n / 100;          // 百位
        int b = (n / 10) % 10;    // 十位
        int c = n % 10;           // 个位
        // 用整型乘法避免浮点误差
        int sum = a * a * a + b * b * b + c * c * c;
        return sum == n;
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        // 读取输入（题面保证合法）
        int n = sc.nextInt();
        // 判定并输出
        System.out.println(isArmstrong(n) ? "YES" : "NO");
        sc.close();
    }
}
```

### C++

```cpp
#include <bits/stdc++.h>
using namespace std;

// 功能函数：判断三位整数是否为水仙花数
bool isArmstrong(int n) {
    int a = n / 100;           // 百位
    int b = (n / 10) % 10;     // 十位
    int c = n % 10;            // 个位
    int sum = a*a*a + b*b*b + c*c*c; // 立方和
    return sum == n;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n;
    // 读取输入（题面保证为三位整数）
    if (cin >> n) {
        cout << (isArmstrong(n) ? "YES" : "NO") << "\n";
    }
    return 0;
}
```