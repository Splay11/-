import java.io.*;
import java.util.*;

public class Main {
  static final int MAXM = 2000;
  static final int THRESH = 500;

  static int n;
  static int[] w, a, b;
  static long[] prefixB, suffixB;
  static long[][] f;

  static long applyFrom(int i, long money) {
    if (i >= n) return money;
    if (money > THRESH && money - suffixB[i] > THRESH) return money - suffixB[i];
    if (money < MAXM) return f[i][(int) money];
    int j = i;
    long cur = money;
    while (j < n && cur > THRESH) {
      cur -= b[j];
      j++;
    }
    if (j >= n) return cur;
    return f[j][(int) cur];
  }

  static long answer(long x) {
    if (x < MAXM) return f[0][(int) x];
    if (x - suffixB[0] > THRESH) return x - suffixB[0];
    int lo = 0, hi = n;
    while (lo < hi) {
      int mid = (lo + hi + 1) / 2;
      if (x - prefixB[mid] > THRESH) lo = mid;
      else hi = mid - 1;
    }
    int i = lo;
    long money = x - prefixB[i];
    if (i >= n) return money;
    return applyFrom(i, money);
  }

  public static void main(String[] args) throws IOException {
    BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
    n = Integer.parseInt(br.readLine());
    w = new int[n];
    a = new int[n];
    b = new int[n];
    for (int i = 0; i < n; i++) {
      String[] sp = br.readLine().split(" ");
      w[i] = Integer.parseInt(sp[0]);
      a[i] = Integer.parseInt(sp[1]);
      b[i] = Integer.parseInt(sp[2]);
    }

    prefixB = new long[n + 1];
    suffixB = new long[n + 1];
    for (int i = 0; i < n; i++) prefixB[i + 1] = prefixB[i] + b[i];
    for (int i = n - 1; i >= 0; i--) suffixB[i] = suffixB[i + 1] + b[i];

    f = new long[n + 1][MAXM];
    for (int m = 0; m < MAXM; m++) f[n][m] = m;

    for (int i = n - 1; i >= 0; i--) {
      for (int m = 0; m < MAXM; m++) {
        long nm;
        if (w[i] < m) {
          nm = m - b[i];
          if (nm < 0) nm = 0;
        } else {
          nm = m + a[i];
        }
        if (nm >= MAXM) {
          if (nm - suffixB[i + 1] > THRESH) {
            f[i][m] = nm - suffixB[i + 1];
          } else {
            int j = i;
            long cur = nm;
            while (j < n && cur > THRESH) {
              cur -= b[j];
              j++;
            }
            if (j >= n) f[i][m] = cur;
            else f[i][m] = f[j][(int) cur];
          }
        } else {
          f[i][m] = f[i + 1][(int) nm];
        }
      }
    }

    int q = Integer.parseInt(br.readLine());
    StringBuilder out = new StringBuilder();
    while (q-- > 0) {
      long x = Long.parseLong(br.readLine());
      out.append(answer(x)).append('\n');
    }
    System.out.print(out);
  }
}
