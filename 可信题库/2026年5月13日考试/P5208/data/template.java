import java.io.*;
import java.util.*;
import java.util.regex.*;

public class Main {
    private static int[] parseIntArray(String s) {
        s = s.trim();
        if (s.equals("[]")) return new int[0];
        s = s.substring(1, s.length() - 1).trim();
        if (s.isEmpty()) return new int[0];
        String[] parts = s.split(",");
        int[] arr = new int[parts.length];
        for (int i = 0; i < parts.length; i++) arr[i] = Integer.parseInt(parts[i].trim());
        return arr;
    }

    private static String fmtList(int[] a) {
        if (a.length == 0) return "[]";
        StringBuilder sb = new StringBuilder();
        sb.append('[');
        for (int i = 0; i < a.length; i++) {
            if (i > 0) sb.append(", ");
            sb.append(a[i]);
        }
        sb.append(']');
        return sb.toString();
    }

    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String line;
        GCSystem obj = null;
        ArrayList<String> outs = new ArrayList<>();
        Pattern gcSys = Pattern.compile("GCSystem\\((\\d+)\\)");
        Pattern create = Pattern.compile("createObject\\((\\d+)\\)");
        Pattern manual = Pattern.compile("manualGC\\((\\d+)\\)");
        Pattern getLive = Pattern.compile("getLiveObjects\\((\\d+)\\)");
        while ((line = br.readLine()) != null) {
            line = line.trim();
            if (line.isEmpty()) continue;
            if (line.startsWith("GCSystem(")) {
                Matcher m = gcSys.matcher(line);
                m.matches();
                obj = new GCSystem(Integer.parseInt(m.group(1)));
                outs.add("null");
            } else if (line.startsWith("createObject(")) {
                Matcher m = create.matcher(line);
                m.matches();
                obj.createObject(Integer.parseInt(m.group(1)));
                outs.add("null");
            } else if (line.startsWith("markObjects(")) {
                String inner = line.substring("markObjects(".length(), line.length() - 1);
                obj.markObjects(parseIntArray(inner));
                outs.add("null");
            } else if (line.startsWith("manualGC(")) {
                Matcher m = manual.matcher(line);
                m.matches();
                obj.manualGC(Integer.parseInt(m.group(1)));
                outs.add("null");
            } else if (line.startsWith("getLiveObjects(")) {
                Matcher m = getLive.matcher(line);
                m.matches();
                outs.add(fmtList(obj.getLiveObjects(Integer.parseInt(m.group(1)))));
            } else {
                throw new Exception("bad op");
            }
        }
        for (String o : outs) System.out.println(o);
    }
}
