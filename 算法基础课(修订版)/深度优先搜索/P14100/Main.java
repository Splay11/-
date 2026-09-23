import java.util.ArrayList;
import java.util.Scanner;

public class Main {
    static final int MAX = 1001; // 假设最大节点数为 1000
    static ArrayList<Integer>[] adj = new ArrayList[MAX]; // 邻接表存储图
    static boolean[] visited = new boolean[MAX]; // 访问标记数组

    // DFS 函数
    public static void dfs(int node) {
        visited[node] = true; // 标记当前节点为已访问
        for (int neighbor : adj[node]) { // 遍历该节点的邻居
            if (!visited[neighbor]) { // 如果邻居未被访问
                dfs(neighbor); // 递归访问邻居节点
            }
        }
    }

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        int n = scanner.nextInt(); // 读取节点数
        int m = scanner.nextInt(); // 读取边数

        // 初始化邻接表
        for (int i = 1; i <= n; i++) {
            adj[i] = new ArrayList<>();
            visited[i] = false; // 初始化访问标记数组
        }

        // 读取边并构建邻接表
        for (int i = 0; i < m; i++) {
            int u = scanner.nextInt();
            int v = scanner.nextInt();
            if (u != v) { // 忽略自环
                adj[u].add(v);
                adj[v].add(u);
            }
        }

        // 统计连通块数量
        int count = 0;
        for (int i = 1; i <= n; i++) {
            if (!visited[i]) {
                dfs(i); // 启动 DFS
                count++; // 每次启动 DFS，发现一个新的连通块
            }
        }

        System.out.println(count); // 输出连通块数量
        scanner.close();
    }
}
