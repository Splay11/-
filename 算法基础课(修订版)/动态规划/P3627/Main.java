import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int n = sc.nextInt();
        int MOD = (int)1e9 + 7;
        int[][] dp = new int[n + 1][n + 1];
        dp[0][0] = 1; // 初始条件
        
        for (int i = 1; i <= n; i++) {
            for (int j = 0; j <= n; j++) {
                dp[i][j] = dp[i - 1][j]; // 不选数字i的方案数
                if (j >= i) {
                    dp[i][j] = (dp[i][j] + dp[i - 1][j - i]) % MOD; // 选数字i的方案数
                }
            }
        }
        
        System.out.println(dp[n][n]);
    }
}
