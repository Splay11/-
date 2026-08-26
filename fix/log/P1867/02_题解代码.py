## 题解
这题分析后发现，其实和树形结构无关，交换可以看成是，将节点的权值放到数组上，对数组进行交换。
由于题目说了是个排列，我们只要从前往后，碰到能交换的进行交换就可以了。


## AC代码
- Python
```python

n = int(input())
a = [0] + [int(x) for x in input().split()]

for _ in range(1, n):
    input()

index_map = {a[i]: i for i in range(1, n + 1)}
res = 0

for i in range(n, 0, -1):
    while a[i] != i:
        res += 1
        temp = a[i]
        a[i] = a[temp]
        a[temp] = temp

        # 更新哈希表
        index_map[a[temp]] = temp
        index_map[a[i]] = i

print(res)



```
- Java
```java
import java.util.*;

public class Main {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        int n = scanner.nextInt();
        int[] a = new int[n + 1];
        Map<Integer, Integer> indexMap = new HashMap<>();

        for (int i = 1; i <= n; i++) {
            a[i] = scanner.nextInt();
            indexMap.put(a[i], i);
        }

        for (int i = 1; i < n; i++) {
            scanner.nextInt();
        }

        int res = 0;

        for (int i = n; i > 0; i--) {
            while (a[i] != i) {
                res++;
                int temp = a[i];
                a[i] = a[temp];
                a[temp] = temp;

                // 更新哈希表
                indexMap.put(a[temp], temp);
                indexMap.put(a[i], i);
            }
        }

        System.out.println(res);
    }
}

```

- CPP
```cpp
#include <iostream>
#include <vector>
#include <unordered_map>
using namespace std;

int main() {
    int n;
    cin >> n;
    vector<int> a(n + 1);
    unordered_map<int, int> index_map;

    for (int i = 1; i <= n; ++i) {
        cin >> a[i];
        index_map[a[i]] = i;
    }

    for (int i = 1; i < n; ++i) {
        int dummy;
        cin >> dummy;
    }

    int res = 0;

    for (int i = n; i > 0; --i) {
        while (a[i] != i) {
            res++;
            int temp = a[i];
            a[i] = a[temp];
            a[temp] = temp;

            // 更新哈希表
            index_map[a[temp]] = temp;
            index_map[a[i]] = i;
        }
    }

    cout << res << endl;

    return 0;
}

```