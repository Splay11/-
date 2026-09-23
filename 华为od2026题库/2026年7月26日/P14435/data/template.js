// 从 stdin 读取 JSON 格式输入
var input = '';
process.stdin.on('data', function(chunk) {
    input += chunk;
});
process.stdin.on('end', function() {
    var grid = JSON.parse(input.trim());

    // 调用用户代码
    var result = countMinefields(grid);

    // 输出结果
    console.log(result);
});
