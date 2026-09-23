#include <bits/stdc++.h>
using namespace std;

int n, sx, sy, ex, ey, k;
long long countPaths = 0;

// 四个方向：上，下，左，右
int dx[4] = {-1, 1, 0, 0};
int dy[4] = {0, 0, -1, 1};

// 递归函数，当前坐标 (x, y)，已经走的步数 steps
void dfs(int x, int y, int steps) {
    // 如果当前坐标是终点，则计数加一
    if (x == ex && y == ey) {
        countPaths++;
        // 注意：即使达到终点，也可以选择继续移动，直到步数达到 k
        // 所以不在此处 return
    }
    // 如果已经达到最大步数，停止递归
    if (steps == k)
        return;
    // 尝试四个方向移动
    for(int dir = 0; dir < 4; dir++) {
        int newX = x + dx[dir];
        int newY = y + dy[dir];
        // 检查新位置是否在网格内
        if(newX >= 1 && newX <= n && newY >=1 && newY <=n) {
            dfs(newX, newY, steps + 1);
        }
    }
}

int main(){
    // 输入
    cin >> n;
    cin >> sx >> sy >> ex >> ey;
    cin >> k;
    
    // 开始递归，初始步数为0
    dfs(sx, sy, 0);
    
    // 输出结果
    cout << countPaths;
    return 0;
}
