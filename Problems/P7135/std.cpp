#include <iostream>
#include <utility>
#include <vector>
using namespace std;

int di[4] = {1, -1, 0, 0};
int dj[4] = {0, 0, 1, -1};

// 统计 grid2 里有多少座岛，整座岛的格子在 grid1 里也都是陆地
// 用栈做 DFS，m、n 到 500，蛇形岛递归会爆
int solve(const vector<vector<int>>& grid1, vector<vector<int>> g2) {
    int m = (int)g2.size();
    int n = (int)g2[0].size();
    int ans = 0;
    vector<pair<int, int>> stack;
    for (int i = 0; i < m; i++) {
        for (int j = 0; j < n; j++) {
            if (g2[i][j] != 1) {
                continue;
            }
            // 从当前格出发走完这座 grid2 岛
            bool ok = true;
            stack.clear();
            stack.push_back({i, j});
            g2[i][j] = 0;
            while (!stack.empty()) {
                int x = stack.back().first;
                int y = stack.back().second;
                stack.pop_back();
                if (grid1[x][y] == 0) {
                    // 这座岛有一块在 grid1 里是水，就不能算子岛屿
                    ok = false;
                }
                for (int k = 0; k < 4; k++) {
                    int ni = x + di[k];
                    int nj = y + dj[k];
                    if (ni >= 0 && ni < m && nj >= 0 && nj < n && g2[ni][nj] == 1) {
                        g2[ni][nj] = 0;
                        stack.push_back({ni, nj});
                    }
                }
            }
            if (ok) {
                ans++;
            }
        }
    }
    return ans;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int m, n;
    cin >> m >> n;
    vector<vector<int>> grid1(m, vector<int>(n));
    vector<vector<int>> grid2(m, vector<int>(n));
    for (int i = 0; i < m; i++) {
        for (int j = 0; j < n; j++) {
            cin >> grid1[i][j];
        }
    }
    for (int i = 0; i < m; i++) {
        for (int j = 0; j < n; j++) {
            cin >> grid2[i][j];
        }
    }
    cout << solve(grid1, grid2) << '\n';
    return 0;
}
