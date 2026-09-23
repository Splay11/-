import java.io.*;

public class Main {
    private static String parseQuoted(String line) {
        line = line.trim();
        if (line.length() >= 2 && line.charAt(0) == '"' && line.charAt(line.length() - 1) == '"')
            return line.substring(1, line.length() - 1);
        return line;
    }

    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String line = br.readLine();
        if (line == null) return;
        String ans = new Solution().flipWorkId(parseQuoted(line));
        System.out.println("\"" + ans + "\"");
    }
}
