const fs = require('fs');
const line = fs.readFileSync(0, 'utf8').trim();
const parts = line.split(',');
const M = parseInt(parts[0], 10);
const N = parseInt(parts[1], 10);
const result = getNthValue(M, N);
console.log(result);
