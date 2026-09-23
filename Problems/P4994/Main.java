import java.io.*;
import java.util.*;

public class Main {
    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StringTokenizer st = new StringTokenizer(br.readLine());
        int q = Integer.parseInt(st.nextToken());
        StringBuilder out = new StringBuilder();
        while (q-- > 0) {
            st = new StringTokenizer(br.readLine());
            int h = Integer.parseInt(st.nextToken());
            int w = Integer.parseInt(st.nextToken());
            long[][] G = new long[h][w];
            long[] rs = new long[h];
            long[] cs = new long[w];
            for (int i = 0; i < h; i++) {
                st = new StringTokenizer(br.readLine());
                for (int j = 0; j < w; j++) {
                    G[i][j] = Long.parseLong(st.nextToken());
                    rs[i] += G[i][j];
                    cs[j] += G[i][j];
                }
            }
            long ans = Long.MIN_VALUE;
            for (long v : rs) ans = Math.max(ans, v);
            for (long v : cs) ans = Math.max(ans, v);
            if (h >= 2) {
                long a = Long.MIN_VALUE, b = Long.MIN_VALUE;
                for (long v : rs) {
                    if (v >= a) {
                        b = a;
                        a = v;
                    } else if (v > b) {
                        b = v;
                    }
                }
                ans = Math.max(ans, a + b);
            }
            if (w >= 2) {
                long a = Long.MIN_VALUE, b = Long.MIN_VALUE;
                for (long v : cs) {
                    if (v >= a) {
                        b = a;
                        a = v;
                    } else if (v > b) {
                        b = v;
                    }
                }
                ans = Math.max(ans, a + b);
            }
            for (int i = 0; i < h; i++) {
                for (int j = 0; j < w; j++) {
                    ans = Math.max(ans, rs[i] + cs[j] - G[i][j]);
                }
            }
            out.append(ans).append('\n');
        }
        System.out.print(out);
    }
}
