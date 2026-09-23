#include <iostream>
#include <vector>
#include <string>
#include <queue>
#include <utility>
using namespace std;

void add_cell(const vector<string>& grid, vector<vector<char>>& vis,
              queue<pair<int, int>>& q, int i, int j) {
    int h = (int)grid.size();
    int w = (int)grid[0].size();
    if (i < 0 || i >= h || j < 0 || j >= w) {
        return;
    }
    if (grid[i][j] != 'V' || vis[i][j]) {
        return;
    }
    vis[i][j] = 1;
    q.push(make_pair(i, j));
}

int count_closed(const vector<string>& grid) {
    int h = (int)grid.size();
    int w = (int)grid[0].size();
    vector<vector<char>> vis(h, vector<char>(w, 0));
    queue<pair<int, int>> q;

    // 从边界上的村庄出发，能走到的都是自由村庄
    for (int j = 0; j < w; j++) {
        add_cell(grid, vis, q, 0, j);
        add_cell(grid, vis, q, h - 1, j);
    }
    for (int i = 0; i < h; i++) {
        add_cell(grid, vis, q, i, 0);
        add_cell(grid, vis, q, i, w - 1);
    }

    int di[4] = {1, -1, 0, 0};
    int dj[4] = {0, 0, 1, -1};
    while (!q.empty()) {
        int i = q.front().first;
        int j = q.front().second;
        q.pop();
        for (int k = 0; k < 4; k++) {
            add_cell(grid, vis, q, i + di[k], j + dj[k]);
        }
    }

    int ans = 0;
    for (int i = 0; i < h; i++) {
        for (int j = 0; j < w; j++) {
            // 没被边界搜到的村庄就是封闭领地
            if (grid[i][j] == 'V' && !vis[i][j]) {
                ans++;
            }
        }
    }
    return ans;
}

int main() {
    int h, w;
    cin >> h >> w;
    vector<string> grid(h);
    for (int i = 0; i < h; i++) {
        cin >> grid[i];
    }
    cout << count_closed(grid) << endl;
    return 0;
}
