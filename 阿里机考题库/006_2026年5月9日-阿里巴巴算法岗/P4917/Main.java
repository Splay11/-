import java.io.*;
import java.util.*;

public class Main {
  static int[] build(int m) {
    // 总和为奇数时无法正负平分
    if (m % 4 == 1 || m % 4 == 2) return null;
    int[] w = new int[m];
    int idx = 0, start;
    if (m % 4 == 3) {
      w[idx++] = 1;
      w[idx++] = 2;
      w[idx++] = -3;
      start = 4;
    } else start = 1;
    for (int x = start; x <= m; x += 4) {
      w[idx++] = x;
      w[idx++] = -(x + 1);
      w[idx++] = -(x + 2);
      w[idx++] = x + 3;
    }
    return w;
  }

  public static void main(String[] args) throws Exception {
    BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
    int q = Integer.parseInt(br.readLine().trim());
    StringBuilder out = new StringBuilder();
    while (q-- > 0) {
      int m = Integer.parseInt(br.readLine().trim());
      int[] w = build(m);
      if (w == null) out.append("-1\n");
      else {
        for (int i = 0; i < m; i++) {
          if (i > 0) out.append(' ');
          out.append(w[i]);
        }
        out.append('\n');
      }
    }
    System.out.print(out);
  }
}
