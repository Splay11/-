import java.util.*;

public class Main {
    public static void main(String[] args) {}
}

class Solution {
    public int minTrustDelay(int n, int[][] edges, int src, int dst, int riskBudget) {
        if (src == dst) return 0;
        List<int[]>[] g = new ArrayList[n];
        for (int i = 0; i < n; i++) g[i] = new ArrayList<>();
        for (int[] e : edges) g[e[0]].add(new int[] {e[1], e[2], e[3]});
        long inf = (1L << 62);
        long[][] dist = new long[n][riskBudget + 1];
        for (int i = 0; i < n; i++) Arrays.fill(dist[i], inf);
        dist[src][0] = 0;
        PriorityQueue<long[]> pq = new PriorityQueue<>(Comparator.comparingLong(a -> a[0]));
        pq.add(new long[] {0, src, 0});
        while (!pq.isEmpty()) {
            long[] cur = pq.poll();
            long delay = cur[0];
            int u = (int) cur[1], used = (int) cur[2];
            if (delay != dist[u][used]) continue;
            if (u == dst) return (int) delay;
            for (int[] e : g[u]) {
                int v = e[0], w = e[1], r = e[2];
                int nu = used + r;
                if (nu > riskBudget) continue;
                long nd = delay + w;
                if (nd < dist[v][nu]) {
                    dist[v][nu] = nd;
                    pq.add(new long[] {nd, v, nu});
                }
            }
        }
        return -1;
    }
}
