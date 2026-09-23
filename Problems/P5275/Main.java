import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.StringTokenizer;

public class Main {
  static int[][] solve(int r, int c, int[][] a) {
    // 层和列对调：新表第 j 行第 i 列 = 原表第 i 行第 j 列
    int[][] b = new int[c][r];
    for (int j = 0; j < c; j++) {
      for (int i = 0; i < r; i++) {
        b[j][i] = a[i][j];
      }
    }
    return b;
  }

  public static void main(String[] args) throws IOException {
    // 规模可达 1000×1000，用 BufferedReader
    BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
    StringTokenizer st = new StringTokenizer(br.readLine());
    int r = Integer.parseInt(st.nextToken());
    int c = Integer.parseInt(st.nextToken());
    int[][] a = new int[r][c];
    for (int i = 0; i < r; i++) {
      st = new StringTokenizer(br.readLine());
      for (int j = 0; j < c; j++) a[i][j] = Integer.parseInt(st.nextToken());
    }
    int[][] b = solve(r, c, a);
    StringBuilder sb = new StringBuilder();
    for (int j = 0; j < c; j++) {
      for (int i = 0; i < r; i++) {
        if (i > 0) sb.append(' ');
        sb.append(b[j][i]);
      }
      sb.append('\n');
    }
    System.out.print(sb.toString());
  }
}
