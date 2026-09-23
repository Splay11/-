import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.StringTokenizer;

public class Main {
  static BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
  static StringTokenizer st;

  static String next() throws IOException {
    while (st == null || !st.hasMoreTokens()) {
      st = new StringTokenizer(br.readLine());
    }
    return st.nextToken();
  }

  static int nextInt() throws IOException {
    return Integer.parseInt(next());
  }

  static long nextLong() throws IOException {
    return Long.parseLong(next());
  }

  static long[] solve(int k, long t, long[] s) {
    // 在硐口 i 接通后，矿石再走 s[i]，值班员走 t
    // 等待就是多出来的时间，不能为负
    long[] ans = new long[k];
    for (int i = 0; i < k; i++) {
      long wait = s[i] - t;
      if (wait < 0) wait = 0;
      ans[i] = wait;
    }
    return ans;
  }

  public static void main(String[] args) throws IOException {
    // 硐口个数可达 100000，一行很长，Scanner 可能超时
    int k = nextInt();
    long t = nextLong();
    long[] s = new long[k];
    for (int i = 0; i < k; i++) s[i] = nextLong();
    long[] ans = solve(k, t, s);
    StringBuilder sb = new StringBuilder();
    for (int i = 0; i < k; i++) {
      if (i > 0) sb.append(' ');
      sb.append(ans[i]);
    }
    sb.append('\n');
    System.out.print(sb.toString());
  }
}
