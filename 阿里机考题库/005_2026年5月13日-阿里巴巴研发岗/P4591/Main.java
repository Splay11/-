import java.io.*;
import java.util.*;

/**
 * 相邻不同串计数 — 逐位 DP
 * f[c]: 当前前缀以字符 c 结尾的方案数，转移时从前一位 total 减去相同的字符数
 */
public class Main {
    static final int MOD = 1000000007;

    static int solveOne(int m, String pat) {
        long[] f = new long[26];
        // 第一位初始化
        if (pat.charAt(0) == '?') {
            Arrays.fill(f, 1);
        } else {
            f[pat.charAt(0) - 'a'] = 1;
        }

        long total = 0;
        for (long v : f) total = (total + v) % MOD;

        for (int i = 1; i < m; i++) {
            char ch = pat.charAt(i);
            long[] nf = new long[26];  // 下一位 dp
            if (ch == '?') {
                for (int c = 0; c < 26; c++)
                    nf[c] = (total - f[c] + MOD) % MOD;
            } else {
                int c = ch - 'a';
                nf[c] = (total - f[c] + MOD) % MOD;
            }

            f = nf;
            total = 0;
            for (long v : f) total = (total + v) % MOD;
            if (total == 0) break;
        }

        return (int) total;
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        PrintWriter out = new PrintWriter(new BufferedOutputStream(System.out));

        int T = Integer.parseInt(br.readLine());
        while (T-- > 0) {
            int m = Integer.parseInt(br.readLine());
            String pat = br.readLine();
            out.println(solveOne(m, pat));
        }
        out.flush();
    }
}
