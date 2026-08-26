## 题解

按照题目模拟即可，注意总和可能会爆 int 。

枚举 $n$ 个位置，将每个位置乘 2 后判断是否相等。

## AC代码
### python
```python
import sys
input = lambda:sys.stdin.readline().strip()
n = int(input())
a = list(map(int, input().split()))
su = sum(list(map(int, input().split())))
s = sum(a)
res = sum([1 if s + val == su else 0 for val in a])
print(res)
```
### C++
```C++
#include <bits/stdc++.h>
using namespace std;

void solve() {
    int n;
    cin >> n;

    vector<int> a(n), b(n);
    long long sum_a = 0, sum_b = 0;
    for (int i = 0; i < n; ++i) {
        cin >> a[i];
        sum_a += a[i];
    }
    for (int i = 0; i < n; ++i) {
        cin >> b[i];
        sum_b += b[i];
    }

    int result = 0;
    long long val = sum_b - sum_a;
    for (int i = 0; i < n; ++i) {
        if (val == a[i]) ++result;
    }
    cout << result << endl;
}

int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(nullptr);

    solve();
    return 0;
}
```
### java
```java
import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        
        // 读取n的值
        int n = scanner.nextInt();
        
        // 读取数组a
        int[] a = new int[n];
        for (int i = 0; i < n; i++) {
            a[i] = scanner.nextInt();
        }
        
        // 读取另一个数组并计算其总和su
        int su = 0;
        for (int i = 0; i < n; i++) {
            su += scanner.nextInt();
        }
        
        // 计算数组a的总和
        int s = 0;
        for (int i = 0; i < n; i++) {
            s += a[i];
        }
        
        // 计算res的值
        int res = 0;
        for (int i = 0; i < n; i++) {
            if (s + a[i] == su) {
                res++;
            }
        }
        
        // 输出结果
        System.out.println(res);

        scanner.close();
    }
}
```