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
                if (c == '[') bracket++;
                else if (c == ']') bracket--;
                else if (c == ',' && bracket == 0) return i;
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
        if (line == null) return;
        line = line.trim();

        int comma = findTopLevelComma(line);
        int month = Integer.parseInt(line.substring(0, comma).trim());

        String rest = line.substring(comma + 1).trim();
        int split = rest.indexOf("],[");
        String employeesStr = rest.substring(0, split + 1);
        String birthdaysStr = rest.substring(split + 2);

        List<String> employees = parseStringList(employeesStr);
        List<String> birthdays = parseStringList(birthdaysStr);

        Solution solution = new Solution();
        System.out.println(solution.countBirthdayGifts(month, employees, birthdays));
    }
}
