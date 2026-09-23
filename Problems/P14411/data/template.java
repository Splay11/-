import java.io.*;
import java.util.*;

class TreeNode {
    int val;
    TreeNode left;
    TreeNode right;

    TreeNode(int val) {
        this.val = val;
    }
}

public class Main {
    private static TreeNode buildTree(String treeStr) {
        String s = treeStr.trim();
        if (s.equals("{}") || s.equals("{#}")) return null;
        if (!s.startsWith("{") || !s.endsWith("}")) throw new RuntimeException("bad tree");
        String inner = s.substring(1, s.length() - 1).trim();
        if (inner.isEmpty() || inner.equals("#")) return null;
        String[] tokens = inner.split(",");
        for (int i = 0; i < tokens.length; i++) tokens[i] = tokens[i].trim();
        if (tokens[0].equals("#")) return null;
        TreeNode root = new TreeNode(Integer.parseInt(tokens[0]));
        Queue<TreeNode> q = new ArrayDeque<>();
        q.add(root);
        int idx = 1;
        while (!q.isEmpty() && idx < tokens.length) {
            TreeNode node = q.poll();
            if (idx < tokens.length) {
                String t = tokens[idx++];
                if (!t.equals("#")) {
                    node.left = new TreeNode(Integer.parseInt(t));
                    q.add(node.left);
                }
            }
            if (idx < tokens.length) {
                String t = tokens[idx++];
                if (!t.equals("#")) {
                    node.right = new TreeNode(Integer.parseInt(t));
                    q.add(node.right);
                }
            }
        }
        return root;
    }

    private static int[] parseLine(String line) {
        line = line.trim();
        int depth = 0;
        int end = -1;
        for (int i = 0; i < line.length(); i++) {
            char c = line.charAt(i);
            if (c == '{') depth++;
            else if (c == '}') {
                depth--;
                if (depth == 0) {
                    end = i;
                    break;
                }
            }
        }
        if (end < 0) throw new RuntimeException("bad input");
        String treeStr = line.substring(0, end + 1);
        String rest = line.substring(end + 1);
        if (!rest.startsWith(",")) throw new RuntimeException("bad threshold");
        int threshold = Integer.parseInt(rest.substring(1).trim());
        return new int[] {0, threshold};
    }

    public static void main(String[] args) throws Exception {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in, "UTF-8"));
        String line = br.readLine();
        if (line == null) return;
        line = line.trim();
        int depth = 0;
        int end = -1;
        for (int i = 0; i < line.length(); i++) {
            char c = line.charAt(i);
            if (c == '{') depth++;
            else if (c == '}') {
                depth--;
                if (depth == 0) {
                    end = i;
                    break;
                }
            }
        }
        String treeStr = line.substring(0, end + 1);
        int threshold = Integer.parseInt(line.substring(end + 2).trim());
        TreeNode root = buildTree(treeStr);
        Solution sol = new Solution();
        int[] ans = sol.analyzeSpiritPaths(root, threshold);
        StringBuilder sb = new StringBuilder("[");
        for (int i = 0; i < ans.length; i++) {
            if (i > 0) sb.append(",");
            sb.append(ans[i]);
        }
        sb.append("]");
        System.out.println(sb.toString());
    }
}
