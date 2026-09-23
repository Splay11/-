import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.StringTokenizer;

public class Main {
    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StringTokenizer st = new StringTokenizer(br.readLine());
        int n = Integer.parseInt(st.nextToken());
        int W = Integer.parseInt(st.nextToken());
        // dp[j]：承重不超过 j 时的最大价值
        long[] dp = new long[W + 1];
        for (int i = 0; i < n; i++) {
            st = new StringTokenizer(br.readLine());
            int w = Integer.parseInt(st.nextToken());
            long v = Long.parseLong(st.nextToken());
            // 倒序保证 0-1（每个物品至多一次）
            for (int j = W; j >= w; j--) {
                long cand = dp[j - w] + v;
                if (cand > dp[j]) {
                    dp[j] = cand;
                }
            }
        }
        System.out.println(dp[W]);
    }
}
