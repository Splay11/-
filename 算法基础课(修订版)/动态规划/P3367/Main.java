import java.util.Scanner;

public class Main {
    static final int MOD = 1000000007;

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int n = sc.nextInt();
        
        // 创建一个 (n+1) x (n+1) 的 dp 表
        int[][] dp = new int[n + 1][n + 1];
        
        // 初始化 dp[0][0] = 1
        dp[0][0] = 1;

        // 动态规划求解
        for (int i = 1; i <= n; i++) {
            for (int j = 0; j <= n; j++) {
                dp[i][j] = dp[i - 1][j];  // 不使用当前数 i
                if (j >= i) {
                    dp[i][j] = (dp[i][j] + dp[i][j - i]) % MOD;  // 使用当前数 i
                }
            }
        }

        // 输出结果
        System.out.println(dp[n][n]);
    }
}
