# 题解

这题题目要求 $2^{a_i}3^{b_i} \neq 2^{a_j}3^{b_j}$ 

那我们直接令所有的 $b = 0$，题目就变成了将一个 $n$ 转成 $2 ^ {a_i} + 2 ^ {a_{i + 1}} ...$，成了一个简单的二进制转换问题。

> 由于 $a_i$ 和 $b_i$ 的数量很有限，那么其 $a_ib_i$ 的组合数量也不多。
>
> 于是塔子哥猜测，出题人原本不是想考察这个。而是更像考察物品数量比较少，且背包容量比较大的，01背包恰好装满问题，这个可以用 **最短路优化背包** 的方法解决，但由于在笔试中这个难度有点超纲了，感兴趣的朋友可以自行了解。



# AC代码

## Python 

```python
T = int(input())
for _ in range(T):
    n = int(input())
    v = [(1 << i) for i in range(31, -1, -1) if (n >> i & 1)]
    print(len(v))
    print(*v)
```

## Java

```java
import java.util.*;

public class Main {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        int T = scanner.nextInt();
        for (int t = 0; t < T; t++) {
            int n = scanner.nextInt();
            List<Integer> v = new ArrayList<>();
            for (int i = 31; i >= 0; i--) {
                if ((n >> i & 1) == 1) {
                    v.add(1 << i);
                }
            }
            System.out.println(v.size());
            for (int num : v) {
                System.out.print(num + " ");
            }
            System.out.println();
        }
    }
}
```

## C++

```cpp
#include <iostream>
#include <vector>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(0);
    
    int T;
    cin >> T;
    while (T--) {
        int n;
        cin >> n;
        vector<int> v;
        for (int i = 31; i >= 0; i--) {
            if ((n >> i) & 1) {
                v.push_back(1 << i);
            }
        }
        cout << v.size() << "\n";
        for (int num : v) {
            cout << num << " ";
        }
        cout << "\n";
    }
    
    return 0;
}
```