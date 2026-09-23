import java.io.*;
import java.util.*;
import java.util.regex.*;

public class Main {
    private static String trim(String s) {
        return s.trim();
    }

    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String line;
        LogSystem obj = null;
        ArrayList<String> outs = new ArrayList<>();
        Pattern enterPat = Pattern.compile("enter\\((\\d+)\\s*,\\s*(true|false)\\)");
        Pattern leavePat = Pattern.compile("leave\\((\\d+)\\)");
        Pattern logPat = Pattern.compile("log\\(\"(.*)\"\\)");
        while ((line = br.readLine()) != null) {
            line = trim(line);
            if (line.isEmpty()) continue;
            if (line.equals("LogSystem()")) {
                obj = new LogSystem();
                outs.add("null");
            } else if (line.startsWith("log(")) {
                Matcher m = logPat.matcher(line);
                if (!m.matches()) throw new Exception("bad log");
                outs.add("\"" + obj.log(m.group(1)) + "\"");
            } else if (line.startsWith("enter(")) {
                Matcher m = enterPat.matcher(line);
                if (!m.matches()) throw new Exception("bad enter");
                obj.enter(Integer.parseInt(m.group(1)), m.group(2).equals("true"));
                outs.add("null");
            } else if (line.startsWith("leave(")) {
                Matcher m = leavePat.matcher(line);
                if (!m.matches()) throw new Exception("bad leave");
                obj.leave(Integer.parseInt(m.group(1)));
                outs.add("null");
            } else {
                throw new Exception("bad op");
            }
        }
        for (int i = 0; i < outs.size(); i++) {
            System.out.print(outs.get(i));
            System.out.print("\n");
        }
    }
}
