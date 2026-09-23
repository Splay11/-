import java.io.*;
import java.util.*;

public class Main {
  static final long INF = (long) 4e18;

  static long[] dijkstra(int n, List<int[]>[] g, int src) {
    long[] dist = new long[n + 1];
    Arrays.fill(dist, INF);
    PriorityQueue<long[]> pq = new PriorityQueue<>(Comparator.comparingLong(x -> x[0]));
    dist[src] = 0;
    pq.add(new long[] {0, src});
    while (!pq.isEmpty()) {
      long[] cur = pq.poll();
      long d = cur[0];
      int u = (int) cur[1];
      if (d != dist[u]) continue;
      for (int[] e : g[u]) {
        int v = e[0], w = e[1];
        if (d + w < dist[v]) {
          dist[v] = d + w;
          pq.add(new long[] {dist[v], v});
        }
      }
    }
    return dist;
  }

  public static void main(String[] args) throws IOException {
    BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
    String[] nmks = br.readLine().trim().split("\\s+");
    int n = Integer.parseInt(nmks[0]);
    int m = Integer.parseInt(nmks[1]);
    int k = Integer.parseInt(nmks[2]);
    int s = Integer.parseInt(nmks[3]);
    @SuppressWarnings("unchecked")
    List<int[]>[] g = new ArrayList[n + 1];
    for (int i = 1; i <= n; i++) g[i] = new ArrayList<>();
    for (int i = 0; i < m; i++) {
      String[] sp = br.readLine().trim().split("\\s+");
      int u = Integer.parseInt(sp[0]), v = Integer.parseInt(sp[1]), w = Integer.parseInt(sp[2]);
      g[u].add(new int[] {v, w});
    }
    for (int i = 0; i < k; i++) {
      String[] sp = br.readLine().trim().split("\\s+");
      int u = Integer.parseInt(sp[0]), v = Integer.parseInt(sp[1]), w = Integer.parseInt(sp[2]);
      g[u].add(new int[] {v, w});
      g[v].add(new int[] {u, w});
    }
    String[] abq = br.readLine().trim().split("\\s+");
    int a = Integer.parseInt(abq[0]), b = Integer.parseInt(abq[1]), q = Integer.parseInt(abq[2]);
    String[] ds = br.readLine().trim().split("\\s+");
    int[] dest = new int[q];
    for (int i = 0; i < q; i++) dest[i] = Integer.parseInt(ds[i]);

    LinkedHashSet<Integer> uniq = new LinkedHashSet<>();
    uniq.add(s);
    for (int x : dest) uniq.add(x);
    Map<Integer, long[]> table = new HashMap<>();
    for (int u : uniq) table.put(u, dijkstra(n, g, u));

    long t = 0;
    int cur = s;
    for (int d : dest) {
      t += table.get(cur)[d];
      if (t % 2 == 1) t += a;
      else t += b;
      cur = d;
    }
    t += table.get(cur)[s];
    System.out.println(t);
  }
}
