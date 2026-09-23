import java.io.*;
import java.util.*;

public class Main {
    // 从输入字符串中提取所有非负整数
    private static List<Integer> parseNumbers(String s) {
        List<Integer> nums = new ArrayList<>();
        int i = 0;
        while (i < s.length()) {
            if (Character.isDigit(s.charAt(i))) {
                int val = 0;
                while (i < s.length() && Character.isDigit(s.charAt(i))) {
                    val = val * 10 + (s.charAt(i) - '0');
                    i++;
                }
                nums.add(val);
            } else {
                i++;
            }
        }
        return nums;
    }

    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in, "UTF-8"));
        String line = br.readLine();
        if (line == null) return;
        line = line.trim();
        if (line.length() == 0) return;

        List<Integer> nums = parseNumbers(line);
        int playerCount = nums.get(0);
        int[][] playerTimeRange = new int[playerCount][2];

        // 第一个数字是 n，后面每两个数字组成一个区间
        int idx = 1;
        for (int i = 0; i < playerCount; i++) {
            playerTimeRange[i][0] = nums.get(idx++);
            playerTimeRange[i][1] = nums.get(idx++);
        }

        Solution solution = new Solution();
        System.out.println(solution.MaxPlayers(playerCount, playerTimeRange));
    }
}
