# 题解

## 题面描述

有一个大小为 $n\times m$ 的矩阵，只包含字母 'o' 和 'p'。每次操作可以将任意一个 'o' 变成 'p'，问最少需要多少次操作才能使矩阵具有**中心对称性**（绕中心旋转180°后矩阵不变）。

---

## 思路

1. **中心对称条件**  
   对于位置 $(i,j)$，它在旋转180°后会映射到 $(n+1-i,\;m+1-j)$。要满足中心对称，必须有
   $$
   a_{i,j} \;=\; a_{n+1-i,\;m+1-j}.
   $$
2. **操作限制**  
   只能将 'o' 变成 'p'，无法将 'p' 变成 'o'。  
3. **贪心配对**  
   - 将矩阵中所有 **互为旋转对称** 的格子两两配对。  
   - 对每一对 $(i,j)$ 和 $(n+1-i,m+1-j)$，如果它们不相同，则一定是一方为 'o'，一方为 'p'；只需把那一侧的 'o' 变为 'p'，需要 1 次操作。  
   - 中心格（当 $n,m$ 同时为奇数时）映射到自身，若为 'o'，保留不变也满足对称，无需操作。

4. **计数方案**  
   枚举所有 $(i,j)$，只处理“**字典序小于其映射位置**”的格子，以免重复。  
   - 条件：  
     ![image](/file/2/d60OsS31_XmumBkMKQfHI.png) 
   - 若 $a_{i,j}\neq a_{n+1-i,\;m+1-j}$ 则答案加 1。

整体时间复杂度 $O(nm)$，空间复杂度 $O(nm)$。

---

## C++

```cpp
#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int n, m;
    cin >> n >> m;
    vector<string> grid(n);
    for (int i = 0; i < n; i++) {
        cin >> grid[i];
    }

    int ans = 0;
    // 枚举“前半”格子，防止重复
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < m; j++) {
            int ii = n - 1 - i;
            int jj = m - 1 - j;
            // 只处理 (i,j) 在字典序上小于 (ii,jj) 的情况
            if (i < ii || (i == ii && j < jj)) {
                if (grid[i][j] != grid[ii][jj]) {
                    // 一方为 'o'，另一方为 'p'，将 'o'→'p'
                    ans++;
                }
            }
        }
    }

    cout << ans << "\n";
    return 0;
}
```
## Python

```python
import sys
input = sys.stdin.readline

def main():
    n, m = map(int, input().split())
    grid = [input().strip() for _ in range(n)]
    ans = 0

    for i in range(n):
        for j in range(m):
            ii, jj = n-1-i, m-1-j
            # 只处理前半对称配对
            if i < ii or (i == ii and j < jj):
                if grid[i][j] != grid[ii][jj]:
                    ans += 1

    print(ans)

if __name__ == "__main__":
    main()
```
## Java

```java
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.IOException;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String[] nm = br.readLine().split(" ");
        int n = Integer.parseInt(nm[0]);
        int m = Integer.parseInt(nm[1]);

        String[] grid = new String[n];
        for (int i = 0; i < n; i++) {
            grid[i] = br.readLine();
        }

        int ans = 0;
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < m; j++) {
                int ii = n - 1 - i;
                int jj = m - 1 - j;
                // 只处理字典序小于映射的位置
                if (i < ii || (i == ii && j < jj)) {
                    if (grid[i].charAt(j) != grid[ii].charAt(jj)) {
                        ans++;
                    }
                }
            }
        }

        System.out.println(ans);
    }
}
```