const fs = require("fs");

// Bash 博弈：n 能被 k+1 整除则后手胜，否则先手胜
function whoWins(n, k) {
    // 每 k+1 颗构成一轮：先手若面对 k+1 的倍数，无论取 1~k 颗，
    // 后手都能取到刚好补成 k+1，把倍数局面丢回给先手
    if (n % (k + 1) === 0) {
        return "后手";
    }
    return "先手";
}

function main() {
    const tokens = fs.readFileSync(0, "utf8").trim().split(/\s+/).map(Number);
    console.log(whoWins(tokens[0], tokens[1]));
}

main();
