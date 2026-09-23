import java.util.Scanner;

public class Main {
    // 找到第一个等于或大于目标值的位置
    public static int lowerBound(int[] arr, int x) {
        int left = 0, right = arr.length - 1;
        while (left <= right) {
            int mid = left + (right - left) / 2; // 避免整数溢出
            if (arr[mid] < x) { 
                left = mid + 1; // 目标值在右半部分
            } else { 
                right = mid - 1; // 目标值可能是当前值，或在左半部分
            }
        }
        return left; // 返回第一个大于等于 x 的位置
    }

    // 找到第一个大于目标值的位置
    public static int upperBound(int[] arr, int x) {
        int left = 0, right = arr.length - 1;
        while (left <= right) {
            int mid = left + (right - left) / 2; // 避免整数溢出
            if (arr[mid] <= x) { 
                left = mid + 1; // 目标值可能在当前值或右半部分
            } else { 
                right = mid - 1; // 目标值在左半部分
            }
        }
        return left; // 返回第一个大于 x 的位置
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        // 输入数组大小和查询次数
        int n = sc.nextInt(); // 数组大小
        int q = sc.nextInt(); // 查询次数

        // 输入数组
        int[] arr = new int[n];
        for (int i = 0; i < n; i++) {
            arr[i] = sc.nextInt();
        }

        // 多次查询
        while (q-- > 0) {
            int x = sc.nextInt(); // 查询的目标值

            // 使用 lowerBound 和 upperBound 找到范围
            int first = lowerBound(arr, x); // 第一次出现的位置
            int last = upperBound(arr, x) - 1; // 最后一次出现的位置

            // 判断目标值是否存在
            if (first < n && arr[first] == x) {
                // 如果存在，输出位置
                System.out.println((first + 1) + " " + (last + 1)); // 输出 1-based 索引
            } else {
                // 如果不存在，输出 -1 -1
                System.out.println("-1 -1");
            }
        }

        sc.close(); // 关闭输入流
    }
}
