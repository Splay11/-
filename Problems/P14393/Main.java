import java.util.ArrayDeque;
import java.util.ArrayList;

public class Solution {
    public int[] canIsolateWithTwoPools(int[] resourceCount, int[][][] conflicts) {
        int[] ans = new int[resourceCount.length];
        // 每组独立判定能否二分到两个资源池
        for (int i = 0; i < resourceCount.length; i++)
            ans[i] = bipartite(resourceCount[i], conflicts[i]) ? 1 : 0;
        return ans;
    }

    private boolean bipartite(int n, int[][] edges) {
        // 自环直接不可行
        for (int[] e : edges)
            if (e[0] == e[1]) return false;

        // 建无向图邻接表
        ArrayList<Integer>[] adj = new ArrayList[n + 1];
        for (int i = 1; i <= n; i++) adj[i] = new ArrayList<>();
        for (int[] e : edges) {
            adj[e[0]].add(e[1]);
            adj[e[1]].add(e[0]);
        }

        int[] color = new int[n + 1];
        for (int i = 0; i <= n; i++) color[i] = -1;

        for (int start = 1; start <= n; start++) {
            if (color[start] != -1 || adj[start].isEmpty()) continue;
            color[start] = 0;
            ArrayDeque<Integer> q = new ArrayDeque<>();
            q.add(start);
            while (!q.isEmpty()) {
                int u = q.poll();
                for (int v : adj[u]) {
                    if (color[v] == -1) {
                        // 相邻顶点染成异色
                        color[v] = 1 - color[u];
                        q.add(v);
                    } else if (color[v] == color[u]) {
                        // 发现同色相邻，存在奇环
                        return false;
                    }
                }
            }
        }
        return true;
    }
}
