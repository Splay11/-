import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.StringTokenizer;

public class Main {
  static int n;
  static int[] parent, sgn;
  static long[] off, fixedv;
  static boolean[] has;

  // 迭代路径压缩，同时维护 c[x] = sgn[x] * c[root] + off[x]
  static int find(int x) {
    ArrayList<Integer> path = new ArrayList<Integer>();
    while (parent[x] != x) {
      path.add(x);
      x = parent[x];
    }
    int r = x;
    for (int i = path.size() - 1; i >= 0; i--) {
      int v = path.get(i);
      int p = parent[v];
      int os = sgn[v];
      sgn[v] = os * sgn[p];
      off[v] = off[v] + (long) os * off[p];
      parent[v] = r;
    }
    return r;
  }

  // 加入方程 c[a] + ka * c[b] = val
  static boolean add(int a, int b, int ka, long val) {
    int ra = find(a), rb = find(b);
    int sa = sgn[a], sb = sgn[b];
    long oa = off[a], ob = off[b];
    long rhs = val - oa - (long) ka * ob;
    if (ra == rb) {
      int coef = sa + ka * sb;
      if (coef == 0) return rhs == 0; // 冗余或矛盾
      if (rhs % coef != 0) return false; // 根不是整数
      long need = rhs / coef;
      if (has[ra] && fixedv[ra] != need) return false;
      has[ra] = true;
      fixedv[ra] = need;
      return true;
    }
    // 把 ra 挂到 rb
    parent[ra] = rb;
    sgn[ra] = -sa * ka * sb;
    off[ra] = sa * rhs;
    if (has[ra] && has[rb]) return fixedv[ra] == sgn[ra] * fixedv[rb] + off[ra];
    if (has[ra]) {
      // 已知 rA，反推 rB
      has[rb] = true;
      fixedv[rb] = sgn[ra] * (fixedv[ra] - off[ra]);
    }
    return true;
  }

  static long[] solve(int nn, char[] typ, int[] aa, int[] bb, long[] ww) {
    n = nn;
    parent = new int[n + 1];
    sgn = new int[n + 1];
    off = new long[n + 1];
    fixedv = new long[n + 1];
    has = new boolean[n + 1];
    for (int i = 1; i <= n; i++) {
      parent[i] = i;
      sgn[i] = 1;
    }
    for (int i = 0; i < typ.length; i++) {
      boolean ok = typ[i] == 'D' ? add(aa[i], bb[i], -1, ww[i]) : add(aa[i], bb[i], 1, ww[i]);
      if (!ok) return new long[] {0, -1}; // 第一维 0 表示 NO
    }
    boolean[] seen = new boolean[n + 1];
    long k = 0;
    for (int i = 1; i <= n; i++) {
      int r = find(i);
      if (!seen[r]) {
        seen[r] = true;
        if (!has[r]) k++; // 未钉死的根各贡献一个自由度
      }
    }
    return new long[] {1, k}; // 第一维 1 表示 YES
  }

  public static void main(String[] args) throws IOException {
    // 记录数可达 1e5，用 BufferedReader 避免 Scanner 超时
    BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
    StringTokenizer st = new StringTokenizer(br.readLine());
    int n = Integer.parseInt(st.nextToken());
    int m = Integer.parseInt(st.nextToken());
    char[] typ = new char[m];
    int[] a = new int[m];
    int[] b = new int[m];
    long[] w = new long[m];
    for (int i = 0; i < m; i++) {
      st = new StringTokenizer(br.readLine());
      typ[i] = st.nextToken().charAt(0);
      a[i] = Integer.parseInt(st.nextToken());
      b[i] = Integer.parseInt(st.nextToken());
      w[i] = Long.parseLong(st.nextToken());
    }
    long[] ans = solve(n, typ, a, b, w);
    if (ans[0] == 0) {
      System.out.println("NO");
      System.out.println(-1);
    } else {
      System.out.println("YES");
      System.out.println(ans[1]);
    }
  }
}
