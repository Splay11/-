import java.util.Scanner;

public class Main {
  static int solve(String w) {
    // 扫一遍，相邻同色就断开，统计当前段长度
    int best = 1;
    int cur = 1;
    for (int i = 1; i < w.length(); i++) {
      if (w.charAt(i) != w.charAt(i - 1)) {
        cur++;
        if (cur > best) best = cur;
      } else {
        cur = 1;
      }
    }
    return best;
  }

  public static void main(String[] args) {
    Scanner sc = new Scanner(System.in);
    String w = sc.next();
    System.out.println(solve(w));
    sc.close();
  }
}
