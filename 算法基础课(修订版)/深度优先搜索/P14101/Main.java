import java.util.*;

public class Main {
    static Map<Integer, List<Integer>> graph = new HashMap<>(); // 邻接表

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        // 读取节点数和边数
        int n = scanner.nextInt(); // 节点数
        int m = scanner.nextInt(); // 边数

        // 初始化邻接表
        for (int i = 1; i <= n; i++) {
            graph.put(i, new ArrayList<>());
        }

        // 读取边的信息并构建邻接表
        for (int i = 0; i < m; i++) {
            int u = scanner.nextInt();
            int v = scanner.nextInt();
            graph.get(u).add(v); // 添加有向边 u -> v
        }

        // 读取起点 s 和终点 t
        int s = scanner.nextInt();
        int t = scanner.nextInt();

        // 调用 DFS 计算路径数量
        int result = dfs(s, t);
        System.out.println(result);

        scanner.close();
    }

    public static int dfs(int u, int t) {
        // 如果到达终点 t，说明找到了一条路径
        if (u == t) {
            return 1;
        }

        int res = 0; // 初始化路径数量

        // 遍历所有邻接节点并递归计算
        if (graph.containsKey(u)) {
            for (int v : graph.get(u)) {
                res += dfs(v, t);
            }
        }

        return res;
    }
}
