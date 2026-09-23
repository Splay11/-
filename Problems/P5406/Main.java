import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.PriorityQueue;
import java.util.StringTokenizer;

public class Main {
    static final long INF = 1L << 62;

    static long[] dijkstra(int n, int src, ArrayList<int[]>[] adj) {
        long[] dist = new long[n + 1];
        for (int i = 0; i <= n; i++) {
            dist[i] = INF;
        }
        dist[src] = 0;
        PriorityQueue<long[]> heap = new PriorityQueue<long[]>((a, b) -> Long.compare(a[0], b[0]));
        heap.add(new long[] {0, src});
        while (!heap.isEmpty()) {
            long[] cur = heap.poll();
            long d = cur[0];
            int u = (int) cur[1];
            if (d != dist[u]) {
                continue;
            }
            for (int i = 0; i < adj[u].size(); i++) {
                int v = adj[u].get(i)[0];
                int w = adj[u].get(i)[1];
                long nd = d + w;
                if (nd < dist[v]) {
                    dist[v] = nd;
                    heap.add(new long[] {nd, v});
                }
            }
        }
        return dist;
    }

    static long minWithOneFree(int n, int s, int t, int[][] edges, ArrayList<int[]>[] adj) {
        // 入口即出口，不必移动
        if (s == t) {
            return 0;
        }
        long[] ds = dijkstra(n, s, adj);
        long[] dt = dijkstra(n, t, adj);
        long ans = ds[t];
        for (int i = 0; i < edges.length; i++) {
            int u = edges[i][0];
            int v = edges[i][1];
            // 免费走 u -> v
            if (ds[u] < INF / 2 && dt[v] < INF / 2) {
                long nd = ds[u] + dt[v];
                if (nd < ans) {
                    ans = nd;
                }
            }
            // 通道是双向的，另一方向同样可以免费
            if (ds[v] < INF / 2 && dt[u] < INF / 2) {
                long nd = ds[v] + dt[u];
                if (nd < ans) {
                    ans = nd;
                }
            }
        }
        return ans >= INF / 2 ? -1 : ans;
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StringTokenizer st = new StringTokenizer(br.readLine());
        int n = Integer.parseInt(st.nextToken());
        int m = Integer.parseInt(st.nextToken());
        int s = Integer.parseInt(st.nextToken());
        int t = Integer.parseInt(st.nextToken());
        int[][] edges = new int[m][3];
        ArrayList<int[]>[] adj = new ArrayList[n + 1];
        for (int i = 0; i <= n; i++) {
            adj[i] = new ArrayList<int[]>();
        }
        for (int i = 0; i < m; i++) {
            st = new StringTokenizer(br.readLine());
            int u = Integer.parseInt(st.nextToken());
            int v = Integer.parseInt(st.nextToken());
            int w = Integer.parseInt(st.nextToken());
            edges[i][0] = u;
            edges[i][1] = v;
            edges[i][2] = w;
            adj[u].add(new int[] {v, w});
            adj[v].add(new int[] {u, w});
        }
        System.out.println(minWithOneFree(n, s, t, edges, adj));
    }
}
