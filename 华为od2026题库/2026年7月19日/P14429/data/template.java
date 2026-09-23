import java.io.*;
import java.util.*;

public class Main {
    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in, "UTF-8"));
        String line = br.readLine();
        if (line == null) return;
        line = line.trim();

        // 顶层逗号分隔 n 与乘客列表
        int comma = line.indexOf(',');
        int n = Integer.parseInt(line.substring(0, comma).trim());
        String rest = line.substring(comma + 1).trim();

        // 提取所有整数并两两配对为 [起点,终点]
        List<Integer> nums = new ArrayList<>();
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < rest.length(); i++) {
            char c = rest.charAt(i);
            if (Character.isDigit(c)) {
                sb.append(c);
            } else if (sb.length() > 0) {
                nums.add(Integer.parseInt(sb.toString()));
                sb.setLength(0);
            }
        }
        if (sb.length() > 0) nums.add(Integer.parseInt(sb.toString()));

        List<List<Integer>> passengers = new ArrayList<>();
        for (int i = 0; i + 1 < nums.size(); i += 2) {
            List<Integer> pair = new ArrayList<>();
            pair.add(nums.get(i));
            pair.add(nums.get(i + 1));
            passengers.add(pair);
        }

        Solution solution = new Solution();
        System.out.println(solution.maxRideProfit(n, passengers));
    }
}
