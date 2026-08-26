## 思路:贪心

首先，要字典序最小，我们自然想到最终构造的LIS为:1 2 3 , ... , k

接下来，我们可以将k + 1 , ... , n **逆序**往插入到k - 1 和 k之间，这样能恰好使得LIS不增大且数字尽量靠后

例如:5 3

1 2 3 -> 1 2 5 4 3 

## 代码:

### python
```py
n , k = map(int, input().split())
a = [0] * n
for i in range(k - 1):
    a[i] = i + 1
a[-1] = k
for i in range(n - 2 , k - 2 , -1):
    a[i] = k + n - i - 1
print(*a)
```
### Java
```java
import java.util.*;
class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int n = sc.nextInt() , k = sc.nextInt();
        int[] a = new int[n];
        for(int i = 0; i < k - 1; i++) {
            a[i] = i + 1;
        }
        a[n - 1] = k;
        for(int i = n - 2; i >= k - 1; i--) {
            a[i] = k + n - i - 1;
        }
        for(int i : a) {
            System.out.print(i + " ");
        }
    }
}
```

### C++
```cpp
#include <bits/stdc++.h>
using namespace std;
int main() {
    int n , k;
    cin >> n >> k;
    vector<int> a(n);
    for(int i = 0; i < k - 1; i++) {
        a[i] = i + 1;
    }
    a[n - 1] = k;
    for(int i = n - 2; i >= k - 1; i--) {
        a[i] = k + n - i - 1;
    }
    for(auto i : a) {
        cout << i << " ";
    }
    return 0;
}
```