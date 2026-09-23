import java.util.Scanner;

public class Main {
    // 截图中的双指针：和等于 k 则左右都移动，和偏小则左移，和偏大则右移
    static int twoSum2(int[] nums, int k) {
        int left = 0;
        int right = nums.length - 1;
        int count = 0;
        // 数组有序且无重复，左右夹逼统计和为 k 的数对
        while (left < right) {
            long current_sum = (long) nums[left] + nums[right];
            if (current_sum == k) {
                // 找到一对，两侧都收一格；无重复所以不会再配同一对数
                count += 1;
                left += 1;
                right -= 1;
            } else if (current_sum < k) {
                // 当前和偏小，左端右移让 nums[left] 变大
                left += 1;
            } else {
                // 当前和偏大，右端左移让 nums[right] 变小
                right -= 1;
            }
        }
        return count;
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int n = sc.nextInt();
        int k = sc.nextInt();
        int[] nums = new int[n];
        for (int i = 0; i < n; i++) {
            nums[i] = sc.nextInt();
        }
        System.out.println(twoSum2(nums, k));
        sc.close();
    }
}
