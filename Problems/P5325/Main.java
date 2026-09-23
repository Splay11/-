import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
  static final int MOD = 1000000007;
  static final int MAXK = 200000;

  static long[] precompute() {
    // f1/f2/f3：长度为 i、结尾恰好连续 1/2/3 格同色的方案数
    long[] f1 = new long[MAXK + 1];
    long[] f2 = new long[MAXK + 1];
    long[] f3 = new long[MAXK + 1];
    long[] tot = new long[MAXK + 1];
    f1[1] = 26;
    tot[1] = 26;
    for (int i = 2; i <= MAXK; i++) {
      // 换色另起一连
      f1[i] = tot[i - 1] * 25 % MOD;
      // 一连延长成两连
      f2[i] = f1[i - 1];
      // 两连延长成三连，不能再变成四连
      f3[i] = f2[i - 1];
      tot[i] = (f1[i] + f2[i] + f3[i]) % MOD;
    }
    return tot;
  }

  static long[] solve(long[] tot, int[] ks) {
    long[] ans = new long[ks.length];
    for (int i = 0; i < ks.length; i++) ans[i] = tot[ks[i]];
    return ans;
  }

  public static void main(String[] args) throws IOException {
    // 询问可达 200000 行，Scanner 会超时
    BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
    int q = Integer.parseInt(br.readLine().trim());
    int[] ks = new int[q];
    for (int i = 0; i < q; i++) ks[i] = Integer.parseInt(br.readLine().trim());
    long[] tot = precompute();
    long[] ans = solve(tot, ks);
    StringBuilder sb = new StringBuilder();
    for (int i = 0; i < q; i++) sb.append(ans[i]).append('\n');
    System.out.print(sb.toString());
  }
}
