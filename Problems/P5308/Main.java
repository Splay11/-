import java.util.Scanner;

public class Main {
  static int solve(int r, int c, int[][] d) {
    // dp[i][j]：走到 (i, j) 的最小调节能耗
    int[][] dp = new int[r][c];
    // 先填第一行：只能一路向右
    for (int j = 1; j < c; j++) {
      dp[0][j] = dp[0][j - 1] + Math.abs(d[0][j] - d[0][j - 1]);
    }
    // 再填第一列：只能一路向下
    for (int i = 1; i < r; i++) {
      dp[i][0] = dp[i - 1][0] + Math.abs(d[i][0] - d[i - 1][0]);
    }
    // 其余格子取「从上走来」和「从左走来」的较小值
    for (int i = 1; i < r; i++) {
      for (int j = 1; j < c; j++) {
        int up = dp[i - 1][j] + Math.abs(d[i][j] - d[i - 1][j]);
        int left = dp[i][j - 1] + Math.abs(d[i][j] - d[i][j - 1]);
        dp[i][j] = Math.min(up, left);
      }
    }
    return dp[r - 1][c - 1];
  }

  public static void main(String[] args) {
    Scanner sc = new Scanner(System.in);
    int r = sc.nextInt();
    int c = sc.nextInt();
    int[][] d = new int[r][c];
    for (int i = 0; i < r; i++) {
      for (int j = 0; j < c; j++) d[i][j] = sc.nextInt();
    }
    System.out.println(solve(r, c, d));
    sc.close();
  }
}
