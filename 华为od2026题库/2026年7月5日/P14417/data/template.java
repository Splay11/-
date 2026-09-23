import java.io.*;
import java.util.*;

public class Main {
    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in, "UTF-8"));
        String line = br.readLine();
        if (line == null) return;
        line = line.trim();

        // 解析 JSON 数组 ["tree","frm","to"]
        List<String> parts = new ArrayList<>();
        StringBuilder cur = new StringBuilder();
        boolean inStr = false;
        for (int i = 0; i < line.length(); i++) {
            char c = line.charAt(i);
            if (c == '"') {
                inStr = !inStr;
                if (!inStr) {
                    parts.add(cur.toString());
                    cur.setLength(0);
                }
            } else if (inStr) {
                cur.append(c);
            }
        }

        String treeLevelOrder = parts.get(0);
        String frm = parts.get(1);
        String to = parts.get(2);

        Solution solution = new Solution();
        System.out.println(solution.minJumps(treeLevelOrder, frm, to));
    }
}
