import java.util.*;

public class Main {

    static List<List<Integer>> adjList;
    static List<Integer> traversalResult;

    public static void dfs(int node, int parent) {
        traversalResult.add(node); // 访问当前节点
        for (int child : adjList.get(node)) {
            if (child != parent) { // 避免回到父节点
                dfs(child, node); // 递归访问子节点
            }
        }
    }

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        // 读取节点数
        int n = scanner.nextInt();
        // 读取表示方式
        int treeType = scanner.nextInt();

        adjList = new ArrayList<>();
        traversalResult = new ArrayList<>();

        for (int i = 0; i <= n; i++) {
            adjList.add(new ArrayList<>());
        }

        if (treeType == 1) {
            // 方式一：通过边的形式输入
            for (int i = 0; i < n - 1; i++) {
                int u = scanner.nextInt();
                int v = scanner.nextInt();
                adjList.get(u).add(v); // 添加子节点
                adjList.get(v).add(u); // 添加父节点（无向树）
            }
        } else if (treeType == 2) {
            // 方式二：通过father数组输入
            int[] father = new int[n];
            for (int i = 0; i < n; i++) {
                father[i] = scanner.nextInt();
            }
            for (int i = 1; i <= n; i++) {
                if (father[i - 1] != 0) {
                    adjList.get(father[i - 1]).add(i); // 添加子节点
                    //adjList.get(i).add(father[i - 1]); // 添加父节点
                }
            }
        }

        // 为了保证遍历顺序的一致性，先对每个节点的子节点进行排序
        for (int i = 1; i <= n; i++) {
            Collections.sort(adjList.get(i));
        }

        // 执行dfs，根节点为1，父节点为0（无）
        dfs(1, 0);

        // 输出遍历结果
        for (int i = 0; i < traversalResult.size(); i++) {
            System.out.print(traversalResult.get(i));
            if (i < traversalResult.size() - 1) {
                System.out.print(" ");
            }
        }
        System.out.println();
    }
}
