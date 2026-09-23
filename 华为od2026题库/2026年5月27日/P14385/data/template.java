import java.io.*;
import java.util.*;

public class Main {
    private static int findTopLevelComma(String s) {
        boolean inString = false;
        int bracket = 0;

        for (int i = 0; i < s.length(); i++) {
            char c = s.charAt(i);

            if (c == '"') {
                inString = !inString;
            } else if (!inString) {
                if (c == '[') {
                    bracket++;
                } else if (c == ']') {
                    bracket--;
                } else if (c == ',' && bracket == 0) {
                    return i;
                }
            }
        }

        return -1;
    }

    private static List<String> parseStringList(String s) {
        List<String> list = new ArrayList<>();
        StringBuilder cur = new StringBuilder();
        boolean inString = false;

        for (int i = 0; i < s.length(); i++) {
            char c = s.charAt(i);

            if (c == '"') {
                if (inString) {
                    list.add(cur.toString());
                    cur.setLength(0);
                }
                inString = !inString;
            } else if (inString) {
                cur.append(c);
            }
        }

        return list;
    }

    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in, "UTF-8"));
        String line = br.readLine();

        if (line == null) {
            return;
        }

        line = line.trim();

        int comma = findTopLevelComma(line);
        String studentsStr = line.substring(0, comma);
        String votesStr = line.substring(comma + 1);

        List<String> studentsList = parseStringList(studentsStr);
        List<String> votesList = parseStringList(votesStr);

        // 转成 String[]，匹配用户代码接口
        String[] students = studentsList.toArray(new String[0]);
        String[] votes = votesList.toArray(new String[0]);

        Solution solution = new Solution();

        // 题目要求输出带双引号的字符串
        System.out.println("\"" + solution.electMonitor(students, votes) + "\"");
    }
}
