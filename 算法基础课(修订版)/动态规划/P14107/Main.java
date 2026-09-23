import java.util.Scanner;

public class Main{
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        int n = scanner.nextInt();  // 读取输入的整数n，表示网格的大小（n x n）

        // 初始化二维动态规划数组dp，大小为n x n，所有元素初始为0
        int[][] dp = new int[n][n];

        dp[0][0] = 1;  // 设置起点dp[0][0]为1，表示从起点到起点有1种路径

        // 遍历每一个网格单元
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                if (i > 0) {
                    dp[i][j] += dp[i - 1][j];  // 如果不是第一行，则可以从上方单元到达当前单元
                }
                if (j > 0) {
                    dp[i][j] += dp[i][j - 1];  // 如果不是第一列，则可以从左侧单元到达当前单元
                }
            }
        }

        System.out.println(dp[n - 1][n - 1]);  // 输出从起点(0,0)到终点(n-1,n-1)的路径总数
    }
}
