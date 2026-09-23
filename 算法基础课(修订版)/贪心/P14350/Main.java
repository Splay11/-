import java.util.Scanner;

public class Main {

    public static int minGroups(int n, int k, int[] a) {
        // 初始化分组数和当前组的最大最小值
        int groupCount = 1;
        int minVal = a[0];
        int maxVal = a[0];

        // 从第二个物品开始遍历
        for (int i = 1; i < n; i++) {
            // 如果当前物品加入组后，最大值和最小值之差超过k，则需要分新的一组
            if (a[i] - minVal > k || maxVal - a[i] > k) {
                groupCount++;
                minVal = a[i];  // 新组的最小值
                maxVal = a[i];  // 新组的最大值
            } else {
                // 更新当前组的最大值和最小值
                minVal = Math.min(minVal, a[i]);
                maxVal = Math.max(maxVal, a[i]);
            }
        }

        return groupCount;
    }

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        // 输入处理
        int n = scanner.nextInt();
        int k = scanner.nextInt();
        int[] a = new int[n];
        for (int i = 0; i < n; i++) {
            a[i] = scanner.nextInt();
        }

        // 输出结果
        System.out.println(minGroups(n, k, a));
    }
}
