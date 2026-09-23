import java.util.*;

public class Main {
    static char[] colors;
    static List<Integer>[] adj;
    static int result = 0;

    // DFS遍历树并判断子树的红黑节点
    static boolean[] dfs(int node, int parent) {
        // 标记当前子树是否包含红色和黑色
        boolean hasRed = false, hasBlack = false;
        if (colors[node] == 'R') hasRed = true;
        else hasBlack = true;

        for (int neighbor : adj[node]) {
            if (neighbor != parent) {
                boolean[] child = dfs(neighbor, node);

                if(child[0]){
                    hasRed = true;
                }
                if(child[1]){
                    hasBlack = true;
                }
            }
        }
        // 如果当前子树既有红色又有黑色节点，则满足条件
        if (hasRed && hasBlack) {
            result++;
        }

        return new boolean[]{hasRed, hasBlack};
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int n = sc.nextInt();
        colors = sc.next().toCharArray();
        adj = new ArrayList[n];
        for (int i = 0; i < n; i++) {
            adj[i] = new ArrayList<>();
        }

        for (int i = 0; i < n - 1; i++) {
            int u = sc.nextInt() - 1;
            int v = sc.nextInt() - 1;
            adj[u].add(v);
            adj[v].add(u);
        }

        dfs(0, -1);
        System.out.println(result);
        sc.close();
    }
}
