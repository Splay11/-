import java.util.HashSet;
import java.util.Scanner;
import java.util.Set;

public class Main {
    public static int longestUniqueSubarrayLength(int[] a) {
        Set<Integer> seen = new HashSet<>(); // 用于记录当前窗口中的元素
        int left = 0; // 左指针
        int maxLength = 0; // 最长不重复子数组的长度

        // 遍历数组
        for (int right = 0; right < a.length; right++) {
            // 如果当前元素在窗口中已经存在，收缩窗口
            while (seen.contains(a[right])) {
                seen.remove(a[left]);
                left++;
            }

            // 加入当前元素
            seen.add(a[right]);

            // 更新最大长度
            maxLength = Math.max(maxLength, right - left + 1);
        }

        return maxLength;
    }

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);

        // 读取输入
        int n = scanner.nextInt(); // 数组的长度
        int[] a = new int[n];

        for (int i = 0; i < n; i++) {
            a[i] = scanner.nextInt(); // 读取数组元素
        }

        // 调用函数并输出结果
        System.out.println(longestUniqueSubarrayLength(a));

        scanner.close();
    }
}
