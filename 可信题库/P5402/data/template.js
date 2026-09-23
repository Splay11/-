const fs = require('fs');
process.nextTick(() => {
    let raw = fs.readFileSync(0, 'utf8');
    if (raw.endsWith('\n')) raw = raw.slice(0, -1);
    if (raw.endsWith('\r')) raw = raw.slice(0, -1);
    const lines = raw.split(/\r?\n/);
    const tray = JSON.parse(lines[0]);
    const stamp = JSON.parse(lines[1] || '[]');
    const ans = new Solution().findStampPos(tray, stamp);
    const r = ans && ans.length >= 2 ? ans[0] : -1;
    const c = ans && ans.length >= 2 ? ans[1] : -1;
    process.stdout.write('[' + r + ', ' + c + ']\n');
});
