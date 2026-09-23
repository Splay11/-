import java.io.*;

public class Main {
  static int solve(int n, int[] a) {
    // 从左到右扫：左边按过的次数决定当前位被翻转了几次
    int ans = 0, flip = 0;
    for (int i = 0; i < n; i++) {
      // 当前实际状态 = 初值异或「左边已按次数的奇偶」
      int cur = a[i] ^ flip;
      if (cur == 0) {
        // 离开前必须按一次，否则这盏灯再也改不回来
        ans++;
        flip ^= 1;
      }
    }
    return ans;
  }

  public static void main(String[] args) throws IOException {
    BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
    // 第一行长度，第二行 0/1 序列
    int n = Integer.parseInt(br.readLine().trim());
    String[] sp = br.readLine().trim().split("\\s+");
    int[] a = new int[n];
    for (int i = 0; i < n; i++) a[i] = Integer.parseInt(sp[i]);
    System.out.println(solve(n, a));
  }
}
