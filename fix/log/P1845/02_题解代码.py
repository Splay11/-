# 题解

双指针模拟

考虑 $n$ 为偶数的情况，第一次删除的是原本 $n / 2 - 1$ 的位置的数，第二次删除的是原本 $n / 2$ 的位置的数，第三次删除的是原本 $n / 2 - 2$ 的位置的数.....以此类推。

如果 $n$ 为奇数，删掉 $n / 2$ 的数后变成偶数的情况。

# AC代码

## Python

```python
def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    a = list(map(int, data[1:]))
    
    a.sort()
    mid = n // 2
    i = mid - (1 - (n % 2))
    j = mid
    
    result = []
    while i >= 0 and j < n:
        result.append(a[i])
        if i != j:
            result.append(a[j])
        i -= 1
        j += 1
    
    print(' '.join(map(str, result)))

if __name__ == "__main__":
    main()
```

## Java

```java
import java.util.*;

public class Main {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        int n = scanner.nextInt();
        int[] a = new int[n];
        for (int i = 0; i < n; i++) {
            a[i] = scanner.nextInt();
        }
        Arrays.sort(a);
        int mid = n / 2;
        int i = mid - (1 - (n % 2));
        int j = mid;

        StringBuilder result = new StringBuilder();
        while (i >= 0 && j < n) {
            result.append(a[i]).append(" ");
            if (i != j) {
                result.append(a[j]).append(" ");
            }
            i--;
            j++;
        }
        System.out.println(result.toString().trim());
    }
}
```

## C++

```cpp
#include <bits/stdc++.h>
using namespace std;

typedef long long LL;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(0);
    
    int n;
    cin >> n;
    vector<int> a(n);
    for (int i = 0; i < n; i++) {
        cin >> a[i];
    }
    sort(a.begin(), a.end());
    int mid = n >> 1;
    int i = mid - (1 - (n & 1));
    int j = mid;
    
    while (i >= 0 && j < n) {
        cout << a[i] << " ";
        if (i != j) {
            cout << a[j] << " ";
        }
        i--;
        j++;
    }
    return 0;
}
```