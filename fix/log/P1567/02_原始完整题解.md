## 思路：哈希表模拟

这道题如果使用线段树那就是变复杂了，可以观察到答案是具有二段性的，所以可以考虑将答案二分，那么我们假设当前要修改到第x版计划，那么要怎么快速知道修改到第x版计划后是否有人的怒火值超过阙值呢，因为每一次修改只会对一段人的怒火值全部加1，那么我们就可以使用差分，O(1)的进行加减，当修改完第x版计划后进行前缀和一一比对是否超出阙值即可

**时间复杂度**:$O(nlogm)$

## 代码


### python

```python
def check(x):
    b = [0] * (n + 100)
    for i in range(1, x + 1):
        x1 = mb[i][0]
        x2 = mb[i][1]
        b[x1] += 1
        b[x2 + 1] -= 1
    for i in range(1, n + 1):
        b[i] += b[i - 1]
        if b[i] > a[i]:
            return False
    return True

n, m = map(int, input().split())
a = [0] + list(map(int, input().split()))
mb = [0] * (m + 1)
for i in range(1, m + 1):
    mb[i] = tuple(map(int, input().split()))

l = 0
r = m

while l < r:
    mid = (l + r + 1) // 2
    if check(mid):
        l = mid
    else:
        r = mid - 1

print(l)
```



**c++**

```cpp
#include <iostream>
#include <vector>

using namespace std;

int n, m;
vector<int> a, b;
vector<pair<int, int>> mb;

bool check(int x) {
    b = vector<int>(n + 100);
    for (int i = 1; i <= x; i++) {
        int x1 = mb[i].first;
        int x2 = mb[i].second;
        b[x1]++;
        b[x2 + 1]--;
    }
    for (int i = 1; i <= n; i++) {
        b[i] += b[i - 1];
        if (b[i] > a[i]) return false;
    }
    return true;
}

int main() {
    cin >> n >> m;
    a = vector<int>(n + 1);
    for (int i = 1; i <= n; i++) cin >> a[i];
    mb = vector<pair<int, int>>(m + 1);
    for (int i = 1; i <= m; i++) cin >> mb[i].first >> mb[i].second;
    int l = 0, r = m;
    while (l < r) {
        int mid = (l + r + 1) / 2;
        if (check(mid)) l = mid;
        else r = mid - 1;
    }
    cout << l << endl;
    return 0;
}
```

**Java**

```java
import java.util.*;

public class Main {
    static int n, m;
    static int[] a, b;
    static int[][] mb;

    static boolean check(int x) {
        b = new int[n + 100];
        for (int i = 1; i <= x; i++) {
            int x1 = mb[i][0];
            int x2 = mb[i][1];
            b[x1]++;
            b[x2 + 1]--;
        }
        for (int i = 1; i <= n; i++) {
            b[i] += b[i - 1];
            if (b[i] > a[i]) return false;
        }
        return true;
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        n = sc.nextInt();
        m = sc.nextInt();
        a = new int[n + 1];
        for (int i = 1; i <= n; i++) a[i] = sc.nextInt();
        mb = new int[m + 1][2];
        for (int i = 1; i <= m; i++) {
            mb[i][0] = sc.nextInt();
            mb[i][1] = sc.nextInt();
        }
        int l = 0, r = m;
        while (l < r) {
            int mid = (l + r + 1) / 2;
            if (check(mid)) l = mid;
            else r = mid - 1;
        }
        System.out.println(l);
    }
}
```