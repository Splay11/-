import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Collections;
import java.util.StringTokenizer;

public class Main {
  static ArrayList<int[]> solve(int n, int[][] edges) {
    // 无向无权图：邻接表存双向边
    ArrayList<Integer>[] g = new ArrayList[n + 1];
    for (int i = 1; i <= n; i++) g[i] = new ArrayList<Integer>();
    for (int[] e : edges) {
      g[e[0]].add(e[1]);
      g[e[1]].add(e[0]);
    }
    // dist[i] = -1 表示还没走到；门厅 1 号距离为 0
    int[] dist = new int[n + 1];
    for (int i = 1; i <= n; i++) dist[i] = -1;
    dist[1] = 0;
    ArrayDeque<Integer> q = new ArrayDeque<Integer>();
    q.add(1);
    while (!q.isEmpty()) {
      int u = q.poll();
      for (int v : g[u]) {
        if (dist[v] < 0) {
          dist[v] = dist[u] + 1;
          q.add(v);
        }
      }
    }
    // 只收集可达点，按（距离，编号）排序
    ArrayList<int[]> arr = new ArrayList<int[]>();
    for (int i = 1; i <= n; i++) {
      if (dist[i] >= 0) arr.add(new int[] {dist[i], i});
    }
    Collections.sort(arr, (a, b) -> {
      if (a[0] != b[0]) return a[0] - b[0];
      return a[1] - b[1];
    });
    return arr;
  }

  public static void main(String[] args) throws IOException {
    // 边数可达 1e5，用 BufferedReader
    BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
    StringTokenizer st = new StringTokenizer(br.readLine());
    int n = Integer.parseInt(st.nextToken());
    int m = Integer.parseInt(st.nextToken());
    int[][] edges = new int[m][2];
    for (int i = 0; i < m; i++) {
      st = new StringTokenizer(br.readLine());
      edges[i][0] = Integer.parseInt(st.nextToken());
      edges[i][1] = Integer.parseInt(st.nextToken());
    }
    ArrayList<int[]> ans = solve(n, edges);
    StringBuilder sb = new StringBuilder();
    for (int[] t : ans) {
      // 输出：编号 距离
      sb.append(t[1]).append(' ').append(t[0]).append('\n');
    }
    System.out.print(sb.toString());
  }
}
