# 思路

* 逐个遍历数组中的每个 $a_i$，若同时满足条件 $a_i$ 为偶数且 $l\le a_i\le r$，则计数器加一。
* 时间复杂度 $O(n)$，空间复杂度 $O(1)$。

## C++ 

```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, l, r;
    if (!(cin >> n >> l >> r)) return 0;
    int ans = 0;
    for (int i = 0; i < n; ++i) {
        int x; 
        cin >> x;
        // 如果 x 是偶数且位于 [l, r]，则计数
        if (x % 2 == 0 && l <= x && x <= r) {
            ++ans;
        }
    }
    cout << ans << "\n";
    return 0;
}
```

## Python 
```python
# 读取输入
n, l, r = map(int, input().split())
arr = list(map(int, input().split()))

ans = 0
for x in arr:
    # 如果 x 是偶数且在 [l, r] 区间内，则计数
    if x % 2 == 0 and l <= x <= r:
        ans += 1

print(ans)
```

## Java 

```java
import java.util.*;

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        int n = sc.nextInt();
        int l = sc.nextInt();
        int r = sc.nextInt();

        int ans = 0;
        for (int i = 0; i < n; i++) {
            int x = sc.nextInt();
            // 如果 x 是偶数且位于 [l, r]，则计数
            if (x % 2 == 0 && x >= l && x <= r) {
                ans++;
            }
        }
        System.out.println(ans);
        sc.close();
    }
}
```