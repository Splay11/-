import java.util.Arrays;
import java.util.Comparator;
import java.util.Scanner;

public class Main {
  static long pickMedian(long[][] pts) {
    // 按坐标排序后，累加人数，找到加权中位数
    Arrays.sort(pts, new Comparator<long[]>() {
      public int compare(long[] x, long[] y) {
        if (x[0] < y[0]) return -1;
        if (x[0] > y[0]) return 1;
        return 0;
      }
    });
    long tot = 0;
    for (int i = 0; i < pts.length; i++) tot += pts[i][1];
    long acc = 0;
    for (int i = 0; i < pts.length; i++) {
      acc += pts[i][1];
      // 前缀人数第一次达到总人数的一半，就是最优落点
      if (acc * 2 >= tot) return pts[i][0];
    }
    return pts[pts.length - 1][0];
  }

  static long solve(int m, long[] a, long[] b, long[] w) {
    long[][] xs = new long[m][2];
    long[][] ys = new long[m][2];
    for (int i = 0; i < m; i++) {
      xs[i][0] = a[i];
      xs[i][1] = w[i];
      ys[i][0] = b[i];
      ys[i][1] = w[i];
    }
    // 横、纵分别取加权中位数
    long P = pickMedian(xs);
    long Q = pickMedian(ys);
    long ans = 0;
    for (int i = 0; i < m; i++) {
      ans += w[i] * (Math.abs(a[i] - P) + Math.abs(b[i] - Q));
    }
    return ans;
  }

  public static void main(String[] args) {
    Scanner sc = new Scanner(System.in);
    int m = sc.nextInt();
    long[] a = new long[m];
    long[] b = new long[m];
    long[] w = new long[m];
    for (int i = 0; i < m; i++) {
      a[i] = sc.nextLong();
      b[i] = sc.nextLong();
      w[i] = sc.nextLong();
    }
    System.out.println(solve(m, a, b, w));
    sc.close();
  }
}
