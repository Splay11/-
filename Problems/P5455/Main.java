import java.util.HashMap;
import java.util.Map;
import java.util.Scanner;

public class Main {
    // 把业务条目映射成二进制，每台机器变成覆盖掩码，再做 0-1 最短覆盖 DP
    static int minDevices(int[][] specs, int[] need) {
        Map<Integer, Integer> bit = new HashMap<>();
        int t = need.length;
        // 只关心业务点名的条目，给它们编号 0..t-1
        for (int i = 0; i < t; i++) {
            bit.put(need[i], i);
        }
        int[] covers = new int[specs.length];
        for (int i = 0; i < specs.length; i++) {
            int mask = 0;
            for (int x : specs[i]) {
                Integer b = bit.get(x);
                if (b != null) {
                    mask |= 1 << b;
                }
            }
            covers[i] = mask;
        }
        int full = (1 << t) - 1;
        int inf = t + 5;
        // dp[s]：覆盖集合恰好为 s 时的最少台数
        int[] dp = new int[1 << t];
        for (int i = 0; i <= full; i++) {
            dp[i] = inf;
        }
        dp[0] = 0;
        for (int c : covers) {
            if (c == 0) {
                continue;
            }
            // 倒序枚举，保证每台机器最多用一次
            for (int s = full; s >= 0; s--) {
                if (dp[s] >= inf) {
                    continue;
                }
                int ns = s | c;
                int v = dp[s] + 1;
                if (v < dp[ns]) {
                    dp[ns] = v;
                }
            }
        }
        return dp[full] >= inf ? 0 : dp[full];
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int d = sc.nextInt();
        int w = sc.nextInt();
        int t = sc.nextInt();
        int[][] specs = new int[d][w];
        for (int i = 0; i < d; i++) {
            for (int j = 0; j < w; j++) {
                specs[i][j] = sc.nextInt();
            }
        }
        int[] need = new int[t];
        for (int i = 0; i < t; i++) {
            need[i] = sc.nextInt();
        }
        sc.close();
        System.out.println(minDevices(specs, need));
    }
}
