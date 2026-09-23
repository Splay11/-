import java.util.Scanner;

public class Main {
  static int solve(String w) {
    // 对每个色号，先丢掉比它大的格子，再数它自己的连续段
    int ans = 0;
    int n = w.length();
    for (int c = 0; c < 26; c++) {
      char ch = (char) ('a' + c);
      boolean inRun = false;
      for (int i = 0; i < n; i++) {
        char x = w.charAt(i);
        if (x > ch) continue;
        if (x == ch) {
          if (!inRun) {
            ans++;
            inRun = true;
          }
        } else {
          // 碰到更小色号，当前段被已经喷好的格子隔开
          inRun = false;
        }
      }
    }
    return ans;
  }

  public static void main(String[] args) {
    Scanner sc = new Scanner(System.in);
    String w = sc.next();
    System.out.println(solve(w));
    sc.close();
  }
}
