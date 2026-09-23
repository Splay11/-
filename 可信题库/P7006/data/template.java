import java.io.*;
import java.util.regex.*;

public class Main {
    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String line;
        ClusterPool obj = null;
        Pattern addRe = Pattern.compile("addNode\\((-?\\d+),\\s*(-?\\d+)\\)");
        Pattern remRe = Pattern.compile("removeNode\\((-?\\d+)\\)");
        Pattern subRe = Pattern.compile("submit\\((-?\\d+),\\s*(-?\\d+)\\)");
        Pattern killRe = Pattern.compile("kill\\((-?\\d+)\\)");
        Pattern usedRe = Pattern.compile("usedOf\\((-?\\d+)\\)");
        Pattern freeRe = Pattern.compile("freeOf\\((-?\\d+)\\)");
        Pattern jobRe = Pattern.compile("jobNode\\((-?\\d+)\\)");
        while ((line = br.readLine()) != null) {
            line = line.trim();
            if (line.isEmpty()) continue;
            if (line.equals("ClusterPool()")) {
                obj = new ClusterPool();
                System.out.println("null");
            } else if (line.startsWith("addNode(")) {
                Matcher m = addRe.matcher(line);
                if (!m.matches()) throw new Exception("bad op");
                System.out.println(obj.addNode(Integer.parseInt(m.group(1)), Integer.parseInt(m.group(2))));
            } else if (line.startsWith("removeNode(")) {
                Matcher m = remRe.matcher(line);
                if (!m.matches()) throw new Exception("bad op");
                System.out.println(obj.removeNode(Integer.parseInt(m.group(1))));
            } else if (line.startsWith("submit(")) {
                Matcher m = subRe.matcher(line);
                if (!m.matches()) throw new Exception("bad op");
                System.out.println(obj.submit(Integer.parseInt(m.group(1)), Integer.parseInt(m.group(2))));
            } else if (line.startsWith("kill(")) {
                Matcher m = killRe.matcher(line);
                if (!m.matches()) throw new Exception("bad op");
                System.out.println(obj.kill(Integer.parseInt(m.group(1))));
            } else if (line.startsWith("usedOf(")) {
                Matcher m = usedRe.matcher(line);
                if (!m.matches()) throw new Exception("bad op");
                System.out.println(obj.usedOf(Integer.parseInt(m.group(1))));
            } else if (line.startsWith("freeOf(")) {
                Matcher m = freeRe.matcher(line);
                if (!m.matches()) throw new Exception("bad op");
                System.out.println(obj.freeOf(Integer.parseInt(m.group(1))));
            } else if (line.startsWith("jobNode(")) {
                Matcher m = jobRe.matcher(line);
                if (!m.matches()) throw new Exception("bad op");
                System.out.println(obj.jobNode(Integer.parseInt(m.group(1))));
            } else {
                throw new Exception("bad op");
            }
        }
    }
}
