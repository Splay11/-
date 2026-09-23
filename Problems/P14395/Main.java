import java.util.ArrayList;
import java.util.Comparator;

public class Solution {
    public String[] filterValidAClassIPs(String[] ips) {
        ArrayList<Entry> valid = new ArrayList<>();
        for (String ip : ips) {
            int[] key = parseValid(ip);
            // 仅保留通过全部校验的 A 类内网 IP
            if (key != null) valid.add(new Entry(ip, key));
        }
        // 先比第二段，再比第三段，最后比第四段（均为数值比较）
        valid.sort(Comparator.comparingInt((Entry e) -> e.key[0])
                .thenComparingInt(e -> e.key[1])
                .thenComparingInt(e -> e.key[2]));
        String[] ans = new String[valid.size()];
        for (int i = 0; i < valid.size(); i++) ans[i] = valid.get(i).ip;
        return ans;
    }

    /** 暂存合法 IP 及其排序键 */
    private static class Entry {
        String ip;
        int[] key; // key[0..2] 对应第二、三、四分段

        Entry(String ip, int[] key) {
            this.ip = ip;
            this.key = key;
        }
    }

    /**
     * 校验单个 IP 字符串。
     * @return 合法时返回后三段数值；非法返回 null
     */
    private int[] parseValid(String ip) {
        // -1 保留末尾空串，便于识别 "10.1.2." 这类非法输入
        String[] parts = ip.split("\\.", -1);
        if (parts.length != 4) return null;
        int[] nums = new int[4];
        for (int i = 0; i < 4; i++) {
            String p = parts[i];
            if (p.isEmpty()) return null;
            // 前导零非法，单独的 "0" 合法
            if (p.length() > 1 && p.charAt(0) == '0') return null;
            for (int j = 0; j < p.length(); j++) {
                char c = p.charAt(j);
                if (c < '0' || c > '9') return null;
            }
            int v = Integer.parseInt(p);
            if (v < 0 || v > 255) return null;
            nums[i] = v;
        }
        // A 类内网首段必须是 10
        if (nums[0] != 10) return null;
        return new int[] {nums[1], nums[2], nums[3]};
    }
}
