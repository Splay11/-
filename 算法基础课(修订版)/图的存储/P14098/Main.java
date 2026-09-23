import java.util.*;

public class GraphComparison {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        int n = scanner.nextInt();

        // 初始化和读取邻接矩阵
        int[][] matrix = new int[n + 1][n + 1];
        for (int i = 1; i <= n; i++) {
            for (int j = 1; j <= n; j++) {
                matrix[i][j] = scanner.nextInt();
            }
        }

        // 转换为邻接表
        List<List<Integer>> adjFromMatrix = new ArrayList<>();
        for (int i = 0; i <= n; i++) {
            adjFromMatrix.add(new ArrayList<>());
        }

        for (int i = 1; i <= n; i++) {
            for (int j = 1; j <= n; j++) {
                if (matrix[i][j] == 1) {
                    adjFromMatrix.get(i).add(j);
                }
            }
        }

        // 读取并初始化邻接表
        List<List<Integer>> adjList = new ArrayList<>();
        for (int i = 0; i <= n; i++) {
            adjList.add(new ArrayList<>());
        }

        for (int i = 1; i <= n; i++) {
            int node = scanner.nextInt();
            int k = scanner.nextInt();
            for (int j = 0; j < k; j++) {
                int neighbor = scanner.nextInt();
                adjList.get(node).add(neighbor);
            }
        }

        // 排序邻接表，以便比较
        for (int i = 1; i <= n; i++) {
            Collections.sort(adjFromMatrix.get(i));
            Collections.sort(adjList.get(i));
        }

        // 比较两张图的邻接表是否一致
        boolean identical = true;
        for (int i = 1; i <= n; i++) {
            if (!adjFromMatrix.get(i).equals(adjList.get(i))) {
                identical = false;
                break;
            }
        }

        System.out.println(identical ? "YES" : "NO");
    }
}
