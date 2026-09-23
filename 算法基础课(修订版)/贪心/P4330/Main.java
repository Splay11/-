import java.io.*;
import java.util.*;

public class Main {
    public static void main(String[] args) throws IOException {
        // 使用 BufferedReader 加速 Java IO
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StringTokenizer st = new StringTokenizer(br.readLine());

        int n = Integer.parseInt(st.nextToken());
        int m = Integer.parseInt(st.nextToken());
        int x = Integer.parseInt(st.nextToken());

        long[] a = new long[n];
        st = new StringTokenizer(br.readLine());
        for (int i = 0; i < n; i++) {
            a[i] = Long.parseLong(st.nextToken());
        }

        // ordersDue[i] 存储最晚发货日期为第 i+1 天的订单数量
        int[] ordersDue = new int[n];
        st = new StringTokenizer(br.readLine());
        for (int i = 0; i < m; i++) {
            int b = Integer.parseInt(st.nextToken());
            // 转换为 0-based 索引
            ordersDue[b - 1]++;
        }

        // 最小优先队列（小顶堆），存储可用的发货槽位 {价格, 数量}
        // 按数组的第一个元素（价格）升序排序
        PriorityQueue<long[]> pq = new PriorityQueue<>(Comparator.comparingLong(arr -> arr[0]));

        long totalCost = 0;

        // 从第 1 天到第 n 天遍历
        for (int i = 0; i < n; i++) {
            // 将当天的发货槽位加入优先队列
            pq.offer(new long[]{a[i], x});

            // 获取当天必须发货的订单数量
            int ordersToShip = ordersDue[i];

            // 为这些订单分配成本最低的槽位
            while (ordersToShip > 0) {
                // 取出当前最便宜的槽位信息
                long[] top = pq.poll();
                long cost = top[0];
                long count = top[1];

                // 决定使用多少个这种价格的槽位
                long numToUse = Math.min(ordersToShip, count);
                
                // 累加成本
                totalCost += numToUse * cost;

                // 更新剩余需要发货的订单数量
                ordersToShip -= numToUse;
                
                // 如果这种价格的槽位还有剩余，将其放回优先队列
                if (count > numToUse) {
                    pq.offer(new long[]{cost, count - numToUse});
                }
            }
        }
        
        System.out.println(totalCost);
    }
}
