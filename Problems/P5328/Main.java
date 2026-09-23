import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.StringTokenizer;

public class Main {
  static String solve(int k, int[] v) {
    // 贪心：货一到就入栈，栈顶刚好是下一个该出的号就立刻出
    int[] st = new int[k];
    int top = 0;
    StringBuilder ops = new StringBuilder();
    int need = 1;
    for (int i = 0; i < k; i++) {
      st[top++] = v[i];
      ops.append('I');
      while (top > 0 && st[top - 1] == need) {
        top--;
        ops.append('O');
        need++;
      }
    }
    if (need == k + 1) return ops.toString();
    return "N";
  }

  public static void main(String[] args) throws IOException {
    // 货件可达 200000，Scanner 可能超时
    BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
    int k = Integer.parseInt(br.readLine().trim());
    StringTokenizer stt = new StringTokenizer(br.readLine());
    int[] v = new int[k];
    for (int i = 0; i < k; i++) v[i] = Integer.parseInt(stt.nextToken());
    System.out.println(solve(k, v));
  }
}
