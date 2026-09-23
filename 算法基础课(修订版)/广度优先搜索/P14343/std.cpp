#include <iostream>
#include <vector>
#include <queue>

using namespace std;

int n, m;  // 定义全局变量行数和列数
vector<vector<int>> mp;  // 输入矩阵，存储区域信息
vector<vector<int>> d;   // 记录到每个点的最短距离，初始化为-1表示不可达

// 计算所有小区到垃圾站的最短距离之和
int solve() {
    int ans = 0;  // 初始化答案
    for (int i = 0; i < n; i++) {  // 遍历每一行
        for (int j = 0; j < m; j++) {  // 遍历每一列
            if (mp[i][j] == 1 && d[i][j] != -1) {  // 如果是小区且可达
                ans += d[i][j];  // 累加到总距离
            }
        }
    }
    return ans;  // 返回计算的总和
}

// 广度优先搜索更新距离矩阵
void bfs() {
    queue<pair<int, int>> q;  // 创建队列用于存储位置
    // 将所有垃圾站(值为0)的位置加入队列，并初始化它们的距离为0
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < m; j++) {
            if (mp[i][j] == 0) {  // 找到垃圾站
                q.push({i, j});  // 加入队列
                d[i][j] = 0;  // 垃圾站的距离设为0
            }
        }
    }

    // 定义四个方向的移动（右、左、下、上）
    int dx[4] = {0, 0, 1, -1};
    int dy[4] = {1, -1, 0, 0};
    
    // 开始BFS遍历
    while (!q.empty()) {  // 当队列不为空时
        auto current = q.front();  // 获取队头元素
        q.pop();  // 弹出队头元素
        int x = current.first;  // 当前x坐标
        int y = current.second;  // 当前y坐标

        for (int i = 0; i < 4; i++) {  // 遍历四个方向
            int nx = x + dx[i];  // 计算新x坐标
            int ny = y + dy[i];  // 计算新y坐标
            // 检查新点是否在边界内并且没有被访问过且不是障碍
            if (nx >= 0 && nx < n && ny >= 0 && ny < m && d[nx][ny] == -1 && mp[nx][ny] != -1) {
                d[nx][ny] = d[x][y] + 1;  // 更新新点的距离
                q.push({nx, ny});  // 将新点加入队列
            }
        }
    }
}

int main() {
    cin >> n >> m;  // 读取行数和列数
    mp.resize(n, vector<int>(m));  // 初始化输入矩阵
    d.resize(n, vector<int>(m, -1));  // 初始化距离矩阵为-1

    // 读取输入矩阵
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < m; j++) {
            cin >> mp[i][j];  // 输入区域信息
        }
    }

    // 执行广度优先搜索更新最短距离
    bfs();
    // 输出结果，即所有小区到垃圾站的最小距离和
    cout << solve() << endl;

    return 0;  // 程序结束
}
