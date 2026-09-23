const fs = require("fs");

// 滑动窗口：对每个右端点，无重复窗口内长度为 k 及以上的子串个数可 O(1) 计算
function countUnique(s, k) {
    const n = s.length;
    // last[c]：字符 c 上一次出现的下标，-1 表示还没出现过
    const last = Array(26).fill(-1);
    let left = 0;
    let ans = 0;
    for (let right = 0; right < n; right++) {
        const idx = s.charCodeAt(right) - 97;
        // 窗口内出现重复，把左端推到上一次该字符的右边
        if (last[idx] >= left) {
            left = last[idx] + 1;
        }
        last[idx] = right;
        // 以 right 为右端、长度 >= k 的起点最多到 right-k+1，且不能小于 left
        const limit = right - k + 1;
        if (limit >= left) {
            ans += limit - left + 1;
        }
    }
    return ans;
}

function main() {
    const tokens = fs.readFileSync(0, "utf8").trim().split(/\s+/);
    const s = tokens[0];
    const k = Number(tokens[1]);
    console.log(String(countUnique(s, k)));
}

main();
