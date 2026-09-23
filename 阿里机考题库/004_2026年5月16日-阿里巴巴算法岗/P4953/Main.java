import java.io.*;
import java.util.*;

public class Main {
    static final int MOD = 1_000_000_007;
    static final int MAXN = 200000 + 5;
    static long[] pw2 = new long[MAXN];

    public static void main(String[] args) throws Exception {
        pw2[0] = 1;
        for (int i = 1; i < MAXN; i++) pw2[i] = pw2[i - 1] * 2 % MOD;

        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int q = Integer.parseInt(br.readLine().trim());
        StringBuilder out = new StringBuilder();
        while (q-- > 0) {
            int m = Integer.parseInt(br.readLine().trim());
            String z = br.readLine().trim();
            boolean[] seen = new boolean[26];
            int kind = 0, diff = 0;
            for (int i = 0; i < m; i++) {
                int id = z.charAt(i) - 'a';
                if (!seen[id]) {
                    seen[id] = true;
                    kind++;
                }
            }
            for (int i = 0; i + 1 < m; i++) {
                if (z.charAt(i) != z.charAt(i + 1)) diff++;
            }
            // 可能失灵字母数 × 每种的插空方案数
            long ans = (26 - kind) * pw2[diff + 2] % MOD;
            out.append(ans).append('\n');
        }
        System.out.print(out);
    }
}
