import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.BitSet;
import java.util.StringTokenizer;

public class Main {
  static final int CAP = 480;

  static boolean anyFrom(BitSet bs, int need) {
    // 是否存在支援耗时 s，满足 need <= s <= 480
    if (need > CAP) return false;
    int s = bs.nextSetBit(need);
    return s >= 0 && s <= CAP;
  }

  static boolean can(int limit, int[] dur, int days, int helpK) {
    // 判断主责单日上限为 limit 时，能否在 days 天内按顺序做完
    int n = dur.length;
    int i = 0, used = 0;
    while (i < n) {
      used++;
      if (used > days) return false;
      BitSet[] dp = new BitSet[helpK + 1];
      for (int t = 0; t <= helpK; t++) dp[t] = new BitSet(CAP + 1);
      dp[0].set(0);
      int total = 0;
      int last = i - 1;
      for (int j = i; j < n; j++) {
        int x = dur[j];
        total += x;
        BitSet[] ndp = new BitSet[helpK + 1];
        for (int t = 0; t <= helpK; t++) ndp[t] = new BitSet(CAP + 1);
        if (x <= limit) {
          // 主责可做：留给自己，或交给支援
          for (int t = 0; t <= helpK; t++) {
            ndp[t].or(dp[t]);
            if (t > 0) {
              for (int s = dp[t - 1].nextSetBit(0); s >= 0; s = dp[t - 1].nextSetBit(s + 1)) {
                if (s + x <= CAP) ndp[t].set(s + x);
              }
            }
          }
        } else {
          // 必须交给支援
          for (int t = 1; t <= helpK; t++) {
            for (int s = dp[t - 1].nextSetBit(0); s >= 0; s = dp[t - 1].nextSetBit(s + 1)) {
              if (s + x <= CAP) ndp[t].set(s + x);
            }
          }
        }
        int need = total - limit;
        if (need < 0) need = 0;
        boolean ok = false;
        for (int t = 0; t <= helpK; t++) {
          if (anyFrom(ndp[t], need)) {
            ok = true;
            break;
          }
        }
        if (!ok) break;
        dp = ndp;
        last = j;
      }
      if (last < i) return false;
      i = last + 1;
    }
    return true;
  }

  static int solve(int n, int m, int k, int[] dur) {
    if (!can(480, dur, m, k)) return -1;
    int lo = 0, hi = 480;
    while (lo < hi) {
      int mid = (lo + hi) / 2;
      if (can(mid, dur, m, k)) hi = mid;
      else lo = mid + 1;
    }
    return lo;
  }

  public static void main(String[] args) throws IOException {
    BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
    StringTokenizer st = new StringTokenizer(br.readLine());
    int n = Integer.parseInt(st.nextToken());
    int m = Integer.parseInt(st.nextToken());
    int k = Integer.parseInt(st.nextToken());
    st = new StringTokenizer(br.readLine());
    int[] dur = new int[n];
    for (int i = 0; i < n; i++) dur[i] = Integer.parseInt(st.nextToken());
    System.out.println(solve(n, m, k, dur));
  }
}
