import java.io.*;
import java.util.*;

public class Main {
    static long solve(int[] a) {
        int n = a.length;
        if (n == 1) return 0;
        Arrays.sort(a);
        // 升序后从大到小扫
        if (a[n - 1] <= 0) return 1L * a[n - 1] * (n - 1);
        long ans = 0;
        for (int i = 0; i < n; i++) {
            int x = a[n - 1 - i]; // 第 i 大
            if (x <= 0) break;
            ans += 1L * x * (n - 1 - i);
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
