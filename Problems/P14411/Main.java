public class Solution {
    private static final int INT_MIN_VAL = -2147483648;

    private static class State {
        int maxVal = INT_MIN_VAL;
        int count = 0;
        int hasGe = 0;
    }

    public int[] analyzeSpiritPaths(TreeNode root, int threshold) {
        if (root == null) {
            return new int[] {INT_MIN_VAL, 0, 0};
        }
        State st = new State();
        dfs(root, 0L, false, threshold, st);
        if (st.count == 0) {
            st.maxVal = INT_MIN_VAL;
        }
        return new int[] {st.maxVal, st.hasGe, st.count};
    }

    private void dfs(TreeNode node, long curSum, boolean prevNeg, int threshold, State st) {
        boolean isNeg = node.val < 0;
        if (isNeg && prevNeg) {
            return;
        }
        long newSum = curSum + node.val;
        boolean isLeaf = node.left == null && node.right == null;
        if (isLeaf) {
            st.maxVal = Math.max(st.maxVal, (int) newSum);
            st.count++;
            if (newSum >= threshold) {
                st.hasGe = 1;
            }
            return;
        }
        if (node.left != null) {
            dfs(node.left, newSum, isNeg, threshold, st);
        }
        if (node.right != null) {
            dfs(node.right, newSum, isNeg, threshold, st);
        }
    }
}
