import java.io.*;
import java.util.*;

public class Main {
    static int n, m;
    static boolean[][] isSpecial;
    static List<int[][]> allPositions = new ArrayList<>();
    static Set<String> finalStates = new HashSet<>();

    static String stateToKey(boolean[][] state) {
        StringBuilder sb = new StringBuilder(n * m);
        for (int i = 0; i < n; ++i) {
            for (int j = 0; j < m; ++j) {
                sb.append(state[i][j] ? '1' : '0');
            }
        }
        return sb.toString();
    }

    static boolean canPlaceBlock(boolean[][] state, int[][] pos) {
        // 检查占用（边界由预生成保证）
        for (int k = 0; k < 3; ++k) {
            int r = pos[k][0], c = pos[k][1];
            if (state[r][c]) return false;
        }
        // 至少一个端点与特殊格子重合
        int r1 = pos[0][0], c1 = pos[0][1];
        int r3 = pos[2][0], c3 = pos[2][1];
        boolean hasSpecialEndpoint = isSpecial[r1][c1] || isSpecial[r3][c3];
        return hasSpecialEndpoint;
    }

    static boolean[][] placeBlock(boolean[][] state, int[][] pos) {
        boolean[][] ns = new boolean[n][m];
        for (int i = 0; i < n; ++i) {
            System.arraycopy(state[i], 0, ns[i], 0, m);
        }
        for (int k = 0; k < 3; ++k) {
            int r = pos[k][0], c = pos[k][1];
            ns[r][c] = true;
        }
        return ns;
    }

    static void dfs(boolean[][] state) {
        boolean canPlaceAny = false;
        for (int[][] pos : allPositions) {
            if (canPlaceBlock(state, pos)) {
                canPlaceAny = true;
                boolean[][] ns = placeBlock(state, pos);
                dfs(ns);
            }
        }
        if (!canPlaceAny) {
            finalStates.add(stateToKey(state));
        }
    }

    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StringTokenizer st = new StringTokenizer(br.readLine().trim());
        n = Integer.parseInt(st.nextToken());
        m = Integer.parseInt(st.nextToken());

        isSpecial = new boolean[n][m];
        for (int i = 0; i < n; ++i) {
            String row = br.readLine().trim();
            for (int j = 0; j < m; ++j) {
                if (row.charAt(j) == '*') isSpecial[i][j] = true;
            }
        }

        // 生成所有 1x3（横向）与 3x1（纵向）位置
        for (int i = 0; i < n; ++i) {
            for (int j = 0; j + 2 < m; ++j) {
                allPositions.add(new int[][] { {i, j}, {i, j + 1}, {i, j + 2} });
            }
        }
        for (int i = 0; i + 2 < n; ++i) {
            for (int j = 0; j < m; ++j) {
                allPositions.add(new int[][] { {i, j}, {i + 1, j}, {i + 2, j} });
            }
        }

        boolean[][] initialState = new boolean[n][m];
        dfs(initialState);

        System.out.println(finalStates.size());
    }
}
