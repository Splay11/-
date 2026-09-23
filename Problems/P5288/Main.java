import java.io.*;

public class Main {
  static int solve(int n, String s, int m) {
    // 统计 26 种类型各自出现次数
    int[] cnt = new int[26];
    for (int i = 0; i < s.length(); i++) {
      cnt[s.charAt(i) - 'A']++;
    }
    // 出现次数最多的那种，以及并列最多的种类数
    int mx = 0;
    for (int c : cnt) mx = Math.max(mx, c);
    int kinds = 0;
    for (int c : cnt) {
      if (c == mx) kinds++;
    }
    // 用最多种类搭框架：(mx-1) 个完整「处理+冷却」段，最后再放下 kinds 个
    // 若其它单据足够填满空档，答案就是总张数 n
    int frame = (mx - 1) * (m + 1) + kinds;
    return Math.max(n, frame);
  }

  public static void main(String[] args) throws IOException {
    BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
    // 第一行张数，第二行类型串，第三行冷却长度
    int n = Integer.parseInt(br.readLine().trim());
    String s = br.readLine().trim();
    int m = Integer.parseInt(br.readLine().trim());
    System.out.println(solve(n, s, m));
  }
}
