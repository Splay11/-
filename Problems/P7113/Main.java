import java.util.Scanner;

public class Main {
    // 删完数组 a[i..j] 的最小代价
    static long minCost(int[] a) {
        int n = a.length;
        // dp[i][j]：把下标 i..j 这一段全部删完的最小代价
        long[][] dp = new long[n][n];
        // 长度为 1：当前长度是 1，代价就是元素本身
        for (int i = 0; i < n; i++) {
            dp[i][i] = a[i];
        }
        // 按区间长度从小到大填表，保证转移时子区间已经算好
        for (int length = 2; length <= n; length++) {
            for (int i = 0; i + length - 1 < n; i++) {
                int j = i + length - 1;
                // 先删左端 a[i]，代价为当前长度 * a[i]，再加上删完剩余区间的最优代价
                long left = (long) length * a[i] + dp[i + 1][j];
                // 先删右端 a[j]，同理
                long right = (long) length * a[j] + dp[i][j - 1];
                dp[i][j] = left < right ? left : right;
            }
        }
        return dp[0][n - 1];
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int n = sc.nextInt();
        int[] a = new int[n];
        for (int i = 0; i < n; i++) {
            a[i] = sc.nextInt();
        }
        System.out.println(minCost(a));
        sc.close();
    }
}
