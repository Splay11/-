import java.io.*;
import java.util.*;

public class Main {
    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in, "UTF-8"));
        String line = br.readLine();
        if (line == null) return;
        line = line.trim();

        // 解析 JSON 数组 [a,b,c,...]
        line = line.substring(1, line.length() - 1); // 去掉首尾 []
        String[] parts = line.split(",");
        int n = parts.length;
        int[] nums = new int[n];
        for (int i = 0; i < n; i++) {
            nums[i] = Integer.parseInt(parts[i].trim());
        }

        Solution solution = new Solution();
        int[] res = solution.sortArrayByParity(nums);

        // 输出 JSON 数组
        StringBuilder sb = new StringBuilder();
        sb.append("[");
        for (int i = 0; i < res.length; i++) {
            if (i > 0) sb.append(",");
            sb.append(res[i]);
        }
        sb.append("]");
        System.out.println(sb.toString());
    }
}
