import java.util.*;

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        ServiceMgrSys sys = new ServiceMgrSys();
        System.out.println("null");
        if (sc.hasNextLine()) {
            sc.nextLine(); // ServiceMgrSys()
        }
        while (sc.hasNextLine()) {
            String line = sc.nextLine().trim();
            if (line.isEmpty()) {
                continue;
            }
            if (line.startsWith("startService")) {
                String inner = line.substring(line.indexOf('(') + 1, line.lastIndexOf(')'));
                String[] parts = inner.split(",", 2);
                int serverId = Integer.parseInt(parts[0].trim());
                String serviceName = parts[1].trim().replace("\"", "");
                System.out.println(sys.startService(serverId, serviceName));
            } else if (line.startsWith("addDependency")) {
                String inner = line.substring(line.indexOf('(') + 1, line.lastIndexOf(')'));
                String[] parts = inner.split(",", 2);
                String fromService = parts[0].trim().replace("\"", "");
                String toService = parts[1].trim().replace("\"", "");
                System.out.println(sys.addDependency(fromService, toService));
            } else if (line.startsWith("isServiceAvailable")) {
                String serviceName = line.substring(line.indexOf('(') + 1, line.lastIndexOf(')'))
                        .replace("\"", "").trim();
                System.out.println(sys.isServiceAvailable(serviceName));
            } else if (line.startsWith("rebootServers")) {
                String inside = line.substring(line.indexOf('[') + 1, line.indexOf(']'));
                String[] serverIds = inside.split(",");
                int[] ids = new int[serverIds.length];
                for (int i = 0; i < serverIds.length; i++) {
                    ids[i] = Integer.parseInt(serverIds[i].trim());
                }
                sys.rebootServers(ids);
                System.out.println("null");
            }
        }
    }
}
