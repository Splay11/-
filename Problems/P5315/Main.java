import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.StringTokenizer;

public class Main {
  static BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
  static StringTokenizer st;

  static String next() throws IOException {
    while (st == null || !st.hasMoreTokens()) {
      st = new StringTokenizer(br.readLine());
    }
    return st.nextToken();
  }

  static int nextInt() throws IOException {
    return Integer.parseInt(next());
  }

  static long nextLong() throws IOException {
    return Long.parseLong(next());
  }

  static ArrayList<Integer> solve(int p, int s, long[] r) {
    // 单调栈求左右最近的不低于自己的测站
    int[] left = new int[p];
    int[] right = new int[p];
    int[] st = new int[p];
    int top = 0;
    for (int i = 0; i < p; i++) {
      while (top > 0 && r[st[top - 1]] < r[i]) top--;
      left[i] = top == 0 ? -1 : st[top - 1];
      st[top++] = i;
    }
    top = 0;
    for (int i = p - 1; i >= 0; i--) {
      while (top > 0 && r[st[top - 1]] < r[i]) top--;
      right[i] = top == 0 ? p : st[top - 1];
      st[top++] = i;
    }
    ArrayList<Integer> peaks = new ArrayList<Integer>();
    for (int i = 0; i < p; i++) {
      // 半径 s 内不能出现 >= r[i] 的其他测站
      boolean okL = left[i] < 0 || i - left[i] > s;
      boolean okR = right[i] >= p || right[i] - i > s;
      if (okL && okR) peaks.add(i + 1);
    }
    return peaks;
  }

  public static void main(String[] args) throws IOException {
    // 测站个数可达 200000，Scanner 会超时，改用缓冲读入
    int p = nextInt();
    int s = nextInt();
    long[] r = new long[p];
    for (int i = 0; i < p; i++) r[i] = nextLong();
    ArrayList<Integer> peaks = solve(p, s, r);
    StringBuilder sb = new StringBuilder();
    sb.append(peaks.size()).append('\n');
    for (int i = 0; i < peaks.size(); i++) {
      if (i > 0) sb.append(' ');
      sb.append(peaks.get(i));
    }
    sb.append('\n');
    System.out.print(sb.toString());
  }
}
