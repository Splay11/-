import java.util.*;

public class Main {

    // 计算最少硬币数的函数
    public static int minCoins(int[] coins, int amount) {
        // 将硬币按面额从大到小排序
        Arrays.sort(coins);
        int coinCount = 0;

        // 遍历硬币，尝试从大到小使用硬币
        for (int i = coins.length - 1; i >= 0; i--) {
            if (amount == 0) {
                break;
            }
            // 使用尽可能多的当前硬币
            coinCount += amount / coins[i];
            amount %= coins[i];  // 更新剩余金额
        }

        // 如果amount变为0，说明找到了最小硬币数
        if (amount == 0) {
            return coinCount;
        } else {
            return -1;  // 如果无法组合成目标金额，返回-1
        }
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        
        int n = sc.nextInt();  // 输入硬币数量
        int[] coins = new int[n];
        
        for (int i = 0; i < n; i++) {
            coins[i] = sc.nextInt();  // 输入硬币面额
        }
        
        int amount = sc.nextInt();  // 输入目标金额

        // 输出最少硬币数
        System.out.println(minCoins(coins, amount));

        sc.close();
    }
}
