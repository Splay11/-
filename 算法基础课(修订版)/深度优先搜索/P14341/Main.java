import java.util.*;

public class Main {
    static Long totalAdd = 0L;

    static Long dfs(int node, int father, List<Integer>[] adj, Long[] a) {
        Long totalSum = 0L;

        // 处理所有子节点
        for (int child : adj[node]) {
            if (child != father) {
                totalSum += dfs(child, node, adj, a);
            }
        }

        // 确保当前节点的权值大于等于所有子节点的权值和
        if (a[node] < totalSum) {
            totalAdd += totalSum - a[node];  // 更新全局的totalAdd
            a[node] = totalSum;  // 更新当前节点的权值
        }

        return a[node];
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int n = sc.nextInt();  // 节点数
        Long[] a = new Long[n];
        for (int i = 0; i < n; i++) {
            a[i] = sc.nextLong();  // 权值数组
        }

        int[][] edges = new int[n - 1][2];
        for (int i = 0; i < n - 1; i++) {
            edges[i][0] = sc.nextInt();
            edges[i][1] = sc.nextInt();
        }

        List<Integer>[] adj = new ArrayList[n];
        for (int i = 0; i < n; i++) {
            adj[i] = new ArrayList<>();
        }

        // 构建树的邻接表
        for (int[] edge : edges) {
            adj[edge[0] - 1].add(edge[1] - 1);
            adj[edge[1] - 1].add(edge[0] - 1);
        }

        // 从根节点0开始DFS
        dfs(0, -1, adj, a);

        System.out.println(totalAdd);  // 输出最终的totalAdd
    }
}
