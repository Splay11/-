import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Scanner;

public class Main {
    static final int INF = 1000000000;

    // 把非 0 格子当成城市，用状压 DP 求从中心出发并返回的最短回路
    static int minSteps(int[][] grid) {
        int n = grid.length;
        int m = grid[0].length;
        int sr = n / 2, sc = m / 2;
        // 点 0 固定为中心，其余点为中心以外的非 0 格子
        List<int[]> pts = new ArrayList<>();
        pts.add(new int[] {sr, sc});
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < m; j++) {
                if (grid[i][j] != 0 && (i != sr || j != sc)) {
                    pts.add(new int[] {i, j});
                }
            }
        }
        int k = pts.size();
        if (k == 1) {
            return 0;
        }
        int[][] dist = new int[k][k];
        for (int a = 0; a < k; a++) {
            for (int b = 0; b < k; b++) {
                dist[a][b] = Math.abs(pts.get(a)[0] - pts.get(b)[0])
                        + Math.abs(pts.get(a)[1] - pts.get(b)[1]);
            }
        }
        int full = 1 << k;
        // dp[mask][i]：已访问集合为 mask、当前停在 i 的最少步数
        int[][] dp = new int[full][k];
        for (int i = 0; i < full; i++) {
            Arrays.fill(dp[i], INF);
        }
        dp[1][0] = 0;
        for (int mask = 0; mask < full; mask++) {
            for (int i = 0; i < k; i++) {
                if (((mask >> i) & 1) == 0 || dp[mask][i] >= INF) {
                    continue;
                }
                for (int j = 0; j < k; j++) {
                    if (((mask >> j) & 1) != 0) {
                        continue;
                    }
                    int nxt = mask | (1 << j);
                    int cand = dp[mask][i] + dist[i][j];
                    if (cand < dp[nxt][j]) {
                        dp[nxt][j] = cand;
                    }
                }
            }
        }
        int end = full - 1;
        int ans = INF;
        // 访问完全部点后，还要走回中心
        for (int i = 0; i < k; i++) {
            int cand = dp[end][i] + dist[i][0];
            if (cand < ans) {
                ans = cand;
            }
        }
        return ans;
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int n = sc.nextInt();
        int m = sc.nextInt();
        int[][] grid = new int[n][m];
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < m; j++) {
                grid[i][j] = sc.nextInt();
            }
        }
        System.out.println(minSteps(grid));
        sc.close();
    }
}
