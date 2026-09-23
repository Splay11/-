import java.io.*;
import java.util.*;

public class Main {
  static double solve(int n, int[] fa, int[] w, int W) {
    // 建二叉树：每个点最多两个孩子
    int[][] ch = new int[n][2];
    int[] cnt = new int[n];
    for (int i = 1; i < n; i++) {
      int p = fa[i - 1];
      ch[p][cnt[p]++] = i;
    }

    int[] sz = new int[n];
    double[] sumw = new double[n];
    double[] edfn = new double[n];
    // 编号递增保证孩子更大，倒序就是自底向上
    for (int u = n - 1; u >= 0; u--) {
      double sw = w[u];
      int s = 1;
      for (int k = 0; k < cnt[u]; k++) {
        int v = ch[u][k];
        s += sz[v];
        sw += sumw[v];
      }
      sz[u] = s;
      sumw[u] = sw;
    }

    // 根的 DFS 序恒为 1，再往下推每个孩子的期望序
    edfn[0] = 1.0;
    int[] st = new int[n];
    int top = 0;
    st[top++] = 0;
    while (top > 0) {
      int u = st[--top];
      if (cnt[u] == 0) continue;
      if (cnt[u] == 1) {
        // 独子：下一个被访问的一定是它
        int v = ch[u][0];
        edfn[v] = edfn[u] + 1.0;
        st[top++] = v;
        continue;
      }
      int a = ch[u][0], b = ch[u][1];
      double wa = w[a], wb = w[b], s = wa + wb;
      // 先走兄弟整棵子树，会把对方子树大小加进自己的期望序
      edfn[a] = edfn[u] + 1.0 + (wb / s) * sz[b];
      edfn[b] = edfn[u] + 1.0 + (wa / s) * sz[a];
      st[top++] = a;
      st[top++] = b;
    }

    double base = 0;
    for (int i = 0; i < n; i++) base += w[i] * (n + 1.0 - edfn[i]);
    double best = base;

    // 枚举把某一个点改成 W；不改的情况已经在 base 里
    for (int x = 0; x < n; x++) {
      if (w[x] == W) continue;
      double extra = (W - w[x]) * (n + 1.0 - edfn[x]);
      int p = (x > 0) ? fa[x - 1] : -1;
      int sib = -1;
      if (p >= 0 && cnt[p] == 2) {
        sib = (ch[p][0] == x) ? ch[p][1] : ch[p][0];
      }
      if (sib >= 0) {
        // 改的是双孩子中的一侧，兄弟先后概率跟着变
        double wx = w[x], ws = w[sib];
        double oldDen = wx + ws, newDen = W + ws;
        double dx = (ws / newDen - ws / oldDen) * sz[sib];
        double ds = (W / newDen - wx / oldDen) * sz[x];
        extra -= dx * (sumw[x] - w[x] + W);
        extra -= ds * sumw[sib];
      }
      best = Math.max(best, base + extra);
    }
    return best;
  }

  public static void main(String[] args) throws IOException {
    BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
    // 点数、n-1 个父亲、n 个权值、目标权值
    int n = Integer.parseInt(br.readLine().trim());
    String faLine = br.readLine();
    int[] fa = new int[Math.max(0, n - 1)];
    if (n > 1) {
      String[] sp = faLine.trim().split("\\s+");
      for (int i = 0; i < n - 1; i++) fa[i] = Integer.parseInt(sp[i]);
    }
    String[] sw = br.readLine().trim().split("\\s+");
    int[] w = new int[n];
    for (int i = 0; i < n; i++) w[i] = Integer.parseInt(sw[i]);
    int W = Integer.parseInt(br.readLine().trim());
    System.out.printf("%.4f\n", solve(n, fa, w, W));
  }
}
