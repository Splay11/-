import java.io.*;
import java.util.*;

public class Main {
    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in, "UTF-8"));
        String line = br.readLine();
        if (line == null) return;
        line = line.trim();

        List<Integer> nums = new ArrayList<>();
        StringBuilder cur = new StringBuilder();
        for (int i = 0; i < line.length(); i++) {
            char c = line.charAt(i);
            if (Character.isDigit(c)) {
                cur.append(c);
            } else if (c == '-' && cur.length() == 0) {
                cur.append(c);
            } else if (cur.length() > 0) {
                nums.add(Integer.parseInt(cur.toString()));
                cur.setLength(0);
            }
        }
        if (cur.length() > 0) nums.add(Integer.parseInt(cur.toString()));

        Solution solution = new Solution();
        System.out.println(solution.countDistinctTags(nums));
    }
}
