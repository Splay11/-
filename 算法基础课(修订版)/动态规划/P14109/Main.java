import java.util.Scanner;

public class Main{
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        
        // 读取数组的长度
        int n = scanner.nextInt();
        int[] a = new int[n + 1]; // 在数组前添加一个元素 0

        // 读取数组元素并存储
        for (int i = 1; i <= n; i++) {
            a[i] = scanner.nextInt();
        }
        
        // 初始化动态规划数组 dp
        int[] dp = new int[n + 1];

        // 遍历数组，计算每个位置的最大子数组和
        for (int i = 1; i <= n; i++) {
            dp[i] = Math.max(dp[i - 1] + a[i], a[i]); // 状态转移方程
        }

        // 找到所有 dp 值中的最大值
        int maxSum = dp[1];
        for (int i = 2; i <= n; i++) {
            maxSum = Math.max(maxSum, dp[i]);
        }
        
        // 输出结果
        System.out.println(maxSum);
    }
}
