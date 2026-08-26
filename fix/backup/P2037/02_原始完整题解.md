## 思路
&emsp;&emsp;其实是一个比较简单的最大不相交区间数量问题，因为所有圆的圆心都在同一条线上，那么每一个圆的左右与坐标轴相交的地方就是左右端点，将圆看作一个区间，所有圆不相交不重合就是所有的区间都相互分离，那么问题就是在许多的区间中选出一部分区间使得选出的区间不相交并使选出的区间数量最大，这其实一个经典的问题，只需要按照区间右端点进行排序，然后从左至右进行贪心的选取即可，具体证明可以自行了解
## 代码
### python

```python
# leetcode 435. 无重叠区间
n = int(input())
lines = []
for _ in range(n):
    x , y = map(int, input().split())
    left = x - y
    right = x + y
    lines.append((left, right))
lines.sort(key=lambda x: x[1])
ans = 0
now = -10**9
for left, right in lines:
    if left > now:
        ans += 1
        now = right
print(ans)
```
### java

```java
import java.util.Arrays;
import java.util.Scanner;

class Main {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        int n = scanner.nextInt();
        int[][] lines = new int[n][2];

        for (int i = 0; i < n; i++) {
            int x = scanner.nextInt();
            int y = scanner.nextInt();
            int left = x - y;
            int right = x + y;
            lines[i][0] = left;
            lines[i][1] = right;
        }

        // 排序
        Arrays.sort(lines, (a, b) -> Integer.compare(a[1], b[1]));

        int ans = 0;
        int now = -1000000000;

        for (int[] line : lines) {
            int left = line[0];
            int right = line[1];
            if (left > now) {
                ans += 1;
                now = right;
            }
        }

        System.out.println(ans);
    }
}
```
### c++

```cpp
#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

int main() {
    int n;
    cin >> n;
    vector<vector<int>> lines(n, vector<int>(2));

    for (int i = 0; i < n; i++) {
        int x, y;
        cin >> x >> y;
        int left = x - y;
        int right = x + y;
        lines[i][0] = left;
        lines[i][1] = right;
    }

    sort(lines.begin(), lines.end(), [](const vector<int> &a, const vector<int> &b) {
        return a[1] < b[1];
    });

    int ans = 0;
    int now = -1000000000;

    for (const vector<int> &line : lines) {
        int left = line[0];
        int right = line[1];
        if (left > now) {
            ans += 1;
            now = right;
        }
    }

    cout << ans << endl;

    return 0;
}
```