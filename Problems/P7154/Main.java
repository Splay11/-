import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.IOException;
import java.util.StringTokenizer;

public class Main {
    // dp[i][j] 表示走到 (i,j) 的最小路径和
    static int solve(int[][] dp, int m, int n) {
        // 第一列只能一直往下
        for (int i = 1; i < m; i++) {
            dp[i][0] += dp[i - 1][0];
        }
        // 第一行只能一直往右
        for (int j = 1; j < n; j++) {
            dp[0][j] += dp[0][j - 1];
        }
        for (int i = 1; i < m; i++) {
            for (int j = 1; j < n; j++) {
                // 只能从上或从左走来
                int up = dp[i - 1][j];
                int left = dp[i][j - 1];
                dp[i][j] += Math.min(up, left);
            }
        }
        return dp[m - 1][n - 1];
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StringTokenizer st = new StringTokenizer(br.readLine());
        int m = Integer.parseInt(st.nextToken());
        int n = Integer.parseInt(st.nextToken());
        int[][] grid = new int[m][n];
        for (int i = 0; i < m; i++) {
            st = new StringTokenizer(br.readLine());
            for (int j = 0; j < n; j++) {
                grid[i][j] = Integer.parseInt(st.nextToken());
            }
        }
        System.out.println(solve(grid, m, n));
    }
}
