## 思路
这道题有两种解决办法，贪心或者动态规划都是可以的，当然贪心会更加简单，拼接博客的吸引度是赞数和踩数差的绝对值，如果令差值最大，显然就是使赞数更多踩数越少或踩数越多赞数越少，显然贪心可以完成这两项，只需要将赞数比踩数多的博客拼接起来和踩数比赞数多的博客拼接起来然后取两个吸引度的最大值即可
## 代码


### c++

```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    int n;
    cin >> n;
    vector<int> a(n);
    long long ans1 = 0, ans2 = 0;
    for (int i = 0; i < n; i++) {
        cin >> a[i];
    }
    for (int i = 0; i < n; i++) {
        int t;
        cin >> t;
        if (a[i] > t) {
            ans1 += a[i] - t;
        } else {
            ans2 += t - a[i];
        }

    }
    cout << max(ans1, ans2) << endl;
    return 0;
}

```
python
```python
n = int(input())
a = list(map(int,input().split()))
b = list(map(int,input().split()))
n = len(a)
c = [0] * n
for i in range(n):
    c[i] = a[i] - b[i]
c.sort()
sum1 = 0
sum2 = 0
for i in range(n - 1, -1, -1):
    if c[i] > 0:
        sum1 += c[i]
    else: sum2 += -c[i]
print(max(sum1, sum2))
```
java
```java
import java.util.*;

public class Main {

    public static void main(String[] args) {
        Scanner sc= new Scanner(System.in);
        int n = sc.nextInt();
        int[] a = new int[n];
        int[] b = new int[n];
        for (int i = 0; i < n; i++) {
            a[i] = sc.nextInt();
        }
        for (int i = 0; i < n; i++) {
            b[i] = sc.nextInt();
        }
        int max1 = 0, max2 = 0;
        long sum1 = 0, sum2 = 0;
        for (int i = 0; i < n; i++) {
            if (a[i] > b[i]){
                sum1 += a[i] - b[i];
            }else {
                sum2 += Math.abs(a[i] - b[i]);
            }
        }
        System.out.println(Math.max(sum1,sum2));
    }


}
```