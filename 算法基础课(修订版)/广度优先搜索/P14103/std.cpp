#include <iostream>
#include <vector>
#include <queue>

using namespace std;

int main(){
    int n, m;
    // 读取迷宫的行数和列数
    cin >> n >> m;
    
    // 初始化迷宫地图
    vector<vector<int>> maze(n, vector<int>(m));
    for(int i = 0; i < n; ++i){
        for(int j = 0; j < m; ++j){
            cin >> maze[i][j];
        }
    }
    
    int x1, y1, x2, y2;
    // 读取起点和终点的坐标
    cin >> x1 >> y1 >> x2 >> y2;
    
    // 检查起点和终点是否在迷宫范围内，并且不是墙壁
    if(x1 < 0 || x1 >= n || y1 < 0 || y1 >= m || 
       x2 < 0 || x2 >= n || y2 < 0 || y2 >= m ||
       maze[x1][y1] == 1 || maze[x2][y2] == 1){
        cout << "NO";
        return 0;
    }
    
    // 初始化访问数组
    vector<vector<bool>> visited(n, vector<bool>(m, false));
    // 定义四个移动方向：上、下、左、右
    int dx[4] = {-1, 1, 0, 0};
    int dy[4] = {0, 0, -1, 1};
    
    // 使用队列进行 BFS
    queue<pair<int, int>> q;
    q.push({x1, y1});
    visited[x1][y1] = true;
    
    bool found = false;
    
    while(!q.empty()){
        pair<int, int> current = q.front();
        q.pop();
        
        // 如果当前点是终点，设置 found 为 true 并跳出循环
        if(current.first == x2 && current.second == y2){
            found = true;
            break;
        }
        
        // 尝试四个方向移动
        for(int i = 0; i < 4; ++i){
            int newX = current.first + dx[i];
            int newY = current.second + dy[i];
            
            // 检查新位置是否在迷宫范围内，且是通路，且未被访问过
            if(newX >=0 && newX < n && newY >=0 && newY < m &&
               maze[newX][newY] == 0 && !visited[newX][newY]){
                q.push({newX, newY});
                visited[newX][newY] = true;
            }
        }
    }
    
    // 根据是否找到终点输出结果
    if(found){
        cout << "YES";
    }
    else{
        cout << "NO";
    }
    
    return 0;
}
