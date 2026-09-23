import java.io.*;
import java.util.*;

public class Main {
    static List<Integer> primesUpto(int m) {
        boolean[] isP = new boolean[m + 1];
        Arrays.fill(isP, true);
        isP[0] = false; isP[1] = false;
        for (int i = 2; i * i <= m; i++) {
            if (isP[i]) {
                for (int j = i * i; j <= m; j += i) isP[j] = false;
            }
        }
        List<Integer> ps = new ArrayList<>();
        for (int i = 2; i <= m; i++) if (isP[i]) ps.add(i);
        return ps;
    }

    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String s;
        s = br.readLine();
        while (s != null && s.trim().isEmpty()) s = br.readLine();
        int n = Integer.parseInt(s.trim());
        StringTokenizer st = new StringTokenizer(br.readLine());
        int[] a = new int[n];
        for (int i = 0; i < n; i++) a[i] = Integer.parseInt(st.nextToken());

        List<Integer> ps = primesUpto(100);
        int ans = 0;
        for (int p : ps) {
            int pre2 = 0, pre1 = 0; // dp[i-2], dp[i-1]
            for (int x : a) {
                int b = (x % p == 0) ? 1 : 0;
                int cur = Math.max(pre1, pre2 + b);
                pre2 = pre1; pre1 = cur;
            }
            ans = Math.max(ans, pre1);
        }
        System.out.println(ans);
    }
}
