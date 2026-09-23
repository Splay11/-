import java.util.Scanner;
import java.lang.Math;

public class AppleDistribution {

    // 检查给小明分配 x 个苹果是否可行
    // n: 小孩总数, m: 苹果总数, k: 小明编号
    private static boolean check(long x, long n, long m, long k) {
        if (x == 0) {
            return true;
        }
        long needed = x; // 小明自己需要 x 个

        // 计算左边小孩需要的苹果数
        long leftKids = k - 1;
        if (leftKids > 0) {
            // 苹果数从 x-1 递减到 1 的小孩数量
            long l = Math.min(leftKids, x - 1);
            // 等差数列求和 (x-1 + x-l) * l / 2，简化为 l*x - l*(l+1)/2
            needed += l * x - l * (l + 1) / 2;
            // 剩下的小孩每人一个
            if (leftKids > l) {
                needed += (leftKids - l);
            }
        }

        // 计算右边小孩需要的苹果数
        long rightKids = n - k;
        if (rightKids > 0) {
            // 苹果数从 x-1 递减到 1 的小孩数量
            long r = Math.min(rightKids, x - 1);
            // 等差数列求和
            needed += r * x - r * (r + 1) / 2;
            // 剩下的小孩每人一个
            if (rightKids > r) {
                needed += (rightKids - r);
            }
        }
        
        return needed <= m;
    }

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        long n = scanner.nextLong();
        long m = scanner.nextLong();
        long k = scanner.nextLong();

        long low = 1, high = m, ans = 0;

        // 二分查找答案
        while (low <= high) {
            long mid = low + (high - low) / 2;
            if (mid == 0) { // 至少一个苹果
                low = mid + 1;
                continue;
            }
            if (check(mid, n, m, k)) {
                // 如果 mid 可行，尝试更大的值
                ans = mid;
                low = mid + 1;
            } else {
                // 如果 mid 不可行，需要减小
                high = mid - 1;
            }
        }

        System.out.println(ans);
        scanner.close();
    }
}
