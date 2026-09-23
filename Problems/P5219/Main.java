import java.io.*;
import java.util.*;

public class Main {
    // 从右向左贪心：维护右侧块的代表值 suf，当前项过大则必须合并。
    static long minMerges(long[] v) {
        long suf = Long.MAX_VALUE / 4;
        long ans = 0;
        for (int i = v.length - 1; i >= 0; i--) {
            if (v[i] <= suf) {
                suf = v[i];
            } else {
                ans++;
                suf += v[i];
            }
        }
        return ans;
    }

    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int q = Integer.parseInt(br.readLine().trim());
        StringBuilder out = new StringBuilder();
        while (q-- > 0) {
            int n = Integer.parseInt(br.readLine().trim());
            StringTokenizer st = new StringTokenizer(br.readLine());
            long[] v = new long[n];
            for (int i = 0; i < n; i++) {
                v[i] = Long.parseLong(st.nextToken());
            }
            out.append(minMerges(v)).append('\n');
        }
        System.out.print(out);
    }
}
