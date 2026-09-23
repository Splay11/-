import java.io.*;
import java.util.regex.*;

public class Main {
    private static final Pattern INIT = Pattern.compile("ParkingLot\\((\\d+)\\)");
    private static final Pattern RESERVE = Pattern.compile("reserve\\((-?\\d+),\\s*(-?\\d+),\\s*(-?\\d+)\\)");
    private static final Pattern CANCEL = Pattern.compile("cancel\\((-?\\d+)\\)");
    private static final Pattern SPOT = Pattern.compile("spotOf\\((-?\\d+)\\)");
    private static final Pattern BUSY = Pattern.compile("busyCount\\((-?\\d+)\\)");

    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StringBuilder sb = new StringBuilder();
        String line;
        ParkingLot obj = null;
        while ((line = br.readLine()) != null) {
            line = line.trim();
            if (line.isEmpty()) continue;
            Matcher m;
            if ((m = INIT.matcher(line)).matches()) {
                obj = new ParkingLot(Integer.parseInt(m.group(1)));
                sb.append("null\n");
            } else if ((m = RESERVE.matcher(line)).matches()) {
                sb.append(obj.reserve(Integer.parseInt(m.group(1)), Integer.parseInt(m.group(2)),
                        Integer.parseInt(m.group(3)))).append('\n');
            } else if ((m = CANCEL.matcher(line)).matches()) {
                sb.append(obj.cancel(Integer.parseInt(m.group(1))) ? "true" : "false").append('\n');
            } else if ((m = SPOT.matcher(line)).matches()) {
                sb.append(obj.spotOf(Integer.parseInt(m.group(1)))).append('\n');
            } else if ((m = BUSY.matcher(line)).matches()) {
                sb.append(obj.busyCount(Integer.parseInt(m.group(1)))).append('\n');
            } else {
                throw new RuntimeException("bad op: " + line);
            }
        }
        System.out.print(sb.toString());
    }
}
