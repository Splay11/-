import java.util.Arrays;
import java.util.Scanner;

public class Main {
    static String kthLargestNumber(String[] nums, int k) {
        // 自定义比较器按「数值从大到小」排序
        Arrays.sort(nums, (a, b) -> {
            if (a.length() != b.length()) {
                // 长度不同：长的数更大，排在前面
                return b.length() - a.length();
            }
            // 长度相同且无前导零：字典序大的数更大，排在前面
            return b.compareTo(a);
        });
        // 第 k 大对应排序后下标 k-1（重复字符串各自占一个名次，不需要去重）
        return nums[k - 1];
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        // 第一行：n（数组长度）和 k（排名）
        int n = sc.nextInt();
        int k = sc.nextInt();
        // 第二行：n 个表示非负整数的字符串
        String[] nums = new String[n];
        for (int i = 0; i < n; i++) {
            nums[i] = sc.next();
        }

        // 输出第 k 大的那个字符串
        System.out.println(kthLargestNumber(nums, k));
        sc.close();
    }
}
