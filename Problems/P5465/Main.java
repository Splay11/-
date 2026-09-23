import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.Collections;
import java.util.PriorityQueue;
import java.util.StringTokenizer;

// 按质量排序后，把热度能互相罩住的稿件并到同一连通块；块内可任意重排
public class Main {
    static int[] parent;
    static int[] rankv;
    static int[] minH;

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        int q = Integer.parseInt(br.readLine().trim());
        StringBuilder out = new StringBuilder();
        for (int tc = 0; tc < q; tc++) {
            int m = Integer.parseInt(br.readLine().trim());
            int[] p = new int[m];
            int[] h = new int[m];
            StringTokenizer st = new StringTokenizer(br.readLine());
            for (int i = 0; i < m; i++) {
                p[i] = Integer.parseInt(st.nextToken());
                h[i] = Integer.parseInt(st.nextToken());
            }
            int[] t = new int[m];
            st = new StringTokenizer(br.readLine());
            for (int i = 0; i < m; i++) {
                t[i] = Integer.parseInt(st.nextToken());
            }
            out.append(canMatch(p, h, t) ? "YES" : "NO").append('\n');
        }
        System.out.print(out.toString());
    }

    static int find(int x) {
        while (parent[x] != x) {
            parent[x] = parent[parent[x]];
            x = parent[x];
        }
        return x;
    }

    static void union(int x, int y) {
        x = find(x);
        y = find(y);
        if (x == y) {
            return;
        }
        if (rankv[x] < rankv[y]) {
            int tmp = x;
            x = y;
            y = tmp;
        }
        parent[y] = x;
        if (minH[y] < minH[x]) {
            minH[x] = minH[y];
        }
        if (rankv[x] == rankv[y]) {
            rankv[x]++;
        }
    }

    static boolean canMatch(int[] p, int[] h, int[] t) {
        int m = p.length;
        parent = new int[m];
        rankv = new int[m];
        minH = new int[m];
        Integer[] order = new Integer[m];
        for (int i = 0; i < m; i++) {
            parent[i] = i;
            minH[i] = h[i];
            order[i] = i;
        }
        // 质量升序，质量相同则热度升序
        java.util.Arrays.sort(order, new java.util.Comparator<Integer>() {
            public int compare(Integer i, Integer j) {
                if (p[i] != p[j]) {
                    return p[i] < p[j] ? -1 : 1;
                }
                if (h[i] != h[j]) {
                    return h[i] < h[j] ? -1 : 1;
                }
                return 0;
            }
        });
        PriorityQueue<int[]> heap = new PriorityQueue<int[]>(new java.util.Comparator<int[]>() {
            public int compare(int[] a, int[] b) {
                if (a[0] != b[0]) {
                    return a[0] < b[0] ? -1 : 1;
                }
                return 0;
            }
        });
        for (int k = 0; k < m; k++) {
            int i = order[k];
            while (!heap.isEmpty() && heap.peek()[0] <= h[i]) {
                int[] cur = heap.poll();
                int x = find(cur[1]);
                if (minH[x] != cur[0]) {
                    continue;
                }
                union(i, x);
            }
            int r = find(i);
            heap.add(new int[] {minH[r], r});
        }
        ArrayList<ArrayList<Integer>> have = new ArrayList<ArrayList<Integer>>();
        ArrayList<ArrayList<Integer>> need = new ArrayList<ArrayList<Integer>>();
        for (int i = 0; i < m; i++) {
            have.add(new ArrayList<Integer>());
            need.add(new ArrayList<Integer>());
        }
        for (int i = 0; i < m; i++) {
            int r = find(i);
            have.get(r).add(h[i]);
            need.get(r).add(t[i]);
        }
        for (int r = 0; r < m; r++) {
            if (have.get(r).isEmpty()) {
                continue;
            }
            Collections.sort(have.get(r));
            Collections.sort(need.get(r));
            if (!have.get(r).equals(need.get(r))) {
                return false;
            }
        }
        return true;
    }
}
