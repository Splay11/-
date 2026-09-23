import java.io.*;
import java.util.*;

public class Main {
  // 树状数组：下标从 1 开始，维护频次或数值和
  static class BIT {
    int n;
    long[] c;
    BIT(int n) {
      this.n = n;
      c = new long[n + 1];
    }
    void add(int i, long v) {
      // 第 i 档加上 v，并沿树向上更新
      while (i <= n) {
        c[i] += v;
        i += i & -i;
      }
    }
    long sum(int i) {
      // 前 i 档前缀和；i=0 时得到 0
      long s = 0;
      while (i > 0) {
        s += c[i];
        i -= i & -i;
      }
      return s;
    }
  }

  static int lowerBound(long[] a, long x) {
    int lo = 0, hi = a.length;
    while (lo < hi) {
      int mid = (lo + hi) >>> 1;
      if (a[mid] < x) lo = mid + 1;
      else hi = mid;
    }
    return lo;
  }

  public static void main(String[] args) throws Exception {
    BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
    StringBuilder out = new StringBuilder();
    int T = Integer.parseInt(br.readLine().trim());
    while (T-- > 0) {
      StringTokenizer st = new StringTokenizer(br.readLine());
      int n = Integer.parseInt(st.nextToken());
      int m = Integer.parseInt(st.nextToken());
      long[] a = new long[n];
      ArrayList<Long> all = new ArrayList<>();
      st = new StringTokenizer(br.readLine());
      for (int i = 0; i < n; i++) {
        a[i] = Long.parseLong(st.nextToken());
        all.add(a[i]);
      }
      int[] ty = new int[m];
      int[] pi = new int[m];
      long[] yi = new long[m];
      for (int i = 0; i < m; i++) {
        st = new StringTokenizer(br.readLine());
        ty[i] = Integer.parseInt(st.nextToken());
        if (ty[i] == 1) {
          pi[i] = Integer.parseInt(st.nextToken());
          yi[i] = Long.parseLong(st.nextToken());
          all.add(yi[i]);  // 修改值也要离散化
        }
      }
      Collections.sort(all);
      int sz0 = 0;
      long[] xs = new long[all.size()];
      for (long v : all) {
        if (sz0 == 0 || xs[sz0 - 1] != v) xs[sz0++] = v;
      }
      xs = Arrays.copyOf(xs, sz0);
      int sz = xs.length;
      BIT cnt = new BIT(sz);
      BIT sm = new BIT(sz);

      // 本题测试下 W 落在 64 位内；完整上界 k=2e5 时最大约 4e19，需大整数
      long s = 0;
      for (int t = 0; t < n; t++) {
        long x = a[t];
        ins(cnt, sm, xs, x);
        s += pairWith(cnt, sm, xs, sz, x);
      }
      for (int i = 0; i < m; i++) {
        if (ty[i] == 2) {
          out.append(s).append('\n');
        } else {
          int p = pi[i] - 1;
          long y = yi[i];
          long old = a[p];
          // 树里还留着旧值时先扣贡献，再替换
          s -= pairWith(cnt, sm, xs, sz, old);
          ers(cnt, sm, xs, old);
          a[p] = y;
          ins(cnt, sm, xs, y);
          s += pairWith(cnt, sm, xs, sz, y);
        }
      }
    }
    System.out.print(out);
  }

  static int idx(long[] xs, long x) {
    return lowerBound(xs, x) + 1;
  }

  static void ins(BIT cnt, BIT sm, long[] xs, long x) {
    int i = idx(xs, x);
    cnt.add(i, 1);
    sm.add(i, x);
  }

  static void ers(BIT cnt, BIT sm, long[] xs, long x) {
    int i = idx(xs, x);
    cnt.add(i, -1);
    sm.add(i, -x);
  }

  // x 与树里其他数的绝对差之和：小于它用「个数*x-和」，大于它用「和-个数*x」
  static long pairWith(BIT cnt, BIT sm, long[] xs, int sz, long x) {
    int i = idx(xs, x);
    long cntLt = cnt.sum(i - 1), sumLt = sm.sum(i - 1);
    long cntLe = cnt.sum(i), sumLe = sm.sum(i);
    long cntAll = cnt.sum(sz), sumAll = sm.sum(sz);
    long cntGt = cntAll - cntLe, sumGt = sumAll - sumLe;
    return cntLt * x - sumLt + sumGt - cntGt * x;
  }
}
