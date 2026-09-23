import java.util.*;

public class Main {

    // 定义一个商品类
    static class Item {
        int weight;
        int value;
        double ratio;

        public Item(int weight, int value) {
            this.weight = weight;
            this.value = value;
            this.ratio = (double) value / weight;  // 计算单位重量的价值
        }
    }

    // 计算分数背包问题的最大价值
    public static double fractionalKnapsack(int n, int C, List<Item> items) {
        // 按照单位重量价值从大到小排序
        items.sort((a, b) -> Double.compare(b.ratio, a.ratio));

        double totalValue = 0.0;
        int remainingCapacity = C;

        // 遍历所有商品，选择不超过背包容量的部分商品
        for (Item item : items) {
            if (remainingCapacity == 0) {
                break;  // 背包已满
            }
            if (item.weight <= remainingCapacity) {  // 商品能完全放入背包
                totalValue += item.value;
                remainingCapacity -= item.weight;
            } else {  // 只能放入部分商品
                totalValue += item.value * ((double) remainingCapacity / item.weight);
                remainingCapacity = 0;  // 背包满了
            }
        }

        return totalValue;
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        // 读取商品数量n和背包最大承重C
        int n = sc.nextInt();
        int C = sc.nextInt();

        List<Item> items = new ArrayList<>();

        // 读取每个商品的重量和价值
        for (int i = 0; i < n; i++) {
            int weight = sc.nextInt();
            int value = sc.nextInt();
            items.add(new Item(weight, value));
        }

        // 计算最大总价值，并输出结果，保留两位小数
        double result = fractionalKnapsack(n, C, items);
        System.out.printf("%.2f\n", result);

        sc.close();
    }
}
