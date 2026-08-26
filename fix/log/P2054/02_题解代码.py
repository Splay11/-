## 思路:思维+构造

考虑构造数位为1234567890x的数，这个数一定能被x整除。

整除后的数作为y即可。

例如：x = 50 , x * y = 1233456789050 那么 y = 2469135781

数字比较大，C++/Java记得开long long

## 代码

### python
```python
t = int(input())
for i in range(t):
    x = int(input())
    s = "1234567890" + str(x)
    y = int(s) // x 
    print(y)
```

### java
```java
import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        int t = scanner.nextInt();
        for (int i = 0; i < t; i++) {
            long x = scanner.nextLong();
            String s = "1234567890" + x;
            long y = Long.parseLong(s) / x;
            System.out.println(y);
        }
        scanner.close();
    }
}
```

### c++
```cpp
#include <iostream>
#include <string>
using namespace std;

int main() {
    int t;
    cin >> t;
    while (t--) {
        long long x;
        cin >> x;
        string s = "1234567890" + to_string(x);
        long long y = stoll(s) / x;
        cout << y << endl;
    }
    return 0;
}
```



OJ会员可以通过点击题目上方《已通过》查看其他通过代码来学习。