import java.util.*;

public class Main {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        int n = scanner.nextInt();
        int k = scanner.nextInt();
        int m = scanner.nextInt();

        int[] x = new int[k];
        for (int i = 0; i < k; i++) {
            x[i] = scanner.nextInt();
        }

        int[] y = new int[m];
        for (int i = 0; i < m; i++) {
            y[i] = scanner.nextInt();
        }

        // 最短路径数组
        int[] dist = new int[n];
        Arrays.fill(dist, -1);
        dist[0] = 0;  // 初始位置为 0，0 需要 0 次操作

        // BFS 队列
        Queue<Integer> q = new LinkedList<>();
        q.add(0);  // 从偏移量 0 开始

        while (!q.isEmpty()) {
            int curr = q.poll();

            for (int xi : x) {
                int nextOffset = (curr + xi) % n;  // 新的偏移量
                if (dist[nextOffset] == -1) {  // 如果这个偏移量没有被访问过
                    dist[nextOffset] = dist[curr] + 1;
                    q.add(nextOffset);
                }
            }
        }

        // 输出每个查询的结果
        for (int target : y) {
            System.out.println(dist[target]);
        }

        scanner.close();
    }
}
