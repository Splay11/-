import java.util.Scanner;

public class Main{
    public static int shortestAllLettersSubstring(String s) {
        int[] count = new int[26]; // 用于记录每个字母的出现次数
        int unique = 0; // 窗口中不同字母的数量
        int n = s.length();
        int minLen = n + 1; // 初始值设置为大于最大可能长度
        int left = 0;

        for (int right = 0; right < n; right++) {
            char c = s.charAt(right);
            if (c >= 'a' && c <= 'z') { // 仅处理小写字母
                int idx = c - 'a';
                if (count[idx] == 0) {
                    unique++; // 新增一个不同的字母
                }
                count[idx]++;
            }

            // 当窗口包含所有26个字母时，尝试收缩左边界
            while (unique == 26) {
                minLen = Math.min(minLen, right - left + 1); // 更新最小长度
                char cl = s.charAt(left);
                if (cl >= 'a' && cl <= 'z') {
                    int idx = cl - 'a';
                    count[idx]--;
                    if (count[idx] == 0) {
                        unique--; // 如果移出的是唯一的字母，unique减少
                    }
                }
                left++; // 收缩窗口
            }
        }

        return (minLen <= n) ? minLen : -1; // 如果找到了符合条件的子串，返回最小长度，否则返回 -1
    }

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        String s = scanner.nextLine().trim(); // 输入字符串
        System.out.println(shortestAllLettersSubstring(s)); // 输出最短子串长度
        scanner.close();
    }
}
