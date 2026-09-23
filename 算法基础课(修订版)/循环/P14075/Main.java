import java.util.ArrayList;
import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        // 读入数组大小
        int n = scanner.nextInt();

        // 定义数组
        int[] arr = new int[n];
        for (int i = 0; i < n; i++) {
            arr[i] = scanner.nextInt(); // 读入数组元素
        }

        // 初始化最大值为数组的第一个元素
        int maxValue = arr[0];

        // 第一个循环：找出数组中的最大值
        for (int i = 0; i < n; i++) {
            maxValue = Math.max(maxValue, arr[i]); // 比较当前最大值和当前元素
        }

        // 创建列表存储最大值的下标
        ArrayList<Integer> indices = new ArrayList<>();

        // 第二个循环：找出所有等于最大值的下标
        for (int i = 0; i < n; i++) {
            boolean isMax = (arr[i] == maxValue ? true : false); // 判断当前元素是否等于最大值
            if (isMax) {
                indices.add(i); // 如果是最大值，记录下标
            }
        }

        // 输出最大值
        System.out.println(maxValue);

        // 输出所有最大值的下标，确保最后一个下标后不加空格
        for (int i = 0; i < indices.size(); i++) {
            System.out.print(indices.get(i) + (i == indices.size() - 1 ? "" : " "));
        }
        System.out.println(); // 输出换行符

        scanner.close(); // 关闭扫描器
    }
}
