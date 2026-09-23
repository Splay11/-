import java.io.*;
import java.util.regex.*;

public class Main {
    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        ParkingLane obj = null;
        Pattern init = Pattern.compile("ParkingLane\\((-?\\d+)\\)");
        Pattern arr = Pattern.compile("arrive\\((-?\\d+)\\)");
        Pattern dep = Pattern.compile("depart\\((-?\\d+)\\)");
        String line;
        while ((line = br.readLine()) != null) {
            line = line.trim();
            if (line.isEmpty()) continue;
            Matcher m;
            if ((m = init.matcher(line)).matches()) {
                obj = new ParkingLane(Integer.parseInt(m.group(1)));
                System.out.println("null");
            } else if ((m = arr.matcher(line)).matches()) {
                System.out.println(obj.arrive(Integer.parseInt(m.group(1))));
            } else if (line.equals("admit()")) {
                System.out.println(obj.admit());
            } else if ((m = dep.matcher(line)).matches()) {
                System.out.println(obj.depart(Integer.parseInt(m.group(1))));
            } else if (line.equals("undo()")) {
                System.out.println(obj.undo());
            } else if (line.equals("front()")) {
                System.out.println(obj.front());
            } else if (line.equals("waiting()")) {
                System.out.println(obj.waiting());
            } else if (line.equals("size()")) {
                System.out.println(obj.size());
            } else return;
        }
    }
}
