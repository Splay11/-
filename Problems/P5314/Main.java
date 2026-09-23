import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.Arrays;
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

  static long solve(int k, int u, int v, long g, long[] h) {
    // 从小到大排完后从右往左取，等价于渗水量从大到小
    Arrays.sort(h);
    long ans = 0;
    for (int i = 0; i < k; i++) {
      long x = h[k - 1 - i];
      if (i < u) {
        // 封堵，该点残留为 0
        continue;
      }
      if (i < u + v) {
        // 引流，减去固定幅度 g
        long val = x - g;
        if (val < 0) val = 0;
        ans += val;
      } else {
        // 暂缓
        ans += x;
      }
    }
    return ans;
  }

  public static void main(String[] args) throws IOException {
    // 渗水点个数可达 200000，Scanner 会超时，改用缓冲读入
    int k = nextInt();
    int u = nextInt();
    int v = nextInt();
    long g = nextLong();
    long[] h = new long[k];
    for (int i = 0; i < k; i++) h[i] = nextLong();
    System.out.println(solve(k, u, v, g, h));
  }
}
