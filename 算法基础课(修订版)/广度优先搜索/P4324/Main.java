// ACM 风格，类名 Main
// 思路：构建站点->线路倒排表，再把同站点上的线路两两连边；每次查询在“线路图”上做 BFS。
import java.io.*;
import java.util.*;

public class Main {

    // 计算一次查询的最少换乘
    static int bfsMinTransfers(int s, int t, List<Integer>[] stationLines, List<Integer>[] adj) {
        if (s == t) return 0;
        List<Integer> starts = stationLines[s];
        List<Integer> tlist = stationLines[t];
        if (starts.isEmpty() || tlist.isEmpty()) return -1;

        // 目标集合转为布尔标记，O(1) 判断
        int m = adj.length;
        boolean[] isTarget = new boolean[m];
        for (int x : tlist) isTarget[x] = true;

        // 同一条线路同时包含 s 与 t
        for (int x : starts) if (isTarget[x]) return 0;

        int[] dist = new int[m];
        Arrays.fill(dist, -1);
        ArrayDeque<Integer> q = new ArrayDeque<>();
        for (int x : starts) { dist[x] = 0; q.add(x); }

        while (!q.isEmpty()) {
            int u = q.poll();
            for (int v : adj[u]) {
                if (dist[v] == -1) {
                    dist[v] = dist[u] + 1;
                    if (isTarget[v]) return dist[v];
                    q.add(v);
                }
            }
        }
        return -1;
    }

    // 构建站点->线路、线路图
    static void buildGraph(int n, int m, List<Integer>[] lines,
                           List<Integer>[] stationLines, List<Integer>[] adj) {
        // 建立站点->线路
        for (int i = 0; i < m; i++) {
            for (int s : lines[i]) {
                stationLines[s].add(i);
            }
        }
        // 同站点上的线路两两连边
        for (int s = 0; s < n; s++) {
            List<Integer> lst = stationLines[s];
            int L = lst.size();
            for (int i = 0; i < L; i++) {
                int a = lst.get(i);
                for (int j = i + 1; j < L; j++) {
                    int b = lst.get(j);
                    adj[a].add(b);
                    adj[b].add(a);
                }
            }
        }
    }

    public static void main(String[] args) throws Exception {
        // 默认用 BufferedReader + StringTokenizer，数据范围小也足够
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StringTokenizer st = new StringTokenizer(br.readLine());
        int n = Integer.parseInt(st.nextToken());
        int m = Integer.parseInt(st.nextToken());
        int k = Integer.parseInt(st.nextToken());

        @SuppressWarnings("unchecked")
        List<Integer>[] lines = new ArrayList[m];
        for (int i = 0; i < m; i++) lines[i] = new ArrayList<>();

        for (int i = 0; i < m; i++) {
            st = new StringTokenizer(br.readLine());
            int cnt = Integer.parseInt(st.nextToken());
            for (int j = 0; j < cnt; j++) {
                lines[i].add(Integer.parseInt(st.nextToken()));
            }
        }

        @SuppressWarnings("unchecked")
        List<Integer>[] stationLines = new ArrayList[n];
        @SuppressWarnings("unchecked")
        List<Integer>[] adj = new ArrayList[m];
        for (int i = 0; i < n; i++) stationLines[i] = new ArrayList<>();
        for (int i = 0; i < m; i++) adj[i] = new ArrayList<>();

        buildGraph(n, m, lines, stationLines, adj);

        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < k; i++) {
            st = new StringTokenizer(br.readLine());
            int s = Integer.parseInt(st.nextToken());
            int t = Integer.parseInt(st.nextToken());
            sb.append(bfsMinTransfers(s, t, stationLines, adj)).append('\n');
        }
        System.out.print(sb.toString());
    }
}
