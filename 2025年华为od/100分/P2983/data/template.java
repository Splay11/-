import java.io.*;

public class Main {
    private static String parseQuoted(String line) {
        if (line != null && line.length() >= 2 && line.charAt(0) == '"'
                && line.charAt(line.length() - 1) == '"') {
            return line.substring(1, line.length() - 1);
        }
        return line == null ? "" : line;
    }

    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in, "UTF-8"));
        String line = br.readLine();
        System.out.println(new Solution().maxBracketDepth(parseQuoted(line)));
    }
}
