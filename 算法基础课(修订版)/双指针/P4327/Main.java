import java.util.*;

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int n = sc.nextInt();  // 读入关卡数

        // 读入两个数组 arr 和 brr
        int[] arr = new int[n];
        int[] brr = new int[n];
        for (int i = 0; i < n; ++i) {
            arr[i] = sc.nextInt();
        }
        for (int i = 0; i < n; ++i) {
            brr[i] = sc.nextInt();
        }

        // 计算差分数组
        int[] diff_a = new int[n - 1];
        int[] diff_b = new int[n - 1];
        for (int i = 0; i < n - 1; ++i) {
            diff_a[i] = arr[i + 1] - arr[i];
            diff_b[i] = brr[i + 1] - brr[i];
        }

        // 滑动窗口方法
        int left = 0, right = 0, ans = 0;
        int m = diff_a.length;

        while (left < m) {
            // 右指针移动到相等区间的最右边
            while (right < m && diff_a[right] == diff_b[right]) {
                right++;
            }
            // 计算该区间的长度
            ans = Math.max(ans, right - left);
            // 左指针移动到右指针的位置，开始新的检查
            left = right + 1;
            right = left;
        }

        // 输出最大长度加 1（因为差分数组少一个元素）
        System.out.println(ans + 1);

        sc.close();
    }
}
