import java.io.*;
import java.util.*;

public class Main {
    static final int MOD = 1_000_000_007;

    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StringTokenizer st = new StringTokenizer(br.readLine());
        int q = Integer.parseInt(st.nextToken());
        StringBuilder out = new StringBuilder();
        while (q-- > 0) {
            st = new StringTokenizer(br.readLine());
            int m = Integer.parseInt(st.nextToken());
            long d = Long.parseLong(st.nextToken());
            st = new StringTokenizer(br.readLine());
            long[] h = new long[m];
            for (int i = 0; i < m; i++) h[i] = Long.parseLong(st.nextToken());
            // 滚动 DP：单人组 / 相邻可配对则再加前前状态
            long dp0 = 1, dp1 = 1;
            for (int i = 1; i < m; i++) {
                long nd = dp1;
                if (h[i] - h[i - 1] <= d) nd = (nd + dp0) % MOD;
                dp0 = dp1;
                dp1 = nd;
            }
            out.append(m == 0 ? 1 : dp1).append('\n');
        }
        System.out.print(out);
    }
}
