import java.io.*;
import java.math.BigInteger;
import java.util.*;

public class Main {
    static final int MOD = 1_000_000_007;

    static int cyclePeriod(String s) {
        int m = s.length();
        for (int d = 1; d <= m; d++) {
            if (m % d != 0) continue;
            boolean ok = true;
            for (int i = 0; i < m; i++) {
                if (s.charAt(i) != s.charAt(i % d)) {
                    ok = false;
                    break;
                }
            }
            if (ok) return d;
        }
        return m;
    }

    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int n = Integer.parseInt(br.readLine().trim());
        String u = br.readLine().trim();
        StringTokenizer st = new StringTokenizer(br.readLine());
        int[] p = new int[n];
        for (int i = 0; i < n; i++) {
            p[i] = Integer.parseInt(st.nextToken()) - 1;
        }

        boolean[] vis = new boolean[n];
        BigInteger ans = BigInteger.ONE;
        for (int i = 0; i < n; i++) {
            if (vis[i]) continue;
            StringBuilder cyc = new StringBuilder();
            int x = i;
            while (!vis[x]) {
                vis[x] = true;
                cyc.append(u.charAt(x));
                x = p[x];
            }
            int per = cyclePeriod(cyc.toString());
            BigInteger bp = BigInteger.valueOf(per);
            ans = ans.divide(ans.gcd(bp)).multiply(bp);
        }
        System.out.println(ans.mod(BigInteger.valueOf(MOD)));
    }
}
