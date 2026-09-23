import java.io.*;
import java.util.*;

public class Main {
  static long countBest(int s, int pL, int pR, int qL, int qR) {
    long[] dp = new long[16];
    dp[15] = 1;
    for (int pos = 30; pos >= 0; pos--) {
      int sb = (s >> pos) & 1;
      int plb = (pL >> pos) & 1, prb = (pR >> pos) & 1;
      int qlb = (qL >> pos) & 1, qrb = (qR >> pos) & 1;
      long[] nz = new long[16], no = new long[16];
      boolean hasOne = false;
      for (int st = 0; st < 16; st++) {
        long cnt = dp[st];
        if (cnt == 0) continue;
        int eqPL = st & 1, eqPR = (st >> 1) & 1;
        int eqQL = (st >> 2) & 1, eqQR = (st >> 3) & 1;
        for (int pb = 0; pb <= 1; pb++) {
          if (eqPL == 1 && pb < plb) continue;
          if (eqPR == 1 && pb > prb) continue;
          int nPL = (eqPL == 1 && pb == plb) ? 1 : 0;
          int nPR = (eqPR == 1 && pb == prb) ? 1 : 0;
          for (int qb = 0; qb <= 1; qb++) {
            if (eqQL == 1 && qb < qlb) continue;
            if (eqQR == 1 && qb > qrb) continue;
            int nQL = (eqQL == 1 && qb == qlb) ? 1 : 0;
            int nQR = (eqQR == 1 && qb == qrb) ? 1 : 0;
            int ns = nPL | (nPR << 1) | (nQL << 2) | (nQR << 3);
            int cur = sb ^ pb ^ qb;
            if (cur == 1) { no[ns] += cnt; hasOne = true; }
            else nz[ns] += cnt;
          }
        }
      }
      dp = hasOne ? no : nz;
    }
    long ans = 0;
    for (long v : dp) ans += v;
    return ans;
  }

  public static void main(String[] args) throws Exception {
    BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
    int q = Integer.parseInt(br.readLine().trim());
    StringBuilder out = new StringBuilder();
    while (q-- > 0) {
      StringTokenizer st = new StringTokenizer(br.readLine());
      int s = Integer.parseInt(st.nextToken());
      st = new StringTokenizer(br.readLine());
      int pL = Integer.parseInt(st.nextToken()), pR = Integer.parseInt(st.nextToken());
      st = new StringTokenizer(br.readLine());
      int qL = Integer.parseInt(st.nextToken()), qR = Integer.parseInt(st.nextToken());
      out.append(countBest(s, pL, pR, qL, qR)).append('\n');
    }
    System.out.print(out);
  }
}
