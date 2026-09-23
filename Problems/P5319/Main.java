import java.util.Scanner;

public class Main {
  static final long INF = 1000000000000000005L;

  static long add(long a, long b) {
    if (a > INF - b) return INF;
    return a + b;
  }

  static String solve(int m, long q, String b) {
    // ways0/ways1：定长、定开头色的交错子序列个数
    long[] ways0 = new long[m + 1];
    long[] ways1 = new long[m + 1];
    long[] pre0 = new long[m + 1];
    long[] pre1 = new long[m + 1];
    for (int i = 0; i < m; i++) {
      long[] cur = new long[m + 1];
      cur[1] = 1;
      if (b.charAt(i) == '0') {
        for (int L = 2; L <= i + 1; L++) cur[L] = pre1[L - 1];
      } else {
        for (int L = 2; L <= i + 1; L++) cur[L] = pre0[L - 1];
      }
      for (int L = 1; L <= i + 1; L++) {
        char start;
        if (L % 2 == 1) start = b.charAt(i);
        else start = b.charAt(i) == '0' ? '1' : '0';
        if (start == '0') ways0[L] = add(ways0[L], cur[L]);
        else ways1[L] = add(ways1[L], cur[L]);
      }
      if (b.charAt(i) == '0') {
        for (int L = 1; L <= i + 1; L++) pre0[L] = add(pre0[L], cur[L]);
      } else {
        for (int L = 1; L <= i + 1; L++) pre1[L] = add(pre1[L], cur[L]);
      }
    }
    // 空串占第 1 名，先扣掉
    q -= 1;
    for (int L = 1; L <= m; L++) {
      long[] cnts = new long[] {ways0[L], ways1[L]};
      for (int start = 0; start <= 1; start++) {
        if (q <= cnts[start]) {
          StringBuilder sb = new StringBuilder();
          int bit = start;
          for (int t = 0; t < L; t++) {
            sb.append((char) ('0' + bit));
            bit = 1 - bit;
          }
          return sb.toString();
        }
        q -= cnts[start];
      }
    }
    return "-1";
  }

  public static void main(String[] args) {
    Scanner sc = new Scanner(System.in);
    int m = sc.nextInt();
    long q = sc.nextLong();
    String b = sc.next();
    System.out.println(solve(m, q, b));
    sc.close();
  }
}
