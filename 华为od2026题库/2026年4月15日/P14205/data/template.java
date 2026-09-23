import java.io.*;
import java.util.*;

public class Main {
    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in, "UTF-8"));
        String s = br.readLine();
        if (s == null) return;
        s = s.trim();

        // 兼容输入带双引号的情况，如 "uuuua"
        if (s.length() >= 2 && s.charAt(0) == '"' && s.charAt(s.length() - 1) == '"') {
            s = s.substring(1, s.length() - 1);
        }

        Solution solution = new Solution();
        List<List<Integer>> ans = solution.countKeys(s);

        StringBuilder sb = new StringBuilder();
        sb.append("[");
        for (int i = 0; i < ans.size(); i++) {
            if (i > 0) sb.append(",");
            sb.append("[").append(ans.get(i).get(0)).append(",").append(ans.get(i).get(1)).append("]");
        }
        sb.append("]");
        System.out.print(sb.toString());
    }
}
