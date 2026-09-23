public class Solution {
    public String[] sortConvertedNums(int[] nums, int base) {
        int n = nums.length;
        String[] converted = new String[n];
        for (int i = 0; i < n; i++) {
            converted[i] = toBase(nums[i], base);
        }
        int[] order = new int[n];
        for (int i = 0; i < n; i++) order[i] = i;
        // 选择排序下标：按原整数降序，等价于按进制串十进制值降序
        for (int i = 0; i < n; i++) {
            int best = i;
            for (int j = i + 1; j < n; j++) {
                if (nums[order[j]] > nums[order[best]]) best = j;
            }
            int tmp = order[i];
            order[i] = order[best];
            order[best] = tmp;
        }
        String[] ans = new String[n];
        for (int i = 0; i < n; i++) ans[i] = converted[order[i]];
        return ans;
    }

    private String toBase(int n, int base) {
        if (n == 0) return "0";
        String digits = "0123456789abcdef";
        StringBuilder sb = new StringBuilder();
        while (n > 0) {
            sb.append(digits.charAt(n % base));
            n /= base;
        }
        return sb.reverse().toString();
    }
}
