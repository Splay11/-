import java.io.*;
import java.util.regex.*;

public class Main {
    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String line;
        ParcelSlots obj = null;
        Pattern ctorRe = Pattern.compile("ParcelSlots\\((-?\\d+)\\)");
        Pattern putRe = Pattern.compile("put\\((-?\\d+),\\s*(-?\\d+)\\)");
        Pattern takeRe = Pattern.compile("take\\((-?\\d+)\\)");
        Pattern moveRe = Pattern.compile("moveRight\\((-?\\d+)\\)");
        while ((line = br.readLine()) != null) {
            line = line.trim();
            if (line.isEmpty()) continue;
            if (line.startsWith("ParcelSlots(")) {
                Matcher m = ctorRe.matcher(line);
                if (!m.matches()) throw new Exception("bad op");
                obj = new ParcelSlots(Integer.parseInt(m.group(1)));
                System.out.println("null");
            } else if (line.startsWith("put(")) {
                Matcher m = putRe.matcher(line);
                if (!m.matches()) throw new Exception("bad op");
                System.out.println(obj.put(Integer.parseInt(m.group(1)), Integer.parseInt(m.group(2))));
            } else if (line.startsWith("take(")) {
                Matcher m = takeRe.matcher(line);
                if (!m.matches()) throw new Exception("bad op");
                System.out.println(obj.take(Integer.parseInt(m.group(1))));
            } else if (line.startsWith("moveRight(")) {
                Matcher m = moveRe.matcher(line);
                if (!m.matches()) throw new Exception("bad op");
                System.out.println(obj.moveRight(Integer.parseInt(m.group(1))));
            } else if (line.equals("occupied()")) {
                System.out.println(obj.occupied());
            } else {
                throw new Exception("bad op");
            }
        }
    }
}
