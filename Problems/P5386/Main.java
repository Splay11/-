import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.List;
import java.util.Queue;
import java.util.Scanner;

public class Main {
    static class TreeNode {
        int val;
        TreeNode left;
        TreeNode right;
        TreeNode(int v) {
            val = v;
        }
    }

    static List<String> parseTokens(String line) {
        // 去掉首尾花括号，按逗号拆成权值或空位 #
        String s = line.trim();
        if (s.startsWith("{") && s.endsWith("}")) {
            s = s.substring(1, s.length() - 1);
        }
        List<String> toks = new ArrayList<String>();
        if (s.isEmpty()) {
            return toks;
        }
        String[] parts = s.split(",");
        for (int i = 0; i < parts.length; i++) {
            toks.add(parts[i].trim());
        }
        return toks;
    }

    static TreeNode buildTree(List<String> toks) {
        // 层序建树：空位不入队
        if (toks.isEmpty() || toks.get(0).equals("#")) {
            return null;
        }
        TreeNode rt = new TreeNode(Integer.parseInt(toks.get(0)));
        Queue<TreeNode> q = new ArrayDeque<TreeNode>();
        q.add(rt);
        int i = 1;
        while (!q.isEmpty() && i < toks.size()) {
            TreeNode node = q.poll();
            if (i < toks.size()) {
                if (!toks.get(i).equals("#")) {
                    node.left = new TreeNode(Integer.parseInt(toks.get(i)));
                    q.add(node.left);
                }
                i++;
            }
            if (i < toks.size()) {
                if (!toks.get(i).equals("#")) {
                    node.right = new TreeNode(Integer.parseInt(toks.get(i)));
                    q.add(node.right);
                }
                i++;
            }
        }
        return rt;
    }

    static int treeDepth(TreeNode root) {
        // 广度优先：根到最远叶子经过的结点数
        if (root == null) {
            return 0;
        }
        Queue<TreeNode> q = new ArrayDeque<TreeNode>();
        q.add(root);
        int d = 0;
        while (!q.isEmpty()) {
            d++;
            int sz = q.size();
            for (int k = 0; k < sz; k++) {
                TreeNode node = q.poll();
                if (node.left != null) {
                    q.add(node.left);
                }
                if (node.right != null) {
                    q.add(node.right);
                }
            }
        }
        return d;
    }

    static int solveLine(String line) {
        return treeDepth(buildTree(parseTokens(line)));
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        String line = sc.nextLine();
        System.out.println(solveLine(line));
        sc.close();
    }
}
