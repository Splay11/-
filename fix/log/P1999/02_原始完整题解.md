## 思路
&emsp;&emsp;此题实际上是一个模拟问题，要求任意k个连续元素总和不超过sum，那么可以从左到右使用滑动窗口的方式取枚举每k个连续的元素，若超过，则对窗口内最后一位数字进行操作
## 代码
### python

```python
from collections import deque

n, k, sum_val = map(int, input().split())
a = list(map(int, input().split()))

dq = deque()
cur = 0
ans = 0

for i in range(n):
    while dq and dq[0][0] < i - k + 1:
        p = dq.popleft()
        cur -= p[1]

    cur += a[i]
    dq.append((i, a[i]))

    while cur > sum_val:
        diff = cur - sum_val
        sub = min(dq[-1][1], diff)
        cur -= sub
        dq[-1] = (dq[-1][0], dq[-1][1] - sub)
        ans += sub

        if dq[-1][1] == 0:
            dq.pop()

print(ans)
```
### java
```java
import java.util.ArrayDeque;
import java.util.Deque;
import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        int n = scanner.nextInt();
        long k = scanner.nextLong();
        long sum_val = scanner.nextLong();

        long[] a = new long[n];
        for (int i = 0; i < n; i++) {
            a[i] = scanner.nextLong();
        }

        Deque<long[]> dq = new ArrayDeque<>();
        long cur = 0;
        long ans = 0;

        for (int i = 0; i < n; i++) {
            while (!dq.isEmpty() && dq.peekFirst()[0] < i - k + 1) {
                long[] p = dq.pollFirst();
                cur -= p[1];
            }

            cur += a[i];
            dq.offerLast(new long[]{i, a[i]});

            while (cur > sum_val) {
                long diff = cur - sum_val;
                long sub = Math.min(dq.peekLast()[1], diff);
                cur -= sub;
                dq.peekLast()[1] -= sub;
                ans += sub;

                if (dq.peekLast()[1] == 0) {
                    dq.pollLast();
                }
            }
        }

        System.out.println(ans);
    }
}
```
### c++
```cpp
#include <iostream>
#include <deque>
#include <vector>
#include <algorithm>

using namespace std;

int main() {
    int n;
    long long k, sum_val;
    cin >> n >> k >> sum_val;

    vector<long long> a(n);
    for (int i = 0; i < n; i++) {
        cin >> a[i];
    }

    deque<pair<int, long long>> dq;
    long long cur = 0;
    long long ans = 0;

    for (int i = 0; i < n; i++) {
        while (!dq.empty() && dq.front().first < i - k + 1) {
            long long p = dq.front().second;
            cur -= p;
            dq.pop_front();
        }

        cur += a[i];
        dq.push_back(make_pair(i, a[i]));

        while (cur > sum_val) {
            long long diff = cur - sum_val;
            long long sub = min(dq.back().second, diff);
            cur -= sub;
            dq.back().second -= sub;
            ans += sub;

            if (dq.back().second == 0) {
                dq.pop_back();
            }
        }
    }

    cout << ans << endl;

    return 0;
}
```