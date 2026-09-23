import java.util.ArrayList;
import java.util.Arrays;
import java.util.Comparator;
import java.util.List;
import java.util.PriorityQueue;
import java.util.Scanner;

public class Main {
    static final long INF = 4_000_000_000_000_000_000L;

    static class Edge {
        int v, w;
        Edge(int v, int w) {
            this.v = v;
            this.w = w;
        }
    }

    // 从 src 出发的最短公里数
    static long[] dijkstra(int p, List<List<Edge>> adj, int src) {
        long[] dist = new long[p + 1];
        Arrays.fill(dist, INF);
        dist[src] = 0;
        PriorityQueue<long[]> pq = new PriorityQueue<>(Comparator.comparingLong(x -> x[0]));
        pq.add(new long[] {0, src});
        while (!pq.isEmpty()) {
            long[] cur = pq.poll();
            long d = cur[0];
            int u = (int) cur[1];
            if (d != dist[u]) {
                continue;
            }
            for (Edge e : adj.get(u)) {
                long nd = d + e.w;
                if (nd < dist[e.v]) {
                    dist[e.v] = nd;
                    pq.add(new long[] {nd, e.v});
                }
            }
        }
        return dist;
    }

    static long minMeetTime(int p, int[][] edges, int a, int b, int[] friends) {
        List<List<Edge>> adj = new ArrayList<>();
        for (int i = 0; i <= p; i++) {
            adj.add(new ArrayList<>());
        }
        for (int[] eg : edges) {
            int x = eg[0], y = eg[1], c = eg[2], z = eg[3];
            adj.get(x).add(new Edge(y, c));
            if (z == 1) {
                adj.get(y).add(new Edge(x, c));
            }
        }
        int q = friends.length;
        long[][] sp = new long[p + 1][];
        boolean[] seen = new boolean[p + 1];
        int[] sources = new int[q + 2];
        sources[0] = a;
        sources[1] = b;
        for (int i = 0; i < q; i++) {
            sources[i + 2] = friends[i];
        }
        for (int s : sources) {
            if (seen[s]) {
                continue;
            }
            seen[s] = true;
            sp[s] = dijkstra(p, adj, s);
        }
        if (q == 0) {
            return 2 * sp[a][b];
        }
        long[] walk = new long[q];
        for (int i = 0; i < q; i++) {
            walk[i] = 10 * sp[friends[i]][b];
        }
        // dp[mask][i]：已接 mask 里的同伴，当前停在同伴 i 处的最短驾车公里
        int N = 1 << q;
        long[][] dp = new long[N][q];
        for (int mask = 0; mask < N; mask++) {
            Arrays.fill(dp[mask], INF);
        }
        for (int i = 0; i < q; i++) {
            dp[1 << i][i] = sp[a][friends[i]];
        }
        for (int mask = 0; mask < N; mask++) {
            for (int i = 0; i < q; i++) {
                if (dp[mask][i] >= INF) {
                    continue;
                }
                if (((mask >> i) & 1) == 0) {
                    continue;
                }
                for (int j = 0; j < q; j++) {
                    if (((mask >> j) & 1) != 0) {
                        continue;
                    }
                    int nmask = mask | (1 << j);
                    long nd = dp[mask][i] + sp[friends[i]][friends[j]];
                    if (nd < dp[nmask][j]) {
                        dp[nmask][j] = nd;
                    }
                }
            }
        }
        long ans = INF;
        for (int mask = 0; mask < N; mask++) {
            long car;
            if (mask == 0) {
                car = 2 * sp[a][b];
            } else {
                car = INF;
                for (int i = 0; i < q; i++) {
                    if (((mask >> i) & 1) != 0) {
                        long cand = 2 * (dp[mask][i] + sp[friends[i]][b]);
                        if (cand < car) {
                            car = cand;
                        }
                    }
                }
            }
            long walkers = 0;
            for (int i = 0; i < q; i++) {
                if (((mask >> i) & 1) == 0 && walk[i] > walkers) {
                    walkers = walk[i];
                }
            }
            long cur = Math.max(car, walkers);
            if (cur < ans) {
                ans = cur;
            }
        }
        return ans;
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int p = sc.nextInt();
        int e = sc.nextInt();
        int a = sc.nextInt();
        int b = sc.nextInt();
        int[][] edges = new int[e][4];
        for (int i = 0; i < e; i++) {
            for (int j = 0; j < 4; j++) {
                edges[i][j] = sc.nextInt();
            }
        }
        int q = sc.nextInt();
        int[] friends = new int[q];
        for (int i = 0; i < q; i++) {
            friends[i] = sc.nextInt();
        }
        sc.close();
        System.out.println(minMeetTime(p, edges, a, b, friends));
    }
}
