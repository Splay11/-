// 标准 DP：dp[j][k] 表示当前占用体积为 j、是否已触发优惠 k 时的最大货值
import java.util.Arrays;
import java.util.Scanner;

public class Main {
    static long maxValue(int n, int W, int T, int[] v, int[] w) {
        final long NEG = -1;
        // dp[vol][trig]：占用 vol、触发标记 trig 的最大货值
        long[][] dp = new long[W + 1][2];
        for (int i = 0; i <= W; i++) {
            Arrays.fill(dp[i], NEG);
        }
        dp[0][0] = 0;
        for (int i = 0; i < n; i++) {
            // 先复制上一轮，对应不装第 i 件
            long[][] newDp = new long[W + 1][2];
            for (int vol = 0; vol <= W; vol++) {
                newDp[vol][0] = dp[vol][0];
                newDp[vol][1] = dp[vol][1];
            }
            for (int vol = 0; vol <= W; vol++) {
                for (int trig = 0; trig <= 1; trig++) {
                    if (dp[vol][trig] < 0) {
                        continue;
                    }
                    // 装第 i 件：未触发用原体积，已触发用折半
                    int cost = trig == 1 ? v[i] / 2 : v[i];
                    int nvol = vol + cost;
                    if (nvol > W) {
                        continue;
                    }
                    // 装上后体积首次达到 T，之后才算触发
                    int ntrig = (trig == 1 || nvol >= T) ? 1 : 0;
                    long val = dp[vol][trig] + w[i];
                    if (val > newDp[nvol][ntrig]) {
                        newDp[nvol][ntrig] = val;
                    }
                }
            }
            dp = newDp;
        }
        // 所有可达状态里取最大货值
        long ans = 0;
        for (int vol = 0; vol <= W; vol++) {
            for (int trig = 0; trig <= 1; trig++) {
                if (dp[vol][trig] > ans) {
                    ans = dp[vol][trig];
                }
            }
        }
        return ans;
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        // 第一行：货物件数、载重上限、优惠阈值
        int n = sc.nextInt();
        int W = sc.nextInt();
        int T = sc.nextInt();
        int[] v = new int[n];
        int[] w = new int[n];
        for (int i = 0; i < n; i++) {
            v[i] = sc.nextInt();
            w[i] = sc.nextInt();
        }
        System.out.println(maxValue(n, W, T, v, w));
    }
}
