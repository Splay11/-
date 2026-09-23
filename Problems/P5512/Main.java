import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.List;
import java.util.StringTokenizer;

public class Main {
    static long[][] dp;
    static int[][] rt;

    // 按记录的根展开前序遍历
    static void preorder(int i, int j, List<Integer> seq) {
        if (i > j) return;
        int r = rt[i][j];
        seq.add(r);
        preorder(i, r - 1, seq);
        preorder(r + 1, j, seq);
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int n = Integer.parseInt(br.readLine().trim());
        StringTokenizer st = new StringTokenizer(br.readLine());
        long[] d = new long[n + 1];
        for (int i = 1; i <= n; i++) d[i] = Long.parseLong(st.nextToken());

        dp = new long[n + 2][n + 2];
        rt = new int[n + 2][n + 2];
        for (int i = 1; i <= n; i++) {
            dp[i][i] = d[i];
            rt[i][i] = i;
            dp[i][i - 1] = 1;
        }
        dp[n + 1][n] = 1;

        for (int len = 2; len <= n; len++) {
            for (int i = 1; i + len - 1 <= n; i++) {
                int j = i + len - 1;
                long best = -1;
                int bestR = i;
                for (int k = i; k <= j; k++) {
                    long left = (k > i) ? dp[i][k - 1] : 1;
                    long right = (k < j) ? dp[k + 1][j] : 1;
                    long score = left * right + d[k];
                    if (score > best) {
                        best = score;
                        bestR = k;
                    }
                }
                dp[i][j] = best;
                rt[i][j] = bestR;
            }
        }

        System.out.println(dp[1][n]);
        List<Integer> seq = new ArrayList<>();
        preorder(1, n, seq);
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < seq.size(); i++) {
            if (i > 0) sb.append(' ');
            sb.append(seq.get(i));
        }
        System.out.println(sb.toString());
    }
}
