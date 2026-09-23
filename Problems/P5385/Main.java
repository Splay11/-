import java.util.Arrays;
import java.util.Scanner;

public class Main {
    // 在 1-边构成的二分图上求最大匹配；得分 = 2*匹配 - m
    static int maxMatching(int[][] g) {
        int m = g.length;
        int[] matchR = new int[m];
        Arrays.fill(matchR, -1);
        int cnt = 0;
        for (int u = 0; u < m; u++) {
            boolean[] seen = new boolean[m];
            if (dfs(u, g, matchR, seen)) {
                cnt++;
            }
        }
        return cnt;
    }

    // 从我方 u 出发找增广路
    static boolean dfs(int u, int[][] g, int[] matchR, boolean[] seen) {
        int m = g.length;
        for (int v = 0; v < m; v++) {
            if (g[u][v] == 1 && !seen[v]) {
                seen[v] = true;
                if (matchR[v] == -1 || dfs(matchR[v], g, matchR, seen)) {
                    matchR[v] = u;
                    return true;
                }
            }
        }
        return false;
    }

    static int bestScore(int[][] g) {
        int m = g.length;
        return 2 * maxMatching(g) - m;
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int q = sc.nextInt();
        for (int t = 0; t < q; t++) {
            int m = sc.nextInt();
            int[][] g = new int[m][m];
            for (int i = 0; i < m; i++) {
                for (int j = 0; j < m; j++) {
                    g[i][j] = sc.nextInt();
                }
            }
            System.out.println(bestScore(g));
        }
        sc.close();
    }
}
