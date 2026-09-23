import java.util.Scanner;

public class Main {
    public static int[] findTwoSum(int[] nums, int target) {
        int left = 0;
        int right = nums.length - 1;

        while (left < right) {
            int sum = nums[left] + nums[right];

            if (sum == target) {
                // 返回1-based索引
                return new int[]{left + 1, right + 1};
            } else if (sum < target) {
                left++;  // 移动左指针
            } else {
                right--; // 移动右指针
            }
        }

        // 如果未找到符合条件的两个数
        return new int[]{-1};
    }

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        // 读取输入
        int n = scanner.nextInt();  // 数组长度
        int[] nums = new int[n];

        for (int i = 0; i < n; i++) {
            nums[i] = scanner.nextInt();
        }

        int target = scanner.nextInt();  // 目标值

        // 调用函数
        int[] result = findTwoSum(nums, target);

        // 输出结果
        if (result.length == 1 && result[0] == -1) {
            System.out.println(-1);
        } else {
            System.out.println(result[0] + " " + result[1]);
        }

        scanner.close();
    }
}
