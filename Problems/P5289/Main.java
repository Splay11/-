import java.io.*;
import java.util.*;

public class Main {
  static long solve(int n, int[] us, int[] vs, long[] ws) {
    // 只有一个点时无处可走
    if (n == 1) return 0;
    // 建无向树，同时累加全部边权
    ArrayList<long[]>[] g = new ArrayList[n + 1];
    for (int i = 1; i <= n; i++) g[i] = new ArrayList<long[]>();
    long total = 0;
    for (int i = 0; i < n - 1; i++) {
      int u = us[i], v = vs[i];
      long w = ws[i];
      g[u].add(new long[] {v, w});
      g[v].add(new long[] {u, w});
      total += w;
    }
    // 从 1 号队部做一遍遍历，算出到每个哨所的距离
    long[] dist = new long[n + 1];
    Arrays.fill(dist, -1);
    dist[1] = 0;
    ArrayDeque<Integer> st = new ArrayDeque<Integer>();
    st.addLast(1);
    while (!st.isEmpty()) {
      int u = st.pollLast();
      for (long[] e : g[u]) {
        int v = (int) e[0];
        long w = e[1];
        if (dist[v] < 0) {
          dist[v] = dist[u] + w;
          st.addLast(v);
        }
      }
    }
    // 除通往最远哨所的链外，每条边都要走一个来回
    long farthest = 0;
    for (int i = 1; i <= n; i++) farthest = Math.max(farthest, dist[i]);
    return 2 * total - farthest;
  }

  public static void main(String[] args) throws IOException {
    BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
    // 第一行点数，随后 n-1 条边
    int n = Integer.parseInt(br.readLine().trim());
    int[] us = new int[Math.max(0, n - 1)];
    int[] vs = new int[Math.max(0, n - 1)];
    long[] ws = new long[Math.max(0, n - 1)];
    for (int i = 0; i < n - 1; i++) {
      String[] sp = br.readLine().trim().split("\\s+");
      us[i] = Integer.parseInt(sp[0]);
      vs[i] = Integer.parseInt(sp[1]);
      ws[i] = Long.parseLong(sp[2]);
    }
    System.out.println(solve(n, us, vs, ws));
  }
}
