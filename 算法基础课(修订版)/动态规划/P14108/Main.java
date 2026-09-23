import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        int n = scanner.nextInt();  // 读取输入的整数n，表示数组的长度
        int[] a = new int[n];  // 读取n个整数，存储在数组a中

        for (int i = 0; i < n; i++) {
            a[i] = scanner.nextInt();
        }

        int[] dp = new int[n + 1];  // 初始化前缀和数组dp，长度为n+1，dp[0]设为0

        // 计算前缀和
        for (int i = 1; i <= n; i++) {
            dp[i] = dp[i - 1] + a[i - 1];  // 当前前缀和等于前一个前缀和加上当前元素
            System.out.println(dp[i]);  // 输出当前的前缀和
        }
    }
}
