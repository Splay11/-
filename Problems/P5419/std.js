// 偶数长度窗口上 0/1 数量相等：交错串 0101... 一定合法

function buildBalanced01(k) {
    // 灯位从 1 开始：奇数位放 0，偶数位放 1
    const chars = [];
    for (let i = 1; i <= k; i++) {
        chars.push(i % 2 === 1 ? "0" : "1");
    }
    return chars.join("");
}

function main(input) {
    const lines = input.trim().split(/\n/);
    // 第一行灯带长度，第二行窗口条数
    const k = Number(lines[0].trim());
    // 后面 q 行 a,b 不用参与构造
    console.log(buildBalanced01(k));
}

let _input = "";
process.stdin.on("data", (c) => { _input += c; });
process.stdin.on("end", () => main(_input));
