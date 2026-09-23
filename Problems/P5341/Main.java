import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;
import java.util.PriorityQueue;
import java.util.Scanner;

public class Main {
    static int maxBottleneck(int c, int t, int[][] edges) {
        List<List<int[]>> graph = new ArrayList<List<int[]>>();
        for (int i = 0; i < c; i++) {
            graph.add(new ArrayList<int[]>());
        }
        for (int[] e : edges) {
            graph.get(e[0]).add(new int[] {e[1], e[2]});
            graph.get(e[1]).add(new int[] {e[0], e[2]});
        }
        final int INF = 1000000000;
        // f[u][used]：到达 u、恰好升级 used 次时，能得到的最大瓶颈
        int[][] f = new int[c][t + 1];
        for (int i = 0; i < c; i++) {
            for (int j = 0; j <= t; j++) {
                f[i][j] = -1;
            }
        }
        f[0][0] = INF;
        PriorityQueue<int[]> pq = new PriorityQueue<int[]>(new Comparator<int[]>() {
            public int compare(int[] a, int[] b) {
                return b[0] - a[0];
            }
        });
        pq.add(new int[] {INF, 0, 0});
        while (!pq.isEmpty()) {
            int[] cur = pq.poll();
            int bneck = cur[0];
            int u = cur[1];
            int used = cur[2];
            if (bneck < f[u][used]) {
                continue;
            }
            for (int[] e : graph.get(u)) {
                int v = e[0];
                int w = e[1];
                // 不升级这条边
                int nxt0 = (bneck == INF) ? w : Math.min(bneck, w);
                if (nxt0 > f[v][used]) {
                    f[v][used] = nxt0;
                    pq.add(new int[] {nxt0, v, used});
                }
                // 升级这条边，带宽变为 2w
                if (used < t) {
                    int ww = 2 * w;
                    int nxt1 = (bneck == INF) ? ww : Math.min(bneck, ww);
                    if (nxt1 > f[v][used + 1]) {
                        f[v][used + 1] = nxt1;
                        pq.add(new int[] {nxt1, v, used + 1});
                    }
                }
            }
        }
        int ans = f[c - 1][0];
        if (t > 0) {
            ans = Math.max(ans, f[c - 1][t]);
        }
        if (ans < 0) {
            return -1;
        }
        return ans;
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int c = sc.nextInt();
        int d = sc.nextInt();
        int t = sc.nextInt();
        int[][] edges = new int[d][3];
        for (int i = 0; i < d; i++) {
            edges[i][0] = sc.nextInt();
            edges[i][1] = sc.nextInt();
            edges[i][2] = sc.nextInt();
        }
        System.out.println(maxBottleneck(c, t, edges));
        sc.close();
    }
}
