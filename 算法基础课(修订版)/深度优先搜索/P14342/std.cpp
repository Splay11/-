#include <bits/stdc++.h>
using namespace std;

int n, k;
bool vis[105][105];  // 访问状态数组

// 深度优先搜索函数
int dfs(int x, int y) {
    if (x == n) return 0;  // 递归边界：到达最后一行

    // 计算下一个搜索位置
    int nextX = (y == n - 1) ? x + 1 : x;
    int nextY = (y == n - 1) ? 0 : y + 1;

    int res = 0;

    // 判断是否能放置2x2方块
    if (x + 1 < n && y + 1 < n && !vis[x][y] && !vis[x + 1][y] && !vis[x][y + 1] && !vis[x + 1][y + 1]) {
        // 标记格子为已访问
        vis[x][y] = vis[x + 1][y] = vis[x][y + 1] = vis[x + 1][y + 1] = true;

        res = max(res, dfs(nextX, nextY) + 1);  // 递归继续搜索

        // 回溯，重置访问状态
        vis[x][y] = vis[x + 1][y] = vis[x][y + 1] = vis[x + 1][y + 1] = false;
    }

    // 不放置方块，继续搜索
    res = max(res, dfs(nextX, nextY));

    return res;
}

int main() {
    cin >> n >> k;
  
    for (int i = 0; i < k; i++) {
        int x, y;
        cin >> x >> y;
        vis[x][y] = true;  // 读取障碍物的位置
    }

    cout << dfs(0, 0) << endl;  // 从 (0, 0) 开始搜索
    return 0;
}
