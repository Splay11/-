import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;

public class Solution {
    public int[] getLoadedFileIds(int[] fileIds, int[] parentIds, int targetId) {
        HashMap<Integer, ArrayList<Integer>> children = new HashMap<>();
        for (int i = 0; i < fileIds.length; i++) {
            children.computeIfAbsent(parentIds[i], k -> new ArrayList<>()).add(fileIds[i]);
        }
        ArrayList<Integer> ans = new ArrayList<>();
        ArrayList<Integer> stack = new ArrayList<>();
        stack.add(targetId);
        while (!stack.isEmpty()) {
            int u = stack.remove(stack.size() - 1);
            ans.add(u);
            ArrayList<Integer> ch = children.get(u);
            if (ch != null) {
                for (int v : ch) stack.add(v);
            }
        }
        int[] out = new int[ans.size()];
        for (int i = 0; i < ans.size(); i++) out[i] = ans.get(i);
        Arrays.sort(out);
        return out;
    }
}
