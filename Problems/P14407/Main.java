public class Solution {
    private static double weighted(long amount, long start, long end, long qs, long qe) {
        if (start > qe || end < qs) return 0.0;
        long duration = end - start;
        if (duration == 0) {
            if (qs <= start && start <= qe) return amount;
            return 0.0;
        }
        long os = Math.max(start, qs);
        long oe = Math.min(end, qe);
        if (os > oe) return 0.0;
        long overlap = oe - os;
        return amount * (double) overlap / (double) duration;
    }

    private static int roundToI32(double x) {
        long val;
        if (x >= 0)
            val = (long) Math.floor(x + 0.5);
        else
            val = (long) Math.ceil(x - 0.5);
        if (val > 2147483647L) return 2147483647;
        if (val < -2147483648L) return -2147483648;
        return (int) val;
    }

    public int queryNetEnergy(String[] commands) {
        String query = commands[commands.length - 1];
        String[] qparts = query.split(",", -1);
        String versionStr = qparts[1].trim();
        long qs = Long.parseLong(qparts[2]);
        long qe = Long.parseLong(qparts[3]);
        boolean useAll = versionStr.equals("A");
        int maxVersion = useAll ? 1_000_000_000 : Integer.parseInt(versionStr);

        double total = 0.0;
        int version = 0;
        for (int i = 0; i < commands.length - 1; i++) {
            version++;
            if (version > maxVersion) break;
            String[] parts = commands[i].split(",", -1);
            if (parts[0].equals("AddProductionRecord")) {
                long amount = Long.parseLong(parts[2]);
                long start = Long.parseLong(parts[3]);
                long end = Long.parseLong(parts[4]);
                total += weighted(amount, start, end, qs, qe);
            } else if (parts[0].equals("AddConsumptionRecord")) {
                long amount = Long.parseLong(parts[1]);
                long start = Long.parseLong(parts[2]);
                long end = Long.parseLong(parts[3]);
                total -= weighted(amount, start, end, qs, qe);
            }
        }
        return roundToI32(total);
    }
}
