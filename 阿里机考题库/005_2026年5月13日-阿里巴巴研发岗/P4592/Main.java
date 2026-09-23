import java.io.*;
import java.util.*;

/**
 * 特权节点路径 — 到达特权节点后所有边免费
 * 算法：
 * 1. Dijkstra 从起点(0)求最短代价
 * 2. 反向 BFS 从终点(n-1)标记能到达终点的节点
 * 3. 枚举特权节点取最小 dist[p]
 * 复杂度：O((n+m) log n)
 */
public class Main {
    static final long INF = (long) 1e18;

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StringTokenizer st = new StringTokenizer(br.readLine());
        int n = Integer.parseInt(st.nextToken());  // 节点数
        int m = Integer.parseInt(st.nextToken());  // 边数
        int k = Integer.parseInt(st.nextToken());  // 特权节点数

        // 读入特权节点
        boolean[] lucky = new boolean[n];
        int[] luckyNodes = new int[k];
        for (int i = 0; i < k; i++) {
            int r = Integer.parseInt(br.readLine()) - 1;  // 转为 0-based
            lucky[r] = true;
            luckyNodes[i] = r;
        }

        // 建图：正向图 + 反向图
        List<int[]>[] g = new ArrayList[n];    // 正向 (v, w)
        List<Integer>[] rg = new ArrayList[n]; // 反向（仅存节点）
        for (int i = 0; i < n; i++) {
            g[i] = new ArrayList<>();
            rg[i] = new ArrayList<>();
        }

        for (int i = 0; i < m; i++) {
            st = new StringTokenizer(br.readLine());
            int u = Integer.parseInt(st.nextToken()) - 1;  // 起点（0-based）
            int v = Integer.parseInt(st.nextToken()) - 1;  // 终点（0-based）
            int w = Integer.parseInt(st.nextToken());       // 安全等级
            g[u].add(new int[]{v, w});
            rg[v].add(u);  // 反向边
        }

        // ---- 第一步：Dijkstra ----
        long[] dist = new long[n];
        Arrays.fill(dist, INF);
        dist[0] = 0;  // 起点为节点 1（下标 0）
        PriorityQueue<long[]> pq = new PriorityQueue<>(
            (a, b) -> Long.compare(a[0], b[0]));
        pq.offer(new long[]{0, 0});

        while (!pq.isEmpty()) {
            long[] top = pq.poll();
            long d = top[0];
            int u = (int) top[1];
            if (d != dist[u]) continue;  // 过期状态，跳过
            for (int[] e : g[u]) {
                int v = e[0], w = e[1];
                long nd = d + w;
                if (nd < dist[v]) {
                    dist[v] = nd;
                    pq.offer(new long[]{nd, v});
                }
            }
        }

        // ---- 第二步：反向 BFS ----
        boolean[] canReach = new boolean[n];
        canReach[n - 1] = true;  // 终点自身可达
        ArrayDeque<Integer> q = new ArrayDeque<>();
        q.offer(n - 1);
        while (!q.isEmpty()) {
            int u = q.poll();
            for (int v : rg[u]) {  // 沿反向边走
                if (!canReach[v]) {
                    canReach[v] = true;
                    q.offer(v);
                }
            }
        }

        // ---- 第三步：枚举特权节点取最小值 ----
        long ans = INF;
        for (int p : luckyNodes) {
            if (canReach[p] && dist[p] < ans) {
                ans = dist[p];
            }
        }

        System.out.println(ans >= INF ? -1 : ans);
    }
}
