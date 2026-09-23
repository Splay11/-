#include <algorithm>
#include <cstring>
#include <functional>
#include <vector>

using namespace std;

class Solution {
   public:
    long long countHikingPaths(vector<vector<int>>& grid, int maxDiff) {
        int n = (int)grid.size();
        int m = (int)grid[0].size();
        int mn = grid[0][0], mx = grid[0][0];
        for (int i = 0; i < n; i++)
            for (int j = 0; j < m; j++) {
                mn = min(mn, grid[i][j]);
                mx = max(mx, grid[i][j]);
            }
        int si = -1, sj = -1, ei = -1, ej = -1;
        for (int i = 0; i < n; i++)
            for (int j = 0; j < m; j++) {
                if (grid[i][j] == mn) si = i, sj = j;
                if (grid[i][j] == mx) ei = i, ej = j;
            }
        static long long memo[12][12];
        static int vis[12][12];
        static int stamp = 1;
        ++stamp;
        const int dirs[4][2] = {{1, 0}, {-1, 0}, {0, 1}, {0, -1}};
        function<long long(int, int)> dfs = [&](int i, int j) -> long long {
            if (i == ei && j == ej) return 1;
            if (vis[i][j] == stamp) return memo[i][j];
            vis[i][j] = stamp;
            long long tot = 0;
            int h = grid[i][j];
            for (int k = 0; k < 4; k++) {
                int ni = i + dirs[k][0], nj = j + dirs[k][1];
                if (ni < 0 || ni >= n || nj < 0 || nj >= m) continue;
                int nh = grid[ni][nj];
                int d = nh - h;
                if (d > 0 && d <= maxDiff) tot += dfs(ni, nj);
            }
            memo[i][j] = tot;
            return tot;
        };
        return dfs(si, sj);
    }
};
