import java.io.*;

public class Main {
  static String solve(int L, String g) {
    int cnt = 0;
    for (int i = 0; i < L; i++) if (g.charAt(i) == 'L') cnt++;
    return "L".repeat(cnt) + "R".repeat(L - cnt);
  }

  public static void main(String[] args) throws Exception {
    BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
    int q = Integer.parseInt(br.readLine().trim());
    StringBuilder out = new StringBuilder();
    while (q-- > 0) {
      int L = Integer.parseInt(br.readLine().trim());
      String g = br.readLine().trim();
      out.append(solve(L, g)).append('\n');
    }
    System.out.print(out);
  }
}
