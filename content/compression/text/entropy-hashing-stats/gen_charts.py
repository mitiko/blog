#!/usr/bin/env python3

import re
data = []

# parse ac-over-huff

# [ac-over-huff] [hsize:  7 ctx: 11 align: 0] csize: 388436 (ratio: 0.505), ctime: 54.287041ms (9ns per bit)
pat = re.compile('\[ac-over-huff\] \[hsize:\s+(\d+) ctx:\s+(\d+) align: 0\] csize: (\d+) \(ratio: ([\d\.]+)\), ctime: ([\d\w\.]+) \(([\w\d]+) per bit\)')
for line in open('ac-over-huff.book1.log').read().split('\n'):
    if not line.startswith('[ac-over-huff]'):
        pass
    x = pat.match(line)
    print(x.groups())
    break
    pass

print("hello world")
