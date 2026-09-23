import java.io.*;
import java.util.*;

public class Main {
    static final long MOD = 1000000007L;
    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int q = Integer.parseInt(br.readLine().trim());
        StringBuilder out = new StringBuilder();
        while (q-- > 0) {
            int m = Integer.parseInt(br.readLine().trim());
            long[] h = new long[m];
            StringTokenizer stok = new StringTokenizer(br.readLine());
            for (int i = 0; i < m; i++) h[i] = Long.parseLong(stok.nextToken());
            ArrayDeque<long[]> st = new ArrayDeque<>(); // {v, c}
            long cur = 0, ans = 0;
            for (int k = 1; k <= m; k++) {
                long x = h[k - 1];
                long cnt = 1;
                while (!st.isEmpty() && st.peekLast()[0] >= x) {
                    long[] top = st.pollLast();
                    cur -= top[0] * top[1];
                    cnt += top[1];
                }
                st.addLast(new long[]{x, cnt});
                cur += x * cnt;
                cur %= MOD;
                if (cur < 0) cur += MOD;
                ans = (ans + cur * (m - k + 1)) % MOD;
            }
            out.append(ans).append('\n');
        }
        System.out.print(out);
    }
}
