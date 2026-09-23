import java.io.*;
import java.util.*;

public class Main {
    static int gcd(int a, int b) {
        while (b != 0) {
            int t = a % b;
            a = b;
            b = t;
        }
        return a;
    }

    static int solveOne(int[] a) {
        int g = 0, len = 0, ans = 0;
        for (int x : a) {
            g = (g == 0) ? x : gcd(g, x);
            len++;
            if (g <= len) {   // 能切就切
                ans++;
                g = 0;
                len = 0;
            }
        }
        return ans == 0 ? -1 : ans;
    }

    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StringBuilder sb = new StringBuilder();
        int T = Integer.parseInt(br.readLine().trim());
        while (T-- > 0) {
            int n = Integer.parseInt(br.readLine().trim());
            StringTokenizer st = new StringTokenizer(br.readLine());
            int[] a = new int[n];
            for (int i = 0; i < n; i++) a[i] = Integer.parseInt(st.nextToken());
            sb.append(solveOne(a)).append('\n');
        }
        System.out.print(sb.toString());
    }
}
