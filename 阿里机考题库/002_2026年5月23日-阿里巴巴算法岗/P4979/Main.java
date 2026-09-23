import java.io.*;
import java.util.*;

public class Main {
    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int q = Integer.parseInt(br.readLine().trim());
        StringBuilder out = new StringBuilder();
        while (q-- > 0) {
            int m = Integer.parseInt(br.readLine().trim());
            long[] x = new long[m], y = new long[m];
            int[] p = new int[m];
            StringTokenizer st = new StringTokenizer(br.readLine());
            for (int i = 0; i < m; i++) x[i] = Long.parseLong(st.nextToken());
            st = new StringTokenizer(br.readLine());
            for (int i = 0; i < m; i++) y[i] = Long.parseLong(st.nextToken());
            st = new StringTokenizer(br.readLine());
            for (int i = 0; i < m; i++) p[i] = Integer.parseInt(st.nextToken());
            HashMap<Long, Integer> freq = new HashMap<>();
            long ans = 0;
            for (int v = 0; v < m; v++) {
                freq.put(x[v], freq.getOrDefault(x[v], 0) + 1);
                ans += freq.getOrDefault(y[p[v] - 1], 0);
            }
            out.append(ans).append('\n');
        }
        System.out.print(out);
    }
}
