## 解题思路

本题使用线性扫描算法。

只需要遍历一次所有石子堆，对于每一堆石子数量 $a_i$：

如果 $a_i > x$，说明这堆满足条件，需要拿走 $y$ 颗石子；

否则不拿。

统计满足条件的石子堆数量 $cnt$，最终答案就是：

$cnt \times y$

由于答案最大可能达到 $2 \times 10^5 \times 10^9 = 2 \times 10^{14}$，所以需要使用长整型存储结果。

## 复杂度分析

时间复杂度：$O(n)$，需要遍历 $n$ 堆石子一次。

空间复杂度：$O(1)$，除输入数组外，只使用常数额外空间。

## 代码实现

### Python

```python
import sys

def solve(n, x, y, arr):
    ans = 0
    for a in arr:
        # 如果当前石子堆数量严格大于 x，就拿走 y 颗
        if a > x:
            ans += y
    return ans

def main():
    n, x, y = map(int, sys.stdin.readline().split())
    arr = list(map(int, sys.stdin.readline().split()))
    print(solve(n, x, y, arr))

if __name__ == "__main__":
    main()
```

### Java

```java
import java.io.*;
import java.util.*;

public class Main {
    public static long solve(int n, long x, long y, long[] arr) {
        long ans = 0;

        for (int i = 0; i < n; i++) {
            // 如果当前石子堆数量严格大于 x，就拿走 y 颗
            if (arr[i] > x) {
                ans += y;
            }
        }

        return ans;
    }

    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));

        StringTokenizer st = new StringTokenizer(br.readLine());
        int n = Integer.parseInt(st.nextToken());
        long x = Long.parseLong(st.nextToken());
        long y = Long.parseLong(st.nextToken());

        long[] arr = new long[n];
        st = new StringTokenizer(br.readLine());

        for (int i = 0; i < n; i++) {
            arr[i] = Long.parseLong(st.nextToken());
        }

        System.out.println(solve(n, x, y, arr));
    }
}
```

### C++

```cpp
#include <iostream>
#include <vector>
using namespace std;

long long solve(int n, long long x, long long y, vector<long long>& arr) {
    long long ans = 0;

    for (int i = 0; i < n; i++) {
        // 如果当前石子堆数量严格大于 x，就拿走 y 颗
        if (arr[i] > x) {
            ans += y;
        }
    }

    return ans;
}

int main() {
    int n;
    long long x, y;
    cin >> n >> x >> y;

    vector<long long> arr(n);
    for (int i = 0; i < n; i++) {
        cin >> arr[i];
    }

    cout << solve(n, x, y, arr) << endl;

    return 0;
}
```