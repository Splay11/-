import java.io.*;
import java.util.*;

public class Main {
    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int q = Integer.parseInt(br.readLine().trim());
        StringBuilder out = new StringBuilder();
        while (q-- > 0) {
            StringTokenizer st = new StringTokenizer(br.readLine());
            int m = Integer.parseInt(st.nextToken());
            long s = Long.parseLong(st.nextToken());
            Integer[] h = new Integer[m];
            st = new StringTokenizer(br.readLine());
            for (int i = 0; i < m; i++) h[i] = Integer.parseInt(st.nextToken());
            // 硬度从大到小：优先尝试更硬的工件
            Arrays.sort(h, Collections.reverseOrder());
            int cnt = 0;
            for (int x : h) {
                // 已成功 cnt 次，当前耐久为 s - cnt
                if (s - cnt >= x) cnt++;
            }
            out.append(cnt).append('\n');
        }
        System.out.print(out);
    }
}
