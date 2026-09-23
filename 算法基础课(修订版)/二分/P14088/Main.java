import java.util.*;

public class Main {

    // 自定义实现的lowerBound函数
    // 功能：找到第一个不小于x的位置
    public static int lowerBound(List<Integer> A, int x) {
        int left = 0, right = A.size() - 1;
        while (left <= right) {
            int mid = left + (right - left) / 2;
            if (A.get(mid) < x) {
                left = mid + 1;  // x在右半部分
            } else {
                right = mid - 1;  // x在左半部分或当前位置
            }
        }
        return left;  // 返回第一个不小于x的位置
    }

    // 自定义实现的upperBound函数
    // 功能：找到第一个大于x的位置
    public static int upperBound(List<Integer> A, int x) {
        int left = 0, right = A.size() - 1;
        while (left <= right) {
            int mid = left + (right - left) / 2;
            if (A.get(mid) <= x) {
                left = mid + 1;  // x在右半部分
            } else {
                right = mid - 1;  // x在左半部分
            }
        }
        return left;  // 返回第一个大于x的位置
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        // 输入数组的大小n
        int n = sc.nextInt();
        List<Integer> A = new ArrayList<>();

        // 输入数组A的元素
        for (int i = 0; i < n; i++) {
            A.add(sc.nextInt());
        }

        // 输入整数C
        int C = sc.nextInt();

        // 对数组A进行排序
        Collections.sort(A);

        long sum = 0;  // 用于存储满足条件的数对总数

        // 遍历数组中的每个元素
        for (int i = 0; i < A.size(); i++) {
            int x = A.get(i) + C;  // 计算目标值 x = A[i] + C

            // 使用自定义的upperBound和lowerBound查找x的出现次数
            sum += upperBound(A, x) - lowerBound(A, x);
        }

        // 输出满足条件的数对总数
        System.out.println(sum);
    }
}
