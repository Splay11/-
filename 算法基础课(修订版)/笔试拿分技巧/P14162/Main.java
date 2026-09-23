import java.util.*;

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int n = sc.nextInt(); // 输入博览会的数量n
        int k = sc.nextInt(); // 每次可以参加的博览会数量k
        
        int[][] a = new int[n][2]; // 用于存储博览会的开始和结束时间
        for (int i = 0; i < n; i++) {
            a[i][0] = sc.nextInt(); // 读取开始时间
            a[i][1] = sc.nextInt(); // 读取结束时间
        }

        // 根据开始时间排序
        Arrays.sort(a, (x, y) -> Integer.compare(x[0], y[0]));

        int start = 0; // 当前时间
        PriorityQueue<Integer> queue = new PriorityQueue<>(); // 最小堆用于存储结束时间
        int idx = 0; // 当前处理的博览会索引
        int ans = 0; // 参加的博览会数量

        while (idx < n || !queue.isEmpty()) {
            // 移除已结束的博览会
            while (!queue.isEmpty() && queue.peek() < start) {
                queue.poll();
            }

            // 添加当前可以参加的博览会
            while (idx < n && a[idx][0] <= start) {
                queue.add(a[idx][1]); // 将结束时间加入优先队列
                idx++;
            }

            // 如果没有可参加的博览会，更新开始时间
            if (queue.isEmpty()) {
                if (idx == n) {
                    break;
                }
                start = Math.max(start, a[idx][0]);
            }
             while (idx < n && a[idx][0] <= start) {
                queue.add(a[idx][1]); // 将结束时间加入优先队列
                idx++;
            }

            // 参加博览会
            for (int i = 0; i < k; i++) {
                if (!queue.isEmpty()) {
                    ans++; // 参加博览会
                    queue.poll(); // 弹出结束时间
                }
            }

            start++; // 增加当前时间
        }

        System.out.println(ans); // 输出参加的博览会数量
    }
}
