import java.util.Arrays;
import java.util.Scanner;

public class Main {
    // 滑动窗口：对每个右端点，无重复窗口内长度为 k 及以上的子串个数可 O(1) 计算
    static long countUnique(String s, int k) {
        int n = s.length();
        // last[c]：字符 c 上一次出现的下标，-1 表示还没出现过
        int[] last = new int[26];
        Arrays.fill(last, -1);
        int left = 0;
        long ans = 0;
        for (int right = 0; right < n; right++) {
            int idx = s.charAt(right) - 'a';
            // 窗口内出现重复，把左端推到上一次该字符的右边
            if (last[idx] >= left) {
                left = last[idx] + 1;
            }
            last[idx] = right;
            // 以 right 为右端、长度 >= k 的起点最多到 right-k+1，且不能小于 left
            int limit = right - k + 1;
            if (limit >= left) {
                ans += (long) (limit - left + 1);
            }
        }
        return ans;
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        String s = sc.next();
        int k = sc.nextInt();
        System.out.println(countUnique(s, k));
        sc.close();
    }
}
