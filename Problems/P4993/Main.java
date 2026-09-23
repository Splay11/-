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
            int m = Integer.parseInt(st.nextToken());
            long[] h = new long[m];
            st = new StringTokenizer(br.readLine());
            for (int i = 0; i < m; i++) h[i] = Long.parseLong(st.nextToken());
            int[] L = new int[m];
            int[] R = new int[m];
            long mx = -1;
            int pos = -1;
            for (int i = 0; i < m; i++) {
                L[i] = pos;
                if (h[i] > mx) {
                    mx = h[i];
                    pos = i;
                } else if (h[i] == mx) {
                    pos = i;
                }
            }
            mx = -1;
            pos = -1;
            for (int i = m - 1; i >= 0; i--) {
                R[i] = pos;
                if (h[i] > mx) {
                    mx = h[i];
                    pos = i;
                } else if (h[i] == mx) {
                    pos = i;
                }
            }
            int ans = 0;
            for (int p = 1; p + 1 < m; p++) {
                if (p - L[p] == R[p] - p) ans++;
            }
            out.append(ans).append('\n');
        }
        System.out.print(out);
    }
}
