## 解题思路

因为题目中 $n \times m \le 16$，所以整个棋盘最多只有 $16$ 个格子。
每个格子只有两种选择：放黑子或白子，因此总布局数最多为

$$
2^{n \times m} \le 2^{16} = 65536
$$

这个数量非常小，可以直接使用**二进制枚举 + 图的连通块搜索**来判断每一种布局是否合法。

### 核心思路

把每一种布局看成一个长度为 $n \times m$ 的二进制状态：

* $0$ 表示白子
* $1$ 表示黑子

对于每个状态：

1. 遍历整个棋盘，找到所有还没访问过的格子。
2. 从这个格子出发，用 **BFS / DFS** 搜索与它**上下左右相邻且颜色相同**的所有格子，得到一个极大连通块。
3. 统计该连通块大小。
4. 如果某个极大连通块大小是偶数，则该布局不合法。
5. 如果所有极大连通块大小都是奇数，则该布局合法，答案加一。

### 为什么这样做是对的

题目要求每个**极大连通块**都是优秀的，而极大连通块本质上就是：

* 在同色条件下，
* 按上下左右连通，
* 形成的最大连通区域。

所以只要对每种布局求出所有同色连通块，并检查它们的大小是否全为奇数即可。

---

## 复杂度分析

设总格子数为

$$
k = n \times m
$$

总共有 $2^k$ 种布局。
对于每一种布局，最多遍历整个棋盘一次并做若干次 BFS/DFS，时间复杂度为 $O(k)$。

所以总时间复杂度为：

$$
O(2^k \times k)
$$

由于 $k \le 16$，所以最多约为：

$$
2^{16} \times 16 \approx 10^6
$$

完全可以通过。

空间复杂度主要是访问数组和队列：

$$
O(k)
$$

---

## 代码实现

### Python

```python
from collections import deque


# 判断一个状态是否满足所有极大连通块大小均为奇数
def check(state, n, m):
    visited = [[False] * m for _ in range(n)]
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    # 获取某个位置的颜色，0表示白子，1表示黑子
    def get_color(x, y):
        idx = x * m + y
        return (state >> idx) & 1

    for i in range(n):
        for j in range(m):
            if visited[i][j]:
                continue

            # 从当前点开始BFS，统计同色连通块大小
            color = get_color(i, j)
            q = deque()
            q.append((i, j))
            visited[i][j] = True
            size = 0

            while q:
                x, y = q.popleft()
                size += 1

                for dx, dy in dirs:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < n and 0 <= ny < m and not visited[nx][ny]:
                        if get_color(nx, ny) == color:
                            visited[nx][ny] = True
                            q.append((nx, ny))

            # 如果某个极大连通块大小为偶数，则不合法
            if size % 2 == 0:
                return False

    return True


# 统计所有合法布局数量
def solve(n, m):
    total = n * m
    ans = 0

    # 枚举每一种黑白布局
    for state in range(1 << total):
        if check(state, n, m):
            ans += 1

    return ans


if __name__ == "__main__":
    n, m = map(int, input().split())
    print(solve(n, m))
```

### Java

```java
import java.util.LinkedList;
import java.util.Queue;
import java.util.Scanner;

public class Main {

    // 判断一个状态是否满足所有极大连通块大小均为奇数
    public static boolean check(int state, int n, int m) {
        boolean[][] visited = new boolean[n][m];
        int[] dx = {-1, 1, 0, 0};
        int[] dy = {0, 0, -1, 1};

        for (int i = 0; i < n; i++) {
            for (int j = 0; j < m; j++) {
                if (visited[i][j]) {
                    continue;
                }

                // 当前格子的颜色
                int color = (state >> (i * m + j)) & 1;

                // BFS统计同色连通块大小
                Queue<int[]> queue = new LinkedList<>();
                queue.offer(new int[]{i, j});
                visited[i][j] = true;
                int size = 0;

                while (!queue.isEmpty()) {
                    int[] cur = queue.poll();
                    int x = cur[0];
                    int y = cur[1];
                    size++;

                    for (int k = 0; k < 4; k++) {
                        int nx = x + dx[k];
                        int ny = y + dy[k];

                        if (nx >= 0 && nx < n && ny >= 0 && ny < m && !visited[nx][ny]) {
                            int nextColor = (state >> (nx * m + ny)) & 1;
                            if (nextColor == color) {
                                visited[nx][ny] = true;
                                queue.offer(new int[]{nx, ny});
                            }
                        }
                    }
                }

                // 如果存在偶数大小连通块，则不合法
                if (size % 2 == 0) {
                    return false;
                }
            }
        }

        return true;
    }

    // 统计所有合法布局数量
    public static int solve(int n, int m) {
        int total = n * m;
        int ans = 0;

        // 枚举所有状态
        for (int state = 0; state < (1 << total); state++) {
            if (check(state, n, m)) {
                ans++;
            }
        }

        return ans;
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int n = sc.nextInt();
        int m = sc.nextInt();
        System.out.println(solve(n, m));
    }
}
```

### C++

```cpp
#include <iostream>
#include <queue>
#include <vector>
using namespace std;


// 判断一个状态是否满足所有极大连通块大小均为奇数
bool check(int state, int n, int m) {
    vector<vector<bool>> visited(n, vector<bool>(m, false));
    int dx[4] = {-1, 1, 0, 0};
    int dy[4] = {0, 0, -1, 1};

    for (int i = 0; i < n; i++) {
        for (int j = 0; j < m; j++) {
            if (visited[i][j]) {
                continue;
            }

            // 当前格子的颜色
            int color = (state >> (i * m + j)) & 1;

            // BFS统计同色连通块大小
            queue<pair<int, int>> q;
            q.push({i, j});
            visited[i][j] = true;
            int size = 0;

            while (!q.empty()) {
                pair<int, int> cur = q.front();
                q.pop();
                int x = cur.first;
                int y = cur.second;
                size++;

                for (int k = 0; k < 4; k++) {
                    int nx = x + dx[k];
                    int ny = y + dy[k];

                    if (nx >= 0 && nx < n && ny >= 0 && ny < m && !visited[nx][ny]) {
                        int nextColor = (state >> (nx * m + ny)) & 1;
                        if (nextColor == color) {
                            visited[nx][ny] = true;
                            q.push({nx, ny});
                        }
                    }
                }
            }

            // 如果存在偶数大小连通块，则不合法
            if (size % 2 == 0) {
                return false;
            }
        }
    }

    return true;
}


// 统计所有合法布局数量
int solve(int n, int m) {
    int total = n * m;
    int ans = 0;

    // 枚举所有状态
    for (int state = 0; state < (1 << total); state++) {
        if (check(state, n, m)) {
            ans++;
        }
    }

    return ans;
}


int main() {
    int n, m;
    cin >> n >> m;
    cout << solve(n, m) << endl;
    return 0;
}
```