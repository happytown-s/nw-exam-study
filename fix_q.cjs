const fs = require('fs');
const path = 'C:/Users/haro/.openclaw/workspace/nw-exam-study/src/data/build_subjectb.cjs';
let content = fs.readFileSync(path, 'utf8');
// Fix: replace "question", with "question":
content = content.replace(/"question",/g, '"question":');
fs.writeFileSync(path, content);
console.log('Fixed!');
