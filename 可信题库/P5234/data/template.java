import java.io.*;

public class Main {
    private static String parseQuoted(String line) {
        line = line.trim();
        if (line.length() < 2 || line.charAt(0) != '"' || line.charAt(line.length() - 1) != '"')
            throw new RuntimeException("bad");
        return line.substring(1, line.length() - 1);
    }

    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in, "UTF-8"));
        String line = br.readLine();
        if (line == null) return;
        String ans = new Solution().sortLetter(parseQuoted(line));
        System.out.println("\"" + ans + "\"");
    }
}
