import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.StringTokenizer;

public class Main {
  static final long INF = (long) 1e18;

  static long solve(int k, int q, int w, int[] v) {
    // 每个位置只补 0..q-1；链上后面的格由模关系唯一确定
    if (w == 1) {
      long ans = 0;
      for (int i = 0; i < k; i++) ans += (q - v[i] % q) % q;
      return ans;
    }
    int[] pref = new int[k + 1];
    for (int i = 0; i < k; i++) pref[i + 1] = pref[i] + v[i];
    int nwin = k - w + 1;
    int[] s = new int[nwin];
    for (int p = 0; p < nwin; p++) s[p] = ((pref[p + w] - pref[p]) % q + q) % q;
    int need = ((-s[0]) % q + q) % q;
    if (w == k) return need;

    long[][] chain = new long[w][q];
    for (int r = 0; r < w; r++) {
      for (int x = 0; x < q; x++) {
        long cost = x;
        int cur = x;
        int p = r;
        while (p + w < k) {
          cur = (cur + s[p] - s[p + 1]) % q;
          if (cur < 0) cur += q;
          cost += cur;
          p += w;
        }
        chain[r][x] = cost;
      }
    }

    long[] dp = new long[q];
    for (int i = 0; i < q; i++) dp[i] = INF;
    dp[0] = 0;
    for (int r = 0; r < w; r++) {
      long[] ndp = new long[q];
      for (int i = 0; i < q; i++) ndp[i] = INF;
      for (int md = 0; md < q; md++) {
        if (dp[md] >= INF) continue;
        for (int x = 0; x < q; x++) {
          int j = md + x;
          if (j >= q) j -= q;
          long val = dp[md] + chain[r][x];
          if (val < ndp[j]) ndp[j] = val;
        }
      }
      dp = ndp;
    }
    return dp[need];
  }

  public static void main(String[] args) throws IOException {
    BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
    StringTokenizer st = new StringTokenizer(br.readLine());
    int k = Integer.parseInt(st.nextToken());
    int q = Integer.parseInt(st.nextToken());
    int w = Integer.parseInt(st.nextToken());
    st = new StringTokenizer(br.readLine());
    int[] v = new int[k];
    for (int i = 0; i < k; i++) v[i] = Integer.parseInt(st.nextToken());
    System.out.println(solve(k, q, w, v));
  }
}
