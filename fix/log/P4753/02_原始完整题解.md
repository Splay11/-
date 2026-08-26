## 解题思路

题目要求判断一个 $n \times m$ 的矩阵，是否对所有合法位置都满足：

$$
A_{i,j}=A_{i+1,j+1}
$$

这说明矩阵中每一条从左上到右下的对角线上的元素都必须相等。

可以直接使用模拟算法解决。

具体做法是遍历所有满足右下角仍然存在的位置，也就是枚举 $i \in [0,n-2]$、$j \in [0,m-2]$，检查：

$$
A_{i,j} \stackrel{?}{=} A_{i+1,j+1}
$$

只要有一处不相等，就说明不满足题意，直接输出 $No$；如果全部检查后都相等，就输出 $Yes$。

实现上，先读入整个矩阵，再进行逐个比较即可。

这道题使用的相关算法是矩阵遍历与模拟判断。

## 复杂度分析

设矩阵大小为 $n \times m$。

需要遍历矩阵中所有可以与右下角比较的位置一次，因此时间复杂度为：

$$
O(n \times m)
$$

需要存储整个矩阵，空间复杂度为：

$$
O(n \times m)
$$

由于题目保证所有测试数据满足 $\sum n \times m \le 10^6$，所以这个复杂度是合适的。

## 代码实现

### Python

```python
# 判断矩阵是否满足条件的函数
def check_matrix(a, n, m):
    # 枚举每个可以和右下角比较的位置
    for i in range(n - 1):
        for j in range(m - 1):
            if a[i][j] != a[i + 1][j + 1]:
                return False
    return True


def main():
    t = int(input())
    ans = []

    for _ in range(t):
        n, m = map(int, input().split())

        # 读入矩阵
        a = []
        for _ in range(n):
            a.append(list(map(int, input().split())))

        # 判断并记录答案
        if check_matrix(a, n, m):
            ans.append("Yes")
        else:
            ans.append("No")

    print("\n".join(ans))


if __name__ == "__main__":
    main()
```

### Java

```java
import java.util.Scanner;

public class Main {

    // 判断矩阵是否满足条件的函数
    public static boolean checkMatrix(int[][] a, int n, int m) {
        // 枚举每个可以和右下角比较的位置
        for (int i = 0; i < n - 1; i++) {
            for (int j = 0; j < m - 1; j++) {
                if (a[i][j] != a[i + 1][j + 1]) {
                    return false;
                }
            }
        }
        return true;
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        StringBuilder sb = new StringBuilder();

        int t = sc.nextInt();

        while (t-- > 0) {
            int n = sc.nextInt();
            int m = sc.nextInt();

            // 读入矩阵
            int[][] a = new int[n][m];
            for (int i = 0; i < n; i++) {
                for (int j = 0; j < m; j++) {
                    a[i][j] = sc.nextInt();
                }
            }

            // 判断并记录答案
            if (checkMatrix(a, n, m)) {
                sb.append("Yes\n");
            } else {
                sb.append("No\n");
            }
        }

        System.out.print(sb.toString());
        sc.close();
    }
}
```

### C++

```cpp
#include <iostream>
#include <vector>
using namespace std;

// 判断矩阵是否满足条件的函数
bool checkMatrix(const vector<vector<int>>& a, int n, int m) {
    // 枚举每个可以和右下角比较的位置
    for (int i = 0; i < n - 1; i++) {
        for (int j = 0; j < m - 1; j++) {
            if (a[i][j] != a[i + 1][j + 1]) {
                return false;
            }
        }
    }
    return true;
}

int main() {
    int t;
    cin >> t;

    while (t--) {
        int n, m;
        cin >> n >> m;

        // 读入矩阵
        vector<vector<int>> a(n, vector<int>(m));
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < m; j++) {
                cin >> a[i][j];
            }
        }

        // 判断并输出结果
        if (checkMatrix(a, n, m)) {
            cout << "Yes\n";
        } else {
            cout << "No\n";
        }
    }

    return 0;
}
```