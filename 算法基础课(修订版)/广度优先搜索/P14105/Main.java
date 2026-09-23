import java.util.*;

public class Main {

    // 定义广度优先搜索的方法
    private static void bfs(int start, List<List<Integer>> adj, boolean[] visited) {
        Queue<Integer> queue = new LinkedList<>();
        queue.offer(start);
        visited[start] = true;

        while (!queue.isEmpty()) {
            int node = queue.poll();

            // 遍历所有相邻节点
            for (int neighbor : adj.get(node)) {
                if (!visited[neighbor]) {
                    visited[neighbor] = true;
                    queue.offer(neighbor);
                }
            }
        }
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        // 读取节点数和边数
        int n = sc.nextInt();
        int m = sc.nextInt();

        // 邻接表存储图
        List<List<Integer>> adj = new ArrayList<>(n + 1);
        for (int i = 0; i <= n; i++) {
            adj.add(new ArrayList<>());
        }

        // 读取图的边
        for (int i = 0; i < m; i++) {
            int u = sc.nextInt();
            int v = sc.nextInt();
            adj.get(u).add(v);
            adj.get(v).add(u);  // 无向图双向连接
        }

        // 访问标记数组
        boolean[] visited = new boolean[n + 1];
        int connectedComponents = 0;

        // 对每个节点进行 BFS 遍历
        for (int i = 1; i <= n; i++) {
            if (!visited[i]) {
                bfs(i, adj, visited);
                connectedComponents++;  // 每找到一个连通块，计数加1
            }
        }

        // 输出连通块的数量
        System.out.println(connectedComponents);
        sc.close();
    }
}
