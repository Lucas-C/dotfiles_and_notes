#!/usr/bin/env node
process.stdin.setEncoding('utf8');
process.stdin.on('data', function(val) {
    console.log(val.trim());
})
