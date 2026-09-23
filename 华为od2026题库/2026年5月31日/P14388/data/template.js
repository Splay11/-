// LeetCode 核心代码模式 - JavaScript 输入输出模板
const fs = require('fs');
process.nextTick(() => {
    const input = fs.readFileSync(0, 'utf8').trim();
    // 输入形如: {12,23,7,13,8}
    const content = input.replace(/^\{|\}$/g, '').trim();
    let arr = [];
    if (content.length > 0) {
        arr = content.split(',').map(s => parseInt(s.trim())).filter(s => !isNaN(s));
    }
    // 构建链表
    function ListNode(val, next) {
        this.val = val;
        this.next = next || null;
    }
    let dummy = new ListNode(0);
    let cur = dummy;
    for (let v of arr) {
        cur.next = new ListNode(v);
        cur = cur.next;
    }
    const head = dummy.next;

    const res = gameResult(head);
    console.log('"' + res + '"');
});
