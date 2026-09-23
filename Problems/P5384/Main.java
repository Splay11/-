import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Comparator;
import java.util.List;
import java.util.PriorityQueue;
import java.util.StringTokenizer;

public class Main {
    static final long INF = 1L << 62;

    static class Edge {
        int to;
        long w;
        Edge(int to, long w) {
            this.to = to;
            this.w = w;
        }
    }

    // 状态最短路：工位 u、已用罐笼 used、上一步是否罐笼 last
    static long minTime(int n, List<int[]> roads, List<int[]> portals, int cap, int src, int dst) {
        if (src == dst) {
            return 0;
        }
        List<List<Edge>> g = new ArrayList<>();
        List<List<Integer>> pg = new ArrayList<>();
        for (int i = 0; i < n; i++) {
            g.add(new ArrayList<>());
            pg.add(new ArrayList<>());
        }
        for (int[] e : roads) {
            g.get(e[0]).add(new Edge(e[1], e[2]));
            g.get(e[1]).add(new Edge(e[0], e[2]));
        }
        for (int[] e : portals) {
            pg.get(e[0]).add(e[1]);
            pg.get(e[1]).add(e[0]);
        }
        long[][][] dist = new long[n][cap + 1][2];
        for (int i = 0; i < n; i++) {
            for (int u = 0; u <= cap; u++) {
                Arrays.fill(dist[i][u], INF);
            }
        }
        dist[src][0][0] = 0;
        PriorityQueue<long[]> pq = new PriorityQueue<>(Comparator.comparingLong(a -> a[0]));
        pq.add(new long[] {0, src, 0, 0});
        while (!pq.isEmpty()) {
            long[] cur = pq.poll();
            long d = cur[0];
            int u = (int) cur[1];
            int used = (int) cur[2];
            int last = (int) cur[3];
            if (d != dist[u][used][last]) {
                continue;
            }
            if (u == dst) {
                return d;
            }
            // 普通巷道：次数不变，last 置 0
            for (Edge e : g.get(u)) {
                long nd = d + e.w;
                if (nd < dist[e.to][used][0]) {
                    dist[e.to][used][0] = nd;
                    pq.add(new long[] {nd, e.to, used, 0});
                }
            }
            // 罐笼：不能连坐，且次数未用尽；出发时可直接坐
            if (last == 0 && used < cap) {
                for (int v : pg.get(u)) {
                    if (d < dist[v][used + 1][1]) {
                        dist[v][used + 1][1] = d;
                        pq.add(new long[] {d, v, used + 1, 1});
                    }
                }
            }
        }
        return -1;
    }

    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StringTokenizer st = new StringTokenizer(br.readLine());
        int n = Integer.parseInt(st.nextToken());
        int m = Integer.parseInt(st.nextToken());
        List<int[]> roads = new ArrayList<>();
        for (int i = 0; i < m; i++) {
            st = new StringTokenizer(br.readLine());
            int u = Integer.parseInt(st.nextToken());
            int v = Integer.parseInt(st.nextToken());
            int d = Integer.parseInt(st.nextToken());
            roads.add(new int[] {u, v, d});
        }
        int p = Integer.parseInt(br.readLine().trim());
        List<int[]> portals = new ArrayList<>();
        for (int i = 0; i < p; i++) {
            st = new StringTokenizer(br.readLine());
            int u = Integer.parseInt(st.nextToken());
            int v = Integer.parseInt(st.nextToken());
            portals.add(new int[] {u, v});
        }
        st = new StringTokenizer(br.readLine());
        int cap = Integer.parseInt(st.nextToken());
        int src = Integer.parseInt(st.nextToken());
        int dst = Integer.parseInt(st.nextToken());
        System.out.println(minTime(n, roads, portals, cap, src, dst));
    }
}
