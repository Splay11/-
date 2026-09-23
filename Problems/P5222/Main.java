import java.util.*;
import java.io.*;

public class Main {
    static List<Integer> solve(int n, int k, int S, int R) {
        for (int M = 1; M <= 6; M++) {
            // 检查保留部分范围
            if (R < n - k || R > (long)(n - k) * M) continue;
            // 检查召回部分范围
            long diff = (long)S - R;
            if (diff < (long)k * M || diff > (long)k * 6) continue;

            // 构造保留部分
            List<Integer> ans = new ArrayList<>();
            long extra = (long)R - (n - k);
            for (int i = 0; i < n - k; i++) {
                int add = (int)Math.min(extra, M - 1);
                ans.add(1 + add);
                extra -= add;
            }

            // 构造召回部分
            extra = diff - (long)k * M;
            for (int i = 0; i < k; i++) {
                int add = (int)Math.min(extra, 6 - M);
                ans.add(M + add);
                extra -= add;
            }
            return ans;
        }
        return null;
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StringTokenizer st = new StringTokenizer(br.readLine());
        int n = Integer.parseInt(st.nextToken());
        int k = Integer.parseInt(st.nextToken());
        int S = Integer.parseInt(st.nextToken());
        int R = Integer.parseInt(st.nextToken());

        List<Integer> ans = solve(n, k, S, R);
        if (ans == null) {
            System.out.println(-1);
        } else {
            StringBuilder out = new StringBuilder();
            for (int i = 0; i < ans.size(); i++) {
                if (i > 0) out.append(' ');
                out.append(ans.get(i));
            }
            System.out.println(out);
        }
    }
}
