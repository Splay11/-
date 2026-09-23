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

    // 按输入顺序建双向循环链表；空序列返回 null，对应原链表为空
    static Node buildCircular(int[] vals) {
        if (vals.length == 0) {
            return null;
        }
        Node head = new Node(vals[0]);
        Node cur = head;
        // 依次把后续节点接到当前尾巴后面，同时维护 prev
        for (int i = 1; i < vals.length; i++) {
            Node nxt = new Node(vals[i]);
            cur.next = nxt;
            nxt.prev = cur;
            cur = nxt;
        }
        // 头尾互连成环
        cur.next = head;
        head.prev = cur;
        return head;
    }

    // 把头插节点接到循环链表最前面；空表时新节点自环
    static Node insertFront(Node head, int x) {
        Node nxt = new Node(x);
        if (head == null) {
            // 空表：唯一节点的前驱、后继都指向自己
            nxt.next = nxt;
            nxt.prev = nxt;
            return nxt;
        }
        // 非空：新节点夹在原尾和原头之间，四条指针都要改
        Node tail = head.prev;
        nxt.next = head;
        nxt.prev = tail;
        tail.next = nxt;
        head.prev = nxt;
        return nxt;
    }

    // 从新头沿后继走 cnt 步，正好一圈
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
        int[] vals = new int[n];
        // n=0 时没有第二行，不要再 readLine
        if (n > 0) {
            st = new StringTokenizer(br.readLine());
            for (int i = 0; i < n; i++) {
                vals[i] = Integer.parseInt(st.nextToken());
            }
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
