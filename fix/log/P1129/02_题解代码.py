题目给出了计算概率的公式，则直接模拟公式即可,公式中的△x就等于(b - a) / 500。求出每个xi的值再求和即可。

C++
```c++
#include<bits/stdc++.h>

using namespace std;

double a, b;

double f(double x) {
    return sin(sqrt(x)) / 5.68 * (b - a) / 500;// 计算每个xi的值
}

void solve() {
    cin >> a >> b;
    double ans = 0;
    for (int i = 0; i < 500; i++) {
        ans += f(a + i * (b - a) / 500); //求出每个xi
    }
    cout << (ans > 0.5) << endl;
}

int main() {
    int t = 1;
    cin >> t;
    while (t--) solve();
    return 0;
}
```

Python
```python
from math import *
def calc(a,b):
    delta = (b-a)/500
    ans = 0
    x = a + delta
    for _ in range(500):
        ans += delta*sin(sqrt(x))/5.68
        x += delta  
    return ans 

t = int(input())
for _ in range(t):
    a,b = list(map(int,input().split()))
    if calc(a,b) > 0.5:
        print(1)
    else:
        print(0)
```

Java
```java
import java.util.*;

public class Main {
    public static void main(String[] args) {
        Scanner in = new Scanner(System.in);
        int n = in.nextInt();

        List<Double> list = new ArrayList<>();

        while (n-- > 0) {
            int a = in.nextInt();
            int b = in.nextInt();

            double deltaX = (b - a) / 500.0;
            double sum = 0.0;

            double xi = a;
            double X_i = a + deltaX;
            // 套公式，总共要加500次
            for (int i = 0; i < 500; i++) {
                sum += Math.sin(Math.sqrt(xi)) / 5.68 * deltaX;

                xi = X_i;
                X_i += deltaX;
            }
            System.out.println(sum > 0.5 ? 1 : 0);
        }




    }


};
```