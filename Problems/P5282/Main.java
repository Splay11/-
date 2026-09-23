import java.io.*;
import java.util.*;

public class Main {
  static Long maxSumLenGe(long[] a, int L) {
    int n = a.length;
    if (n < L) return null;
    long[] P = new long[n + 1];
    for (int i = 0; i < n; i++) P[i + 1] = P[i] + a[i];
    long best = P[L] - P[0];
    long mn = P[0];
    for (int r = L; r <= n; r++) {
      best = Math.max(best, P[r] - mn);
      int nxt = r - L + 1;
      if (nxt <= n && P[nxt] < mn) mn = P[nxt];
    }
    return best;
  }

  public static void main(String[] args) throws IOException {
    BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
    String[] nm = br.readLine().trim().split("\\s+");
    int n = Integer.parseInt(nm[0]), m = Integer.parseInt(nm[1]);
    int[][] g = new int[n][m];
    for (int i = 0; i < n; i++) {
      String[] row = br.readLine().trim().split("\\s+");
      for (int j = 0; j < m; j++) g[i][j] = Integer.parseInt(row[j]);
    }

    long ans = Long.MIN_VALUE / 4;
    for (int top = 0; top < n; top++) {
      long[] col = new long[m];
      for (int bottom = top; bottom < n; bottom++) {
        int h = bottom - top + 1;
        for (int j = 0; j < m; j++) col[j] += g[bottom][j];
        Long s = maxSumLenGe(col, h);
        if (s != null) ans = Math.max(ans, (long) h * s);
      }
    }
    for (int left = 0; left < m; left++) {
      long[] row = new long[n];
      for (int right = left; right < m; right++) {
        int w = right - left + 1;
        for (int i = 0; i < n; i++) row[i] += g[i][right];
        Long s = maxSumLenGe(row, w);
        if (s != null) ans = Math.max(ans, (long) w * s);
      }
    }
    System.out.println(ans);
  }
}
