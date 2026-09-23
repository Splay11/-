import java.io.*;

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

    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in, "UTF-8"));
        String line = br.readLine();
        if (line == null) return;
        line = line.trim();

        int comma = findTopLevelComma(line);
        int n = Integer.parseInt(line.substring(0, comma).trim());

        String rest = line.substring(comma + 1).trim();
        // 提取引号内的字符串
        int startQuote = rest.indexOf('"');
        int endQuote = rest.lastIndexOf('"');
        String channels = rest.substring(startQuote + 1, endQuote);

        Solution solution = new Solution();
        System.out.println(solution.mergeBroadcastChannels(n, channels));
    }
}
