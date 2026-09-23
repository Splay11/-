import java.util.Scanner;

public class Main {

    // 手写二分查找，返回第一个大于等于 target 的位置
    public static int lowerBound(int[] arr, int target) {
        int left = 0, right = arr.length;
        while (left < right) {
            int mid = left + (right - left) / 2;
            if (arr[mid] >= target) {
                right = mid; // target 或者比 target 小的元素应该在左边
            } else {
                left = mid + 1; // target 应该在右边
            }
        }
        return left; // 返回第一个大于等于 target 的位置
    }

    // 手写二分查找，返回第一个大于 target 的位置
    public static int upperBound(int[] arr, int target) {
        int left = 0, right = arr.length;
        while (left < right) {
            int mid = left + (right - left) / 2;
            if (arr[mid] > target) {
                right = mid; // target 需要在左边
            } else {
                left = mid + 1; // target 或者比 target 小的元素需要在右边
            }
        }
        return left; // 返回第一个大于 target 的位置
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        // 输入 n 和 Q
        int n = sc.nextInt();
        int Q = sc.nextInt();

        // 输入升序排列的数组 arr
        int[] arr = new int[n];
        for (int i = 0; i < n; i++) {
            arr[i] = sc.nextInt();
        }

        // 处理 Q 个查询
        while (Q-- > 0) {
            int target = sc.nextInt();

            // 查找比 target 小的最大值（前驱）
            int pos_max = lowerBound(arr, target) - 1;  // 找到比 target 小的最大元素的位置
            int max_val = (pos_max >= 0) ? arr[pos_max] : -1; // 若存在前驱，则返回，否则返回 -1

            // 查找比 target 大的最小值（后继）
            int pos_min = upperBound(arr, target);  // 找到第一个比 target 大的元素的位置
            int min_val = (pos_min < arr.length) ? arr[pos_min] : -1; // 若存在后继，则返回，否则返回 -1

            // 输出结果
            System.out.println(max_val + " " + min_val);
        }

        sc.close();
    }
}
