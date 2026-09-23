import java.io.*;

public class Main {
    private static class Parsed {
        String sn;
        int m;

        Parsed(String sn, int m) {
            this.sn = sn;
            this.m = m;
        }
    }

    private static Parsed parseInput(String line) {
        line = line.trim();
        if (line.isEmpty() || line.charAt(0) != '"') throw new RuntimeException("bad input");
        int i = 1;
        StringBuilder sn = new StringBuilder();
        while (i < line.length() && line.charAt(i) != '"') sn.append(line.charAt(i++));
        if (i >= line.length() || line.charAt(i) != '"') throw new RuntimeException("bad string end");
        i++;
        if (i >= line.length() || line.charAt(i) != ',') throw new RuntimeException("bad comma");
        int m = Integer.parseInt(line.substring(i + 1).trim());
        return new Parsed(sn.toString(), m);
    }

    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in, "UTF-8"));
        String line = br.readLine();
        if (line == null) return;
        Parsed in = parseInput(line);
        String ans = new Solution().rearrangeSN(in.sn, in.m);
        System.out.println('"' + ans + '"');
    }
}
