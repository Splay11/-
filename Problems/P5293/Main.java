import java.io.*;
import java.util.*;

public class Main {
  static long solve(int n, int F, int[] p, int[][] edges) {
    // 建无向图
    ArrayList<int[]>[] g = new ArrayList[n + 1];
    for (int i = 1; i <= n; i++) g[i] = new ArrayList<int[]>();
    for (int[] e : edges) {
      int u = e[0], v = e[1], c = e[2], t = e[3];
      g[u].add(new int[] {v, c, t});
      g[v].add(new int[] {u, c, t});
    }
    long INF = Long.MAX_VALUE / 4;
    long[][] dist = new long[n + 1][F + 1];
    for (int i = 1; i <= n; i++) Arrays.fill(dist[i], INF);
    // 出发时满箱
    dist[1][F] = 0;
    PriorityQueue<long[]> pq = new PriorityQueue<long[]>(new Comparator<long[]>() {
      public int compare(long[] a, long[] b) {
        return Long.compare(a[0], b[0]);
      }
    });
    pq.add(new long[] {0, 1, F});
    while (!pq.isEmpty()) {
      long[] cur = pq.poll();
      long d = cur[0];
      int u = (int) cur[1], f = (int) cur[2];
      if (d != dist[u][f]) continue;
      if (u == n) return d;
      // 加 1 格电
      if (f < F) {
        long nd = d + p[u];
        if (nd < dist[u][f + 1]) {
          dist[u][f + 1] = nd;
          pq.add(new long[] {nd, u, f + 1});
        }
      }
      for (int[] e : g[u]) {
        int v = e[0], c = e[1], t = e[2];
        if (f >= c) {
          long nd = d + t;
          int nf = f - c;
          if (nd < dist[v][nf]) {
            dist[v][nf] = nd;
            pq.add(new long[] {nd, v, nf});
          }
        }
      }
    }
    return -1;
  }

  public static void main(String[] args) throws IOException {
    BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
    String[] sp = br.readLine().trim().split("\\s+");
    int n = Integer.parseInt(sp[0]);
    int m = Integer.parseInt(sp[1]);
    int F = Integer.parseInt(sp[2]);
    String[] ps = br.readLine().trim().split("\\s+");
    int[] p = new int[n + 1];
    for (int i = 1; i <= n; i++) p[i] = Integer.parseInt(ps[i - 1]);
    int[][] edges = new int[m][4];
    for (int i = 0; i < m; i++) {
      String[] e = br.readLine().trim().split("\\s+");
      for (int j = 0; j < 4; j++) edges[i][j] = Integer.parseInt(e[j]);
    }
    System.out.println(solve(n, F, p, edges));
  }
}
