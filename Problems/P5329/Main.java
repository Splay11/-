import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.PriorityQueue;
import java.util.StringTokenizer;

public class Main {
  static class E {
    int v, c, t;
    E(int v, int c, int t) {
      this.v = v;
      this.c = c;
      this.t = t;
    }
  }

  static class St implements Comparable<St> {
    long tm;
    int u, f;
    St(long tm, int u, int f) {
      this.tm = tm;
      this.u = u;
      this.f = f;
    }
    public int compareTo(St o) {
      if (tm < o.tm) return -1;
      if (tm > o.tm) return 1;
      return 0;
    }
  }

  static long solve(int k, int q, int[] r, ArrayList<E>[] g) {
    // 状态 (城市, 剩余油量)
    long inf = 1000000000000000000L;
    long[][] dist = new long[k + 1][q + 1];
    for (int i = 1; i <= k; i++) {
      for (int f = 0; f <= q; f++) dist[i][f] = inf;
    }
    dist[1][q] = 0;
    PriorityQueue<St> pq = new PriorityQueue<St>();
    pq.add(new St(0, 1, q));
    while (!pq.isEmpty()) {
      St cur = pq.poll();
      if (cur.tm != dist[cur.u][cur.f]) continue;
      if (cur.f < q) {
        long ntm = cur.tm + r[cur.u - 1];
        int nf = cur.f + 1;
        if (ntm < dist[cur.u][nf]) {
          dist[cur.u][nf] = ntm;
          pq.add(new St(ntm, cur.u, nf));
        }
      }
      for (E e : g[cur.u]) {
        if (cur.f >= e.c) {
          long ntm = cur.tm + e.t;
          int nf = cur.f - e.c;
          if (ntm < dist[e.v][nf]) {
            dist[e.v][nf] = ntm;
            pq.add(new St(ntm, e.v, nf));
          }
        }
      }
    }
    long ans = inf;
    for (int f = 0; f <= q; f++) if (dist[k][f] < ans) ans = dist[k][f];
    if (ans >= inf) return -1;
    return ans;
  }

  public static void main(String[] args) throws IOException {
    BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
    StringTokenizer st = new StringTokenizer(br.readLine());
    int k = Integer.parseInt(st.nextToken());
    int e = Integer.parseInt(st.nextToken());
    int q = Integer.parseInt(st.nextToken());
    st = new StringTokenizer(br.readLine());
    int[] r = new int[k];
    for (int i = 0; i < k; i++) r[i] = Integer.parseInt(st.nextToken());
    ArrayList<E>[] g = new ArrayList[k + 1];
    for (int i = 1; i <= k; i++) g[i] = new ArrayList<E>();
    for (int i = 0; i < e; i++) {
      st = new StringTokenizer(br.readLine());
      int a = Integer.parseInt(st.nextToken());
      int b = Integer.parseInt(st.nextToken());
      int c = Integer.parseInt(st.nextToken());
      int t = Integer.parseInt(st.nextToken());
      g[a].add(new E(b, c, t));
      g[b].add(new E(a, c, t));
    }
    System.out.println(solve(k, q, r, g));
  }
}
