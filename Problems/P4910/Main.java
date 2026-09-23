import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.util.StringTokenizer;

public class Main {
    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int T = Integer.parseInt(br.readLine().trim());
        StringBuilder out = new StringBuilder();
        while (T-- > 0) {
            StringTokenizer st = new StringTokenizer(br.readLine());
            int n = Integer.parseInt(st.nextToken());
            long d = Long.parseLong(st.nextToken());
            long[] a = new long[n];
            st = new StringTokenizer(br.readLine());
            for (int i = 0; i < n; ++i) {
                a[i] = Long.parseLong(st.nextToken());
            }
            int ans = 1;
            int cur = 1;
            for (int i = 1; i < n; ++i) {
                long diff = a[i] - a[i - 1];
                if (diff < 0) {
                    diff = -diff;
                }
                if (diff <= d) {
                    ++cur;
                } else {
                    cur = 1;
                }
                if (cur > ans) {
                    ans = cur;
                }
            }
            out.append(ans).append('\n');
        }
        System.out.print(out.toString());
    }
}
