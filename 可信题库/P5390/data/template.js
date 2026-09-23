const fs = require('fs');
process.nextTick(() => {
    const raw = fs.readFileSync(0, 'utf8');
    const s = raw.replace(/[\r\n]+$/, '');
    console.log(new Solution().reviseMarks(s));
});
