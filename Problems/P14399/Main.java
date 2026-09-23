import java.util.ArrayList;
import java.util.HashMap;

public class Solution {
    public int maxZoneImbalance(int[] loads, int[][] edges) {
        int n = loads.length;
        if (edges.length == 0) return -1;
        int[] parent = new int[n];
        for (int i = 0; i < n; i++) parent[i] = i;

        for (int[] e : edges) union(parent, e[0], e[1]);

        HashMap<Integer, ArrayList<Integer>> groups = new HashMap<>();
        for (int i = 0; i < n; i++) {
            int r = find(parent, i);
            groups.computeIfAbsent(r, k -> new ArrayList<>()).add(i);
        }

        int ans = -1;
        for (ArrayList<Integer> nodes : groups.values()) {
            if (nodes.size() < 2) continue;
            int mn = loads[nodes.get(0)], mx = loads[nodes.get(0)];
            for (int id : nodes) {
                mn = Math.min(mn, loads[id]);
                mx = Math.max(mx, loads[id]);
            }
            ans = Math.max(ans, (mx - mn) * nodes.size());
        }
        return ans;
    }

    private int find(int[] parent, int x) {
        while (parent[x] != x) {
            parent[x] = parent[parent[x]];
            x = parent[x];
        }
        return x;
    }

    private void union(int[] parent, int a, int b) {
        a = find(parent, a);
        b = find(parent, b);
        if (a != b) parent[b] = a;
    }
}
