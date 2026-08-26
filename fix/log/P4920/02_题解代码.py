## 解题思路

本题使用的核心算法是数学推导与同余不变量。

一次操作有两种情况：

从第一个王国给第二个王国：

第一个王国减少 $1$，第二个王国增加 $2$。

如果当前数量为 $x,y$，那么差值为：

$x-y$

操作后差值变为：

$(x-1)-(y+2)=x-y-3$

也就是说，差值会减少 $3$。

同理，如果从第二个王国给第一个王国，差值会增加 $3$。

因此，两个王国水晶数量的差值对 $3$ 取模是不变的。

最终想要相等，差值必须变成 $0$，所以初始差值必须满足：

$(x-y)\bmod 3=0$

如果满足这个条件，就可以一直让水晶多的一方发动仪式，每次让差值减少或增加 $3$，最终一定可以变成相等。

所以判断条件就是：

$(x-y)%3==0$

## 复杂度分析

对于每组测试数据，只需要进行一次取模判断。

时间复杂度为：

$O(T)$

空间复杂度为：

$O(1)$

## 代码实现

### Python

```python
import sys

# 判断两个王国是否可以最终水晶数量相等
def can_equal(x, y):
    # 差值对 3 取模不变，最终相等时差值必须为 0
    return (x - y) % 3 == 0

def main():
    data = sys.stdin.read().split()
    t = int(data[0])
    ans = []
    idx = 1

    for _ in range(t):
        x = int(data[idx])
        y = int(data[idx + 1])
        idx += 2

        # 根据判断结果输出答案
        if can_equal(x, y):
            ans.append("YES")
        else:
            ans.append("NO")

    print("\n".join(ans))

if __name__ == "__main__":
    main()
```

### Java

```java
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.util.StringTokenizer;

public class Main {

    // 判断两个王国是否可以最终水晶数量相等
    static boolean canEqual(long x, long y) {
        // 差值对 3 取模不变，最终相等时差值必须为 0
        return (x - y) % 3 == 0;
    }

    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StringBuilder sb = new StringBuilder();

        int t = Integer.parseInt(br.readLine().trim());

        for (int i = 0; i < t; i++) {
            StringTokenizer st = new StringTokenizer(br.readLine());

            long x = Long.parseLong(st.nextToken());
            long y = Long.parseLong(st.nextToken());

            // 根据判断结果输出答案
            if (canEqual(x, y)) {
                sb.append("YES\n");
            } else {
                sb.append("NO\n");
            }
        }

        System.out.print(sb.toString());
    }
}
```

### C++

```cpp
#include <iostream>
using namespace std;

// 判断两个王国是否可以最终水晶数量相等
bool canEqual(long long x, long long y) {
    // 差值对 3 取模不变，最终相等时差值必须为 0
    return (x - y) % 3 == 0;
}

int main() {
    int T;
    cin >> T;

    while (T--) {
        long long x, y;
        cin >> x >> y;

        // 根据判断结果输出答案
        if (canEqual(x, y)) {
            cout << "YES\n";
        } else {
            cout << "NO\n";
        }
    }

    return 0;
}
```