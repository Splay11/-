import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.StringTokenizer;

public class Main {
    static final int[] DI = {1, -1, 0, 0};
    static final int[] DJ = {0, 0, 1, -1};

    // 统计 grid2 里有多少座岛，整座岛的格子在 grid1 里也都是陆地
    // 用栈做 DFS，m、n 到 500，蛇形岛递归会爆
    static int solve(int[][] grid1, int[][] grid2) {
        int m = grid2.length;
        int n = grid2[0].length;
        // 复制一份再染色，避免改到原矩阵
        int[][] g2 = new int[m][n];
        for (int i = 0; i < m; i++) {
            for (int j = 0; j < n; j++) {
                g2[i][j] = grid2[i][j];
            }
        }
        int ans = 0;
        List<int[]> stack = new ArrayList<>();
        for (int i = 0; i < m; i++) {
            for (int j = 0; j < n; j++) {
                if (g2[i][j] != 1) {
                    continue;
                }
                // 从当前格出发走完这座 grid2 岛
                boolean ok = true;
                stack.clear();
                stack.add(new int[] {i, j});
                g2[i][j] = 0;
                while (!stack.isEmpty()) {
                    int[] cur = stack.remove(stack.size() - 1);
                    int x = cur[0];
                    int y = cur[1];
                    if (grid1[x][y] == 0) {
                        // 这座岛有一块在 grid1 里是水，就不能算子岛屿
                        ok = false;
                    }
                    for (int k = 0; k < 4; k++) {
                        int ni = x + DI[k];
                        int nj = y + DJ[k];
                        if (ni >= 0 && ni < m && nj >= 0 && nj < n && g2[ni][nj] == 1) {
                            g2[ni][nj] = 0;
                            stack.add(new int[] {ni, nj});
                        }
                    }
                }
                if (ok) {
                    ans++;
                }
            }
        }
        return ans;
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StringTokenizer st = new StringTokenizer(br.readLine());
        int m = Integer.parseInt(st.nextToken());
        int n = Integer.parseInt(st.nextToken());
        int[][] grid1 = new int[m][n];
        int[][] grid2 = new int[m][n];
        for (int i = 0; i < m; i++) {
            st = new StringTokenizer(br.readLine());
            for (int j = 0; j < n; j++) {
                grid1[i][j] = Integer.parseInt(st.nextToken());
            }
        }
        for (int i = 0; i < m; i++) {
            st = new StringTokenizer(br.readLine());
            for (int j = 0; j < n; j++) {
                grid2[i][j] = Integer.parseInt(st.nextToken());
            }
        }
        System.out.println(solve(grid1, grid2));
    }
}
