#include <bits/stdc++.h>
using namespace std;

class Solution {
public:
    vector<int> countShortestPaths(int n, vector<vector<int>>& guards) {
        int sy = n / 2;
        int sx = 0, ex = n - 1, ey = sy;
        vector<vector<char>> ban(n, vector<char>(n, 0));
        for (auto& g : guards) {
            int gx = g[0], gy = g[1];
            for (int dx = -1; dx <= 1; dx++)
                for (int dy = -1; dy <= 1; dy++) {
                    int nx = gx + dx, ny = gy + dy;
                    if (nx >= 0 && nx < n && ny >= 0 && ny < n) ban[nx][ny] = 1;
                }
        }
        if (ban[sx][sy] || ban[ex][ey]) return {0, 0};
        const int dirs[4][2] = {{1, 0}, {-1, 0}, {0, 1}, {0, -1}};
        vector<vector<int>> dist(n, vector<int>(n, -1));
        vector<vector<long long>> ways(n, vector<long long>(n, 0));
        deque<pair<int, int>> q;
        dist[sx][sy] = 0;
        ways[sx][sy] = 1;
        q.push_back({sx, sy});
        while (!q.empty()) {
            int x = q.front().first, y = q.front().second;
            q.pop_front();
            for (int k = 0; k < 4; k++) {
                int nx = x + dirs[k][0], ny = y + dirs[k][1];
                if (nx < 0 || nx >= n || ny < 0 || ny >= n || ban[nx][ny]) continue;
                if (dist[nx][ny] == -1) {
                    dist[nx][ny] = dist[x][y] + 1;
                    ways[nx][ny] = ways[x][y];
                    q.push_back({nx, ny});
                } else if (dist[nx][ny] == dist[x][y] + 1) {
                    ways[nx][ny] += ways[x][y];
                }
            }
        }
        if (dist[ex][ey] == -1) return {0, 0};
        return {(int)ways[ex][ey], dist[ex][ey] + 1};
    }
};
