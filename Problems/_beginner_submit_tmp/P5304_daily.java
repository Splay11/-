import java.util.*;

public class Solution {
    public int maxDropoffReach(int n, int[][] links, int[] width) {
        if (n <= 0) return 0;
        List<Integer>[] g = new ArrayList[n];
        for (int i = 0; i < n; i++) g[i] = new ArrayList<>();
        for (int[] e : links) {
            g[e[0]].add(e[1]);
            g[e[1]].add(e[0]);
        }
        List<Integer>[] ch = new ArrayList[n];
        for (int i = 0; i < n; i++) ch[i] = new ArrayList<>();
        int[] parent = new int[n];
        Arrays.fill(parent, -1);
        Deque<Integer> q = new ArrayDeque<>();
        q.add(0); parent[0] = -2;
        while (!q.isEmpty()) {
            int u = q.poll();
            for (int v : g[u]) if (parent[v] == -1) {
                parent[v] = u; ch[u].add(v); q.add(v);
            }
        }
        boolean[][] vis = new boolean[n][2];
        boolean[] seen = new boolean[n];
        Deque<int[]> st = new ArrayDeque<>();
        st.push(new int[]{0, 0});
        vis[0][0] = true;
        while (!st.isEmpty()) {
            int[] cur = st.pop();
            int u = cur[0], used = cur[1];
            seen[u] = true;
            for (int v : ch[u]) {
                int nu;
                if (width[u] > width[v]) nu = used;
                else if (used == 0) nu = 1;
                else continue;
                if (!vis[v][nu]) {
                    vis[v][nu] = true;
                    st.push(new int[]{v, nu});
                }
            }
        }
        int ans = 0;
        for (boolean b : seen) if (b) ans++;
        return ans;
    }
}
