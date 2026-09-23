import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.StringTokenizer;

public class Main {
  // 返回：长度、左端点（从 1 起）、公共变化量
  static long[] solve(int n, long m, long[] a) {
    long bestLen = 1, bestL = 1, bestD = 0;
    if (n == 1) return new long[] {bestLen, bestL, bestD};
    int i = 0;
    while (i < n - 1) {
      long d = (a[i + 1] - a[i]) % m;
      if (d < 0) d += m;
      int j = i;
      while (j + 1 < n) {
        long cur = (a[j + 1] - a[j]) % m;
        if (cur < 0) cur += m;
        if (cur != d) break;
        j++;
      }
      long curLen = j - i + 1;
      // 更长才更新，同样长时保留更靠左的
      if (curLen > bestLen) {
        bestLen = curLen;
        bestL = i + 1;
        bestD = d;
      }
      i = j; // 下一段从当前段末尾接着比
    }
    return new long[] {bestLen, bestL, bestD};
  }

  public static void main(String[] args) throws IOException {
    // n 可达 2e5，用 BufferedReader
    BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
    StringTokenizer st = new StringTokenizer(br.readLine());
    int n = Integer.parseInt(st.nextToken());
    long m = Long.parseLong(st.nextToken());
    st = new StringTokenizer(br.readLine());
    long[] a = new long[n];
    for (int i = 0; i < n; i++) a[i] = Long.parseLong(st.nextToken());
    long[] ans = solve(n, m, a);
    System.out.println(ans[0] + " " + ans[1] + " " + ans[2]);
  }
}
