#include <bits/stdc++.h>
using namespace std;

int n, k;  // n: 迷宫大小，k: 最大步数
int a[100][100];  // 存储迷宫中每个格子的辐射值

// BFS函数，检查是否可以在k步内到达终点，且所有经过的格子辐射值 ≤ val
bool bfs(int val) {
    // 检查起点和终点的辐射值是否符合
    if (a[0][0] > val || a[n-1][n-1] > val) return false;

    // 定义移动方向：右、左、下、上
    int dx[4] = {0, 0, 1, -1};  // x方向的变化
    int dy[4] = {1, -1, 0, 0};  // y方向的变化

    // 距离数组，记录每个格子的最短步数
    vector<vector<int>> dist(n, vector<int>(n, -1));  // 初始化为-1，表示未访问
    dist[0][0] = 0;  // 起点的步数为0

    // 使用队列进行BFS，存储x, y坐标
    queue<pair<int, int>> q;
    q.push({0, 0});  // 将起点入队

    while (!q.empty()) {
        pair<int, int> current = q.front(); q.pop();  // 获取队首元素
        int x = current.first;  // 当前x坐标
        int y = current.second;  // 当前y坐标
        int steps = dist[x][y];  // 当前步数

        // 如果到达终点，检查步数是否 ≤ K
        if (x == n-1 && y == n-1) {
            return steps <= k;  // 若步数小于等于K，返回true
        }

        // 遍历四个方向
        for (int i = 0; i < 4; i++) {
            int nx = x + dx[i];  // 计算新x坐标
            int ny = y + dy[i];  // 计算新y坐标
            // 检查边界
            if (nx < 0 || nx >= n || ny < 0 || ny >= n) continue;  // 超出边界则跳过
            // 检查辐射值和是否已访问
            if (a[nx][ny] > val || dist[nx][ny] != -1) continue;  // 辐射值超标或已访问则跳过
            // 检查步数是否超过K
            if (steps + 1 > k) continue;  // 若步数超过K，则跳过
            // 更新步数并加入队列
            dist[nx][ny] = steps + 1;  // 更新当前格子的步数
            q.push({nx, ny});  // 将新位置入队
        }
    }

    // 如果无法到达终点
    return false;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(0);
    // 读取n和k
    cin >> n >> k;
    // 读取迷宫的辐射值
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            cin >> a[i][j];  // 输入辐射值
        }
    }

    // 二分查找的初始边界
    int left = max(a[0][0], a[n-1][n-1]);  // 最小防护能力
    int right = INT32_MIN;  // 最大防护能力
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            right = max(right, a[i][j]);  // 找到迷宫中辐射值的最大值
        }
    }

    int answer = right;  // 初始化答案为最大辐射值
    while (left <= right) {
        int mid = left + (right - left) / 2;  // 中间值
        if (bfs(mid)) {  // 如果可以到达终点
            answer = mid;  // 更新答案为当前mid
            right = mid - 1;  // 尝试更小的防护能力
        } else {
            left = mid + 1;  // 增加防护能力
        }
    }

    // 输出结果
    cout << answer;  // 输出最低防护能力
    return 0;
}
