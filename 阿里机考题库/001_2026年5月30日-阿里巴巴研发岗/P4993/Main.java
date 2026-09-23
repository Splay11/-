import java.io.*;
import java.util.*;

public class Main {
    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int q = Integer.parseInt(br.readLine().trim());
        StringBuilder out = new StringBuilder();
        while (q-- > 0) {
            int m = Integer.parseInt(br.readLine().trim());
            long[] h = new long[m];
            StringTokenizer st = new StringTokenizer(br.readLine());
            for (int i = 0; i < m; i++) h[i] = Long.parseLong(st.nextToken());
            int[] L = new int[m], R = new int[m];
            long mx = -1;
            int pos = -1;
            // 左扫求每个位置左侧最近峰值下标
            for (int i = 0; i < m; i++) {
                L[i] = pos;
                if (h[i] > mx) { mx = h[i]; pos = i; }
                else if (h[i] == mx) pos = i;
            }
            mx = -1; pos = -1;
            // 右扫求每个位置右侧最近峰值下标
            for (int i = m - 1; i >= 0; i--) {
                R[i] = pos;
                if (h[i] > mx) { mx = h[i]; pos = i; }
                else if (h[i] == mx) pos = i;
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
