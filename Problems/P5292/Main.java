import java.io.*;

public class Main {
  static boolean canReach(int n, long[] a, long m, int k, long x) {
    // 差分数组记录区间加何时失效
    long[] diff = new long[n + 1];
    long add = 0, used = 0;
    for (int i = 0; i < n; i++) {
      add += diff[i];
      long need = x - a[i] - add;
      if (need > 0) {
        used += need;
        if (used > m) return false;
        // 左端钉在 i，窗口尽量长为 k
        add += need;
        long end = i + (long) k;
        if (end < n) diff[(int) end] -= need;
      }
    }
    return true;
  }

  static long solve(int n, long m, int k, long[] a) {
    // 二分最终最小值
    long lo = a[0];
    for (int i = 1; i < n; i++) lo = Math.min(lo, a[i]);
    long hi = lo + m, ans = lo;
    while (lo <= hi) {
      long mid = lo + (hi - lo) / 2;
      if (canReach(n, a, m, k, mid)) {
        ans = mid;
        lo = mid + 1;
      } else {
        hi = mid - 1;
      }
    }
    return ans;
  }

  public static void main(String[] args) throws IOException {
    BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
    // 第一行 n,m,k，第二行 n 个数
    String[] sp = br.readLine().trim().split("\\s+");
    int n = Integer.parseInt(sp[0]);
    long m = Long.parseLong(sp[1]);
    int k = Integer.parseInt(sp[2]);
    String[] sa = br.readLine().trim().split("\\s+");
    long[] a = new long[n];
    for (int i = 0; i < n; i++) a[i] = Long.parseLong(sa[i]);
    System.out.println(solve(n, m, k, a));
  }
}
