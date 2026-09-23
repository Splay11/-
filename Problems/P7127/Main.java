import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.StringTokenizer;

public class Main {
    static class Node {
        int val;
        Node prev;
        Node next;
        Node(int v) {
            val = v;
        }
    }

    // 用给定序列建成双向循环链表，返回原头节点
    static Node buildCircular(int[] vals) {
        Node head = new Node(vals[0]);
        Node cur = head;
        for (int i = 1; i < vals.length; i++) {
            Node nxt = new Node(vals[i]);
            cur.next = nxt;
            nxt.prev = cur;
            cur = nxt;
        }
        // 头尾互连，形成循环
        cur.next = head;
        head.prev = cur;
        return head;
    }

    // 在循环链表最前面插入值为 x 的新节点，返回新头
    static Node insertFront(Node head, int x) {
        Node nxt = new Node(x);
        Node tail = head.prev;
        // 新节点夹在原来的尾和头之间
        nxt.next = head;
        nxt.prev = tail;
        tail.next = nxt;
        head.prev = nxt;
        return nxt;
    }

    // 从 head 沿后继走 cnt 步，收集节点值
    static List<Integer> traverse(Node head, int cnt) {
        List<Integer> out = new ArrayList<>();
        Node cur = head;
        for (int i = 0; i < cnt; i++) {
            out.add(cur.val);
            cur = cur.next;
        }
        return out;
    }

    static List<Integer> insertAndList(int[] vals, int x) {
        Node head = buildCircular(vals);
        head = insertFront(head, x);
        return traverse(head, vals.length + 1);
    }

    public static void main(String[] args) throws IOException {
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        StringTokenizer st = new StringTokenizer(br.readLine());
        int n = Integer.parseInt(st.nextToken());
        int x = Integer.parseInt(st.nextToken());
        st = new StringTokenizer(br.readLine());
        int[] vals = new int[n];
        for (int i = 0; i < n; i++) {
            vals[i] = Integer.parseInt(st.nextToken());
        }
        List<Integer> ans = insertAndList(vals, x);
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < ans.size(); i++) {
            if (i > 0) {
                sb.append(' ');
            }
            sb.append(ans.get(i));
        }
        System.out.println(sb);
    }
}
