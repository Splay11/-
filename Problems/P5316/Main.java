import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.StringTokenizer;
import java.util.TreeMap;

public class Main {
  static BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
  static StringTokenizer st;

  static String next() throws IOException {
    while (st == null || !st.hasMoreTokens()) {
      st = new StringTokenizer(br.readLine());
    }
    return st.nextToken();
  }

  static int nextInt() throws IOException {
    return Integer.parseInt(next());
  }

  // 动态 int 列表，避免 ArrayList<Integer> 装箱
  static class IL {
    int[] a = new int[2];
    int n;
    void add(int x) {
      if (n == a.length) {
        int[] b = new int[n * 2];
        for (int i = 0; i < n; i++) b[i] = a[i];
        a = b;
      }
      a[n++] = x;
    }
  }

  static void add(TreeMap<Integer, Integer> mp, int x) {
    Integer c = mp.get(x);
    mp.put(x, c == null ? 1 : c + 1);
  }

  static void remove(TreeMap<Integer, Integer> mp, int x) {
    int c = mp.get(x);
    if (c == 1) mp.remove(x);
    else mp.put(x, c - 1);
  }

  static int[] solve(int w, int[] v, IL[] addC, IL[] delC, IL[] addD, IL[] delD) {
    // hc 维护当前稀释上界，取最小；hd 维护当前回灌下界，取最大
    TreeMap<Integer, Integer> hc = new TreeMap<Integer, Integer>();
    TreeMap<Integer, Integer> hd = new TreeMap<Integer, Integer>();
    int inf = 2000000000;
    int[] e = new int[w];
    for (int i = 1; i <= w; i++) {
      for (int j = 0; j < delC[i].n; j++) remove(hc, delC[i].a[j]);
      for (int j = 0; j < addC[i].n; j++) add(hc, addC[i].a[j]);
      for (int j = 0; j < delD[i].n; j++) remove(hd, delD[i].a[j]);
      for (int j = 0; j < addD[i].n; j++) add(hd, addD[i].a[j]);
      int hi = hc.isEmpty() ? inf : hc.firstKey();
      int lo = hd.isEmpty() ? 0 : hd.lastKey();
      int val = v[i - 1];
      if (val < lo) val = lo;
      if (val > hi) val = hi;
      e[i - 1] = val;
    }
    return e;
  }

  public static void main(String[] args) throws IOException {
    // 断面个数可达 200000，Scanner 会超时，改用缓冲读入
    int w = nextInt();
    int x = nextInt();
    int y = nextInt();
    int[] v = new int[w];
    for (int i = 0; i < w; i++) v[i] = nextInt();
    IL[] addC = new IL[w + 2];
    IL[] delC = new IL[w + 2];
    IL[] addD = new IL[w + 2];
    IL[] delD = new IL[w + 2];
    for (int i = 0; i <= w + 1; i++) {
      addC[i] = new IL();
      delC[i] = new IL();
      addD[i] = new IL();
      delD[i] = new IL();
    }
    // 稀释闸 [L,R] 上界 c：L 加入，R+1 删除
    for (int i = 0; i < x; i++) {
      int L = nextInt(), R = nextInt(), c = nextInt();
      addC[L].add(c);
      delC[R + 1].add(c);
    }
    // 回灌泵 [L,R] 下界 d：同样拆成端点事件
    for (int i = 0; i < y; i++) {
      int L = nextInt(), R = nextInt(), d = nextInt();
      addD[L].add(d);
      delD[R + 1].add(d);
    }
    int[] e = solve(w, v, addC, delC, addD, delD);
    StringBuilder sb = new StringBuilder();
    for (int i = 0; i < w; i++) {
      if (i > 0) sb.append(' ');
      sb.append(e[i]);
    }
    sb.append('\n');
    System.out.print(sb.toString());
  }
}
