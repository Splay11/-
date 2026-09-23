import java.util.Scanner;

public class Main {
    // 当前行动者从 a[i..j] 能拿到的最大得分
    static long firstScore(int[] a) {
        int n = a.length;
        // pre[k] 为前 k 个数的和，用来 O(1) 求区间和
        long[] pre = new long[n + 1];
        for (int i = 0; i < n; i++) {
            pre[i + 1] = pre[i] + a[i];
        }
        // dp[i][j]：轮到当前玩家时，从下标 i..j 能拿到的最大得分
        long[][] dp = new long[n][n];
        for (int i = 0; i < n; i++) {
            dp[i][i] = a[i];
        }
        // 按区间长度从小到大填表
        for (int length = 2; length <= n; length++) {
            for (int i = 0; i + length - 1 < n; i++) {
                int j = i + length - 1;
                long tot = pre[j + 1] - pre[i];
                // 取左端则对手得 dp[i+1][j]；取右端则对手得 dp[i][j-1]
                // 当前得分 = 区间和 - 对手得分，应让对手拿到的更少
                long opp = dp[i + 1][j] < dp[i][j - 1] ? dp[i + 1][j] : dp[i][j - 1];
                dp[i][j] = tot - opp;
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
        System.out.println(firstScore(a));
        sc.close();
    }
}
