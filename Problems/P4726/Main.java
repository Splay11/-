import java.util.*;

public class Solution {
    private int n, m, si, sj, ei, ej, maxDiff;
    private int[][] grid;
    private long[][] memo;
    private boolean[][] done;

    public long countHikingPaths(int[][] grid, int maxDiff) {
        this.grid = grid;
        this.maxDiff = maxDiff;
        n = grid.length;
        m = grid[0].length;
        int mn = grid[0][0], mx = grid[0][0];
        for (int i = 0; i < n; i++)
            for (int j = 0; j < m; j++) {
                mn = Math.min(mn, grid[i][j]);
                mx = Math.max(mx, grid[i][j]);
            }
        for (int i = 0; i < n; i++)
            for (int j = 0; j < m; j++) {
                if (grid[i][j] == mn) {
                    si = i;
                    sj = j;
                }
                if (grid[i][j] == mx) {
                    ei = i;
                    ej = j;
                }
            }
        memo = new long[n][m];
        done = new boolean[n][m];
        return dfs(si, sj);
    }

    private long dfs(int i, int j) {
        if (i == ei && j == ej) return 1;
        if (done[i][j]) return memo[i][j];
        done[i][j] = true;
        long tot = 0;
        int h = grid[i][j];
        int[][] dirs = {{1, 0}, {-1, 0}, {0, 1}, {0, -1}};
        for (int[] d : dirs) {
            int ni = i + d[0], nj = j + d[1];
            if (ni < 0 || ni >= n || nj < 0 || nj >= m) continue;
            int nh = grid[ni][nj];
            int diff = nh - h;
            if (diff > 0 && diff <= maxDiff) tot += dfs(ni, nj);
        }
        memo[i][j] = tot;
        return tot;
    }
}
