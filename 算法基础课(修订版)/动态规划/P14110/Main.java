import java.util.Scanner;

public class LongestIncreasingSubsequence {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        
        // 读取数组的长度
        int n = scanner.nextInt();
        int[] a = new int[n];
        
        // 读取数组元素并存储
        for (int i = 0; i < n; i++) {
            a[i] = scanner.nextInt();
        }
        
        // 初始化动态规划数组 dp，所有值初始为 1
        int[] dp = new int[n];
        for (int i = 0; i < n; i++) {
            dp[i] = 1;
        }
        
        // 遍历每个元素，计算最长递增子序列
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < i; j++) {
                if (a[i] > a[j]) {
                    dp[i] = Math.max(dp[i], dp[j] + 1);
                }
            }
        }
        
        // 找到 dp 数组中的最大值
        int maxLength = 0;
        for (int i = 0; i < n; i++) {
            maxLength = Math.max(maxLength, dp[i]);
        }
        
        // 输出结果
        System.out.println(maxLength);
    }
}
