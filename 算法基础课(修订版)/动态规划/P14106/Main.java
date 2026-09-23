import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        int n = scanner.nextInt();  // 读取输入的整数n

        int[] dp = new int[n + 2];  // 初始化动态规划数组，长度为n+2，防止下标越界
        dp[1] = 1;  // 第1个位置的值设为1
        dp[2] = 2;  // 第2个位置的值设为2

        for (int i = 3; i <= n; i++) {
            dp[i] = dp[i - 1] + dp[i - 2];  // 当前位的值等于前两位的和
        }

        System.out.println(dp[n]);  // 输出第n个位置的值
    }
}
