import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.StringTokenizer;

public class Main {
  static int size;
  static int[] mx, mn, lz;

  static void app(int i, int v) {
    // 整段加上延迟标记
    mx[i] += v;
    mn[i] += v;
    lz[i] += v;
  }

  static void push(int i) {
    if (lz[i] != 0) {
      app(i * 2, lz[i]);
      app(i * 2 + 1, lz[i]);
      lz[i] = 0;
    }
  }

  static void pull(int i) {
    mx[i] = Math.max(mx[i * 2], mx[i * 2 + 1]);
    mn[i] = Math.min(mn[i * 2], mn[i * 2 + 1]);
  }

  static void add(int l, int r, int v, int i, int L, int R) {
    // 区间 [l,r] 上的 h 全部加 v
    if (r < L || R < l) return;
    if (l <= L && R <= r) {
      app(i, v);
      return;
    }
    push(i);
    int mid = (L + R) >> 1;
    add(l, r, v, i * 2, L, mid);
    add(l, r, v, i * 2 + 1, mid + 1, R);
    pull(i);
  }

  static int qmax(int l, int r, int i, int L, int R) {
    if (r < L || R < l) return Integer.MIN_VALUE / 4;
    if (l <= L && R <= r) return mx[i];
    push(i);
    int mid = (L + R) >> 1;
    return Math.max(qmax(l, r, i * 2, L, mid), qmax(l, r, i * 2 + 1, mid + 1, R));
  }

  static int leftEq(int l, int r, int val, int i, int L, int R) {
    // [l,r] 里最左的、h 恰好等于 val 的位置；没有则返回 -1
    if (r < L || R < l || mx[i] < val || mn[i] > val) return -1;
    if (L == R) return mx[i] == val ? L : -1;
    push(i);
    int mid = (L + R) >> 1;
    int a = leftEq(l, r, val, i * 2, L, mid);
    if (a != -1) return a;
    return leftEq(l, r, val, i * 2 + 1, mid + 1, R);
  }

  static String solve(int k, int[] p, int[] q) {
    // 共有 k+1 个窗。装满段不能留空；某段人比窗多则全是 0
    int m = k + 1;
    ArrayList<ArrayList<Integer>> byR = new ArrayList<ArrayList<Integer>>();
    for (int i = 0; i < m + 2; i++) byR.add(new ArrayList<Integer>());
    for (int i = 0; i < k; i++) byR.get(q[i]).add(p[i]);

    size = 1;
    while (size < m + 2) size *= 2;
    mx = new int[size * 2];
    mn = new int[size * 2];
    lz = new int[size * 2];
    for (int i = 1; i <= m + 1; i++) {
      mx[size + i] = i;
      mn[size + i] = i;
    }
    for (int i = size - 1; i >= 1; i--) {
      mx[i] = Math.max(mx[i * 2], mx[i * 2 + 1]);
      mn[i] = Math.min(mn[i * 2], mn[i * 2 + 1]);
    }

    int total = 0;
    boolean overflow = false;
    int[] diff = new int[m + 3];
    int[] freq = new int[m + 2];
    int[] touched = new int[m + 2];
    for (int R = 1; R <= m; R++) {
      // 右端点等于 R 的人加入；相同左端点合并成一次区间加
      ArrayList<Integer> cur = byR.get(R);
      if (cur.isEmpty()) continue;
      int nt = 0;
      for (int x : cur) {
        if (freq[x] == 0) touched[nt++] = x;
        freq[x]++;
      }
      for (int i = 0; i < nt; i++) {
        int x = touched[i];
        int c = freq[x];
        freq[x] = 0;
        total += c;
        if (x + 1 <= m) add(x + 1, m, -c, 1, 0, size - 1);
      }
      if (overflow) continue;
      int gmx = qmax(1, R, 1, 0, size - 1) + total - (R + 1);
      if (gmx > 0) {
        overflow = true;
      } else if (gmx == 0) {
        int target = (R + 1) - total;
        int L = leftEq(1, R, target, 1, 0, size - 1);
        if (L != -1) {
          diff[L]++;
          diff[R + 1]--;
        }
      }
    }
    if (overflow) {
      StringBuilder sb = new StringBuilder(m);
      for (int i = 0; i < m; i++) sb.append('0');
      return sb.toString();
    }
    StringBuilder ans = new StringBuilder(m);
    int s = 0;
    for (int t = 1; t <= m; t++) {
      s += diff[t];
      ans.append(s > 0 ? '0' : '1');
    }
    return ans.toString();
  }

  public static void main(String[] args) throws IOException {
    // 行数可达 2e5，不用 Scanner
    BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
    int k = Integer.parseInt(br.readLine().trim());
    int[] p = new int[k];
    int[] q = new int[k];
    for (int i = 0; i < k; i++) {
      StringTokenizer st = new StringTokenizer(br.readLine());
      p[i] = Integer.parseInt(st.nextToken());
      q[i] = Integer.parseInt(st.nextToken());
    }
    System.out.println(solve(k, p, q));
  }
}
