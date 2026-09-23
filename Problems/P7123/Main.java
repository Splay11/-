import java.util.Scanner;

public class Main {
    // 求两个数组最长公共子数组（必须连续）的长度
    static int longestCommonSubarray(int[] a, int[] b) {
        int n = a.length;
        int m = b.length;
        // dp[i][j]：以 a[i-1]、b[j-1] 结尾的公共子数组最长能有多长
        int[][] dp = new int[n + 1][m + 1];
        int ans = 0;
        for (int i = 1; i <= n; i++) {
            for (int j = 1; j <= m; j++) {
                if (a[i - 1] == b[j - 1]) {
                    // 当前这一对相等，长度就是左上角那格再加 1
                    dp[i][j] = dp[i - 1][j - 1] + 1;
                    if (dp[i][j] > ans) {
                        ans = dp[i][j];
                    }
                }
                // 不相等时 dp[i][j] 保持 0：公共子数组在这里断开
            }
        }
        return ans;
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int n = sc.nextInt();
        int m = sc.nextInt();
        int[] a = new int[n];
        int[] b = new int[m];
        for (int i = 0; i < n; i++) {
            a[i] = sc.nextInt();
        }
        for (int i = 0; i < m; i++) {
            b[i] = sc.nextInt();
        }
        sc.close();
        System.out.println(longestCommonSubarray(a, b));
    }
}
