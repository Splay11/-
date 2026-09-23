import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.StringTokenizer;

public class Main {
    static long kadane(long[] a) {
        long best = a[0], cur = a[0];
        for (int i = 1; i < a.length; i++) {
            cur = Math.max(a[i], cur + a[i]);
            best = Math.max(best, cur);
        }
        return best;
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StringTokenizer st = new StringTokenizer(br.readLine());
        int n = Integer.parseInt(st.nextToken());
        int k = Integer.parseInt(st.nextToken());
        st = new StringTokenizer(br.readLine());
        long[] a = new long[n];
        for (int i = 0; i < n; i++) {
            a[i] = Long.parseLong(st.nextToken());
        }
        long one = kadane(a);
        if (k == 1) {
            System.out.println(one);
            return;
        }
        long total = 0;
        for (long x : a) total += x;
        // 最大前缀和
        long s = 0, maxPref = a[0];
        for (long x : a) {
            s += x;
            if (s > maxPref) maxPref = s;
        }
        // 最大后缀和
        s = 0;
        long maxSuf = a[n - 1];
        for (int i = n - 1; i >= 0; i--) {
            s += a[i];
            if (s > maxSuf) maxSuf = s;
        }
        long ans = Math.max(one, maxSuf + maxPref);
        if (k > 2 && total > 0) {
            ans = Math.max(ans, maxSuf + (k - 2) * total + maxPref);
        }
        System.out.println(ans);
    }
}
