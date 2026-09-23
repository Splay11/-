import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.Arrays;
import java.util.StringTokenizer;

public class Main {
  static long solve(int k, long q, long[] x, long[] y) {
    // 总残差 = sum(x)+sum(y) - q * 进位次数，尽量多配对满足 x+y >= q
    Arrays.sort(x);
    Arrays.sort(y);
    int i = k - 1;
    int j = 0;
    long wrap = 0;
    long sx = 0;
    long sy = 0;
    for (int t = 0; t < k; t++) {
      sx += x[t];
      sy += y[t];
    }
    // 从大到小看研发侧，配上还能进位的最小测试侧收益
    while (i >= 0 && j < k) {
      if (x[i] + y[j] >= q) {
        wrap++;
        i--;
        j++;
      } else {
        // 这个测试侧收益连当前最大研发侧都凑不齐
        j++;
      }
    }
    return sx + sy - wrap * q;
  }

  public static void main(String[] args) throws IOException {
    // k 可达 300000，不用 Scanner
    BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
    StringTokenizer st = new StringTokenizer(br.readLine());
    int k = Integer.parseInt(st.nextToken());
    long q = Long.parseLong(st.nextToken());
    st = new StringTokenizer(br.readLine());
    long[] x = new long[k];
    for (int i = 0; i < k; i++) x[i] = Long.parseLong(st.nextToken());
    st = new StringTokenizer(br.readLine());
    long[] y = new long[k];
    for (int i = 0; i < k; i++) y[i] = Long.parseLong(st.nextToken());
    System.out.println(solve(k, q, x, y));
  }
}
