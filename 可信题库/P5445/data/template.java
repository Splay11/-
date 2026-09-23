import java.io.*;
import java.util.regex.*;

public class Main {
    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        PickupDesk obj = null;
        Pattern init = Pattern.compile("PickupDesk\\(\\)");
        Pattern order = Pattern.compile("order\\((-?\\d+)\\)");
        Pattern serve = Pattern.compile("serve\\(\\)");
        Pattern waiting = Pattern.compile("waiting\\(\\)");
        String line;
        while ((line = br.readLine()) != null) {
            line = line.trim();
            if (line.isEmpty()) continue;
            Matcher m;
            if ((m = init.matcher(line)).matches()) {
                obj = new PickupDesk();
                System.out.println("null");
            } else if ((m = order.matcher(line)).matches()) {
                System.out.println(obj.order(Integer.parseInt(m.group(1))));
            } else if (serve.matcher(line).matches()) {
                System.out.println(obj.serve());
            } else if (waiting.matcher(line).matches()) {
                System.out.println(obj.waiting());
            } else {
                throw new RuntimeException("bad op: " + line);
            }
        }
    }
}
