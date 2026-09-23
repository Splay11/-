import java.io.*;
import java.util.*;

public class Main {
    static long solve(int[] a) {
        int n = a.length;
        long ans = 0;
        for (int l = 0; l < n; l++) {
            long s = 0;
            int lim = Math.min(n, l + 100);
            for (int r = l; r < lim; r++) {
                s += a[r];
                int L = r - l + 1;
                if (s == 1L * L * L) ans++;
            }
        }
        return ans;
    }

    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StringTokenizer st = new StringTokenizer(br.readLine());
        int T = Integer.parseInt(st.nextToken());
        StringBuilder sb = new StringBuilder();
        while (T-- > 0) {
            st = new StringTokenizer(br.readLine());
            int n = Integer.parseInt(st.nextToken());
            int[] a = new int[n];
            st = new StringTokenizer(br.readLine());
            for (int i = 0; i < n; i++) a[i] = Integer.parseInt(st.nextToken());
            sb.append(solve(a)).append('\n');
        }
        System.out.print(sb);
    }
}
