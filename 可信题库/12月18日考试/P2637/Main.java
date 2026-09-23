import java.util.*;

public class Main {
    static class ServiceMgrSys {
        Map<String, Set<Integer>> running = new HashMap<>();
        Map<Integer, Set<String>> onServer = new HashMap<>();
        Map<String, Set<String>> deps = new HashMap<>();

        void rebootServers(int[] serverIds) {
            for (int sid : serverIds) {
                Set<String> names = onServer.getOrDefault(sid, Collections.emptySet());
                for (String name : new ArrayList<>(names)) {
                    Set<Integer> servers = running.get(name);
                    if (servers != null) {
                        servers.remove(sid);
                        if (servers.isEmpty()) running.remove(name);
                    }
                }
                onServer.put(sid, new HashSet<>());
            }
        }

        boolean startService(int serverId, String serviceName) {
            Set<String> set = onServer.computeIfAbsent(serverId, k -> new HashSet<>());
            if (set.contains(serviceName)) return false;
            set.add(serviceName);
            running.computeIfAbsent(serviceName, k -> new HashSet<>()).add(serverId);
            return true;
        }

        boolean addDependency(String fromServiceName, String toServiceName) {
            Set<String> set = deps.computeIfAbsent(fromServiceName, k -> new HashSet<>());
            if (set.contains(toServiceName)) return false;
            set.add(toServiceName);
            return true;
        }

        boolean isServiceAvailable(String serviceName) {
            Map<String, Boolean> memo = new HashMap<>();
            return dfs(serviceName, memo);
        }

        private boolean dfs(String name, Map<String, Boolean> memo) {
            if (memo.containsKey(name)) return memo.get(name);
            Set<Integer> servers = running.get(name);
            if (servers == null || servers.isEmpty()) {
                memo.put(name, false);
                return false;
            }
            for (String dep : deps.getOrDefault(name, Collections.emptySet())) {
                if (!dfs(dep, memo)) {
                    memo.put(name, false);
                    return false;
                }
            }
            memo.put(name, true);
            return true;
        }
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        ServiceMgrSys sys = new ServiceMgrSys();
        System.out.println("null");
        if (sc.hasNextLine()) sc.nextLine(); // 构造行
        while (sc.hasNextLine()) {
            String line = sc.nextLine().trim();
            if (line.isEmpty()) continue;
            if (line.startsWith("startService")) {
                String[] parts = line.substring(line.indexOf('(') + 1, line.lastIndexOf(')')).split(",");
                int serverId = Integer.parseInt(parts[0].trim());
                String serviceName = parts[1].trim().replace("\"", "");
                System.out.println(sys.startService(serverId, serviceName));
            } else if (line.startsWith("addDependency")) {
                String[] parts = line.substring(line.indexOf('(') + 1, line.lastIndexOf(')')).split(",");
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
