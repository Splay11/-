import java.util.*;

public class Main {
    public static void main(String[] args) {
        // 读取输入数据
        Scanner scanner = new Scanner(System.in);
        int n = scanner.nextInt(); // 数组大小
        int q = scanner.nextInt(); // 查询次数

        // 输入升序数组
        int[] arr = new int[n];
        for (int i = 0; i < n; i++) {
            arr[i] = scanner.nextInt();
        }

        // 处理每个查询
        for (int i = 0; i < q; i++) {
            int target = scanner.nextInt(); // 目标值
            if (binarySearch(arr, target)) {
                System.out.println("YES");
            } else {
                System.out.println("NO");
            }
        }

        scanner.close();
    }
    // 二分查找函数：判断目标值是否存在于数组中
    public static boolean binarySearch(int[] arr, int target) {
        int left = 0, right = arr.length - 1;
    
        // 开始二分查找
        while (left <= right) {
            int mid = (left + right) / 2; // 中间位置
    
            if (arr[mid] == target) {
                return true; // 找到目标值
            } else if (arr[mid] < target) {
                left = mid + 1; // 目标值在右半部分
            } else {
                right = mid - 1; // 目标值在左半部分
            }
        }
    
        // 没有找到目标值
        return false;
    }
}
