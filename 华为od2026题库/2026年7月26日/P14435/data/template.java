import java.util.*;

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        String s = sc.nextLine();
        sc.close();

        // 统计 n：数 '[' 的数量减 1（最外层方括号）
        int n = 0;
        for (int i = 0; i < s.length(); i++) {
            if (s.charAt(i) == '[') n++;
        }
        n--;

        int[][] grid = new int[n][n];
        int depth = 0, row = 0, col = 0, num = 0;
        boolean inNum = false;

        for (int i = 0; i < s.length(); i++) {
            char c = s.charAt(i);
            if (c == '[') {
                depth++;
                if (depth == 2) col = 0;  // 进入新一行，列号归零
            } else if (c == ']') {
                if (inNum) { grid[row][col++] = num; num = 0; inNum = false; }
                if (depth == 2) row++;    // 当前行结束，行号加一
                depth--;
            } else if (c >= '0' && c <= '9') {
                num = num * 10 + (c - '0');
                inNum = true;
            } else if (c == ',' && inNum && depth == 2) {
                // 行内逗号分隔，结算当前数字
                grid[row][col++] = num;
                num = 0; inNum = false;
            }
        }

        Solution sol = new Solution();
        System.out.println(sol.countMinefields(grid));
    }
}
