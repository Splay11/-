import java.util.*;

public class Main {
    public static int coinChange(int[] coins, int amount) {
        int[] dp = new int[amount + 1];
        Arrays.fill(dp, Integer.MAX_VALUE); // 初始化 dp 数组，值为 INT_MAX
        dp[0] = 0; // 基础情况：金额为 0 时需要 0 个硬币

        for (int i = 1; i <= amount; i++) { // 遍历金额从 1 到 amount
            for (int coin : coins) { // 遍历每种硬币面额
                if (i >= coin && dp[i - coin] != Integer.MAX_VALUE) {
                    dp[i] = Math.min(dp[i], dp[i - coin] + 1); // 转移方程：选择硬币后的最优解
                }
            }
        }

        return dp[amount] == Integer.MAX_VALUE ? -1 : dp[amount]; // 检查是否能凑出目标金额
    }

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        // 输入硬币的种类数
        int n = scanner.nextInt();

        // 输入每种硬币的面额
        int[] coins = new int[n];
        for (int i = 0; i < n; i++) {
            coins[i] = scanner.nextInt();
        }

        // 输入目标金额
        int amount = scanner.nextInt();

        // 计算结果并输出
        int result = coinChange(coins, amount);
        System.out.println(result);
    }
}
