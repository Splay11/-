import java.io.*;
import java.util.regex.*;

public class Main {
    private static final Pattern P = Pattern.compile("^\"(.*)\"\\s*,\\s*\"(.*)\"$");

    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in, "UTF-8"));
        String line = br.readLine();
        if (line == null) return;
        Matcher m = P.matcher(line.trim());
        if (!m.matches()) throw new RuntimeException("bad input");
        System.out.println(new Solution().countFormableGroups(m.group(1), m.group(2)));
    }
}
