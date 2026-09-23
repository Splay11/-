import java.io.*;
import java.util.*;

public class Main {
  static int n;
  static int[] dist;

  // 反转三进制状态左边 p 位，对应把前缀倒过来
  static int revPrefix(int x, int p) {
    int[] d = new int[n];
    int t = x;
    for (int i = n - 1; i >= 0; i--) {
      d[i] = t % 3;
      t /= 3;
    }
    int i = 0, j = p - 1;
    while (i < j) {
      int tmp = d[i];
      d[i] = d[j];
      d[j] = tmp;
      i++;
      j--;
    }
    int y = 0;
    for (int k = 0; k < n; k++) y = y * 3 + d[k];
    return y;
  }

  static void build() {
    int tot = 1;
    for (int i = 0; i < n; i++) tot *= 3;
    dist = new int[tot];
    Arrays.fill(dist, -1);
    ArrayDeque<Integer> q = new ArrayDeque<>();
    // 枚举 A、B 个数，构造全部已经排好序的串
    for (int na = 0; na <= n; na++) {
      for (int nb = 0; nb <= n - na; nb++) {
        int nc = n - na - nb;
        int x = 0;
        for (int i = 0; i < na; i++) x = x * 3;
        for (int i = 0; i < nb; i++) x = x * 3 + 1;
        for (int i = 0; i < nc; i++) x = x * 3 + 2;
        dist[x] = 0;
        q.add(x);
      }
    }
    // 从有序串向外搜，得到每个串的最少前缀反转次数
    while (!q.isEmpty()) {
      int x = q.poll();
      int d0 = dist[x];
      for (int p = 2; p <= n; p++) {
        int y = revPrefix(x, p);
        if (dist[y] < 0) {
          dist[y] = d0 + 1;
          q.add(y);
        }
      }
    }
  }

  static int encode(String s) {
    int x = 0;
    for (int i = 0; i < s.length(); i++) x = x * 3 + (s.charAt(i) - 'A');
    return x;
  }

  public static void main(String[] args) throws IOException {
    BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
    String[] nq = br.readLine().trim().split("\\s+");
    n = Integer.parseInt(nq[0]);
    int qn = Integer.parseInt(nq[1]);
    build();
    StringBuilder out = new StringBuilder();
    for (int i = 0; i < qn; i++) {
      String s = br.readLine().trim();
      out.append(dist[encode(s)]).append('\n');
    }
    System.out.print(out);
  }
}
