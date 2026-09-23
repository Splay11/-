import java.io.*;
import java.util.*;

public class Main {
    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int q = Integer.parseInt(br.readLine().trim());
        StringBuilder out = new StringBuilder();
        while (q-- > 0) {
            int m = Integer.parseInt(br.readLine().trim());
            int[] g = new int[m + 1];
            StringTokenizer st = new StringTokenizer(br.readLine());
            for (int i = 1; i <= m; i++) g[i] = Integer.parseInt(st.nextToken());
            long[] dis = new long[m + 1];
            Arrays.fill(dis, (long) 1e18);
            dis[1] = 0;
            ArrayDeque<Integer> dq = new ArrayDeque<>();
            dq.add(1);
            while (!dq.isEmpty()) {
                int x = dq.pollFirst();
                int y = g[x];
                if (dis[y] > dis[x]) { // 传送
                    dis[y] = dis[x];
                    dq.addFirst(y);
                }
                if (x < m && dis[x + 1] > dis[x] + 1) { // 右移
                    dis[x + 1] = dis[x] + 1;
                    dq.addLast(x + 1);
                }
            }
            out.append(dis[m]).append('\n');
        }
        System.out.print(out);
    }
}
