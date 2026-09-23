import java.util.Scanner;

public class Main {

    // 计算最大利润的函数
    public static int maxProfit(int[] prices) {
        int maxProfit = 0;

        // 遍历价格数组，从第二天开始与前一天进行比较
        for (int i = 1; i < prices.length; i++) {
            // 如果今天的价格比昨天高，则可以获得利润
            if (prices[i] > prices[i - 1]) {
                // 累加利润
                maxProfit += prices[i] - prices[i - 1];
            }
        }

        return maxProfit;
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        // 获取数组长度
        int n = sc.nextInt();
        
        // 获取价格数组
        int[] prices = new int[n];
        for (int i = 0; i < n; i++) {
            prices[i] = sc.nextInt();
        }

        // 输出最大利润
        System.out.println(maxProfit(prices));

        sc.close();
    }
}
