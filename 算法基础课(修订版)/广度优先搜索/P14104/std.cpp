#include <iostream>
#include <vector>
#include <queue>
using namespace std;

// 定义方向向量，分别表示上、下、左、右四个方向
int dx[4] = {-1, 1, 0, 0};
int dy[4] = {0, 0, -1, 1};

int shortestPath(vector<vector<int>> &grid, int m, int n, int x1, int y1, int x2, int y2) {
    // 检查起点和终点是否为墙
    if(grid[x1][y1] == 1 || grid[x2][y2] == 1) return -1;

    // 创建访问数组，初始化为未访问
    vector<vector<bool>> visited(m, vector<bool>(n, false));
    queue<pair<pair<int, int>, int>> q; // 队列中存储坐标及当前路径长度

    // 将起点加入队列，并标记为已访问
    q.push({{x1, y1}, 0});
    visited[x1][y1] = true;

    while(!q.empty()) {
        auto current = q.front();
        q.pop();

        int x = current.first.first;
        int y = current.first.second;
        int steps = current.second;

        // 如果当前坐标是目标点，返回路径长度
        if(x == x2 && y == y2) return steps;

        // 尝试向四个方向移动
        for(int i = 0; i < 4; ++i){
            int newX = x + dx[i];
            int newY = y + dy[i];

            // 检查新坐标是否在范围内，且是空白格子，且未被访问
            if(newX >=0 && newX < m && newY >=0 && newY < n 
               && grid[newX][newY] == 0 && !visited[newX][newY]){
                q.push({{newX, newY}, steps + 1});
                visited[newX][newY] = true; // 标记为已访问
            }
        }
    }

    // 如果队列为空仍未找到目标点，返回-1
    return -1;
}

int main(){
    int m, n;
    cin >> m >> n;
    vector<vector<int>> grid(m, vector<int>(n, 0));
    // 读取矩阵
    for(int i = 0; i < m; ++i){
        for(int j = 0; j < n; ++j){
            char c;
            cin >> c;
            grid[i][j] = c - '0';
        }
    }
    int x1, y1, x2, y2;
    cin >> x1 >> y1 >> x2 >> y2;
    cout << shortestPath(grid, m, n, x1, y1, x2, y2);
    return 0;
}
