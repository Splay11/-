import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.StringTokenizer;

public class Main {
    // 状态压缩求最短巡回时长
    static int minTour(int m, int[] lo, int[] hi, int[][] dur) {
        int k = m - 1;
        int full = (1 << k) - 1;
        int inf = 1000000000;
        // dp[mask][u]：已送达集合为 mask、当前停在 u 时的最早到达时刻
        int[][] dp = new int[1 << k][m];
        for (int mask = 0; mask <= full; mask++) {
            for (int u = 0; u < m; u++) {
                dp[mask][u] = inf;
            }
        }
        // 时刻 0 停在仓站，还没送过任何客户
        dp[0][0] = 0;
        for (int mask = 0; mask <= full; mask++) {
            for (int u = 0; u < m; u++) {
                int now = dp[mask][u];
                if (now >= inf) {
                    continue;
                }
                // 枚举下一个尚未送达的客户
                for (int v = 1; v < m; v++) {
                    int bit = 1 << (v - 1);
                    if ((mask & bit) != 0) {
                        continue;
                    }
                    int t = now + dur[u][v];
                    // 早到必须等到可收货下界，等候计入总时长
                    if (t < lo[v]) {
                        t = lo[v];
                    }
                    // 迟到则这条转移非法
                    if (t > hi[v]) {
                        continue;
                    }
                    int nmask = mask | bit;
                    if (t < dp[nmask][v]) {
                        dp[nmask][v] = t;
                    }
                }
            }
        }
        int ans = inf;
        // 所有客户都送达后，从最后一站回到仓站
        for (int u = 1; u < m; u++) {
            if (dp[full][u] >= inf) {
                continue;
            }
            int t = dp[full][u] + dur[u][0];
            if (t < lo[0]) {
                t = lo[0];
            }
            if (t > hi[0]) {
                continue;
            }
            if (t < ans) {
                ans = t;
            }
        }
        return ans >= inf ? -1 : ans;
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int m = Integer.parseInt(br.readLine().trim());
        int[] lo = new int[m];
        int[] hi = new int[m];
        for (int p = 0; p < m; p++) {
            StringTokenizer st = new StringTokenizer(br.readLine());
            lo[p] = Integer.parseInt(st.nextToken());
            hi[p] = Integer.parseInt(st.nextToken());
        }
        int[][] dur = new int[m][m];
        for (int p = 0; p < m; p++) {
            StringTokenizer st = new StringTokenizer(br.readLine());
            for (int q = 0; q < m; q++) {
                dur[p][q] = Integer.parseInt(st.nextToken());
            }
        }
        System.out.println(minTour(m, lo, hi, dur));
    }
}
