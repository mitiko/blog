#!/usr/bin/env python3

import re

data = []


def parse_nanos(s: str):
    if s.endswith('ns'):
        return float(s[:-2])
    if s.endswith('ms'):
        return float(s[:-2]) * 1_000
    if s.endswith('s'):
        return float(s[:-1]) * 1_000 * 1_000
    raise Exception('Unknown time unit')


# [ac-over-huff] [hsize:  7 ctx: 11 align: 0] csize: 388436 (ratio: 0.505), ctime: 54.287041ms (9ns per bit)
patterns = {
    'ac-over-huff': re.compile(
        r'\[ac-over-huff\] '
        r'\[hsize:\s+(?P<hsize>\d+) ctx:\s+(?P<ctx>\d+) align: 0\] '
        r'csize: (?P<csize>\d+) \(ratio: (?P<ratio>[\d\.]+)\), '
        r'ctime: (?P<ctime>[\d\w\.]+) \((?P<btime>[\w\d]+) per bit\)'
    )
}

parse_funcs = {
    'ac-over-huff': {
        'hsize': int,
        'ctx': int,
        'csize': int,
        'ratio': float,
        'ctime': parse_nanos,
        'btime': parse_nanos,
    }
}

for alg in patterns.keys():
    for line in open(f'{alg}.book1.log').read().split('\n'):
        x = patterns[alg].match(line)
        if x is None:
            continue
        obj = x.groupdict()
        for key, func in parse_funcs[alg].items():
            obj[key] = func(obj[key])
        obj['alg'] = alg
        data.append(obj)

print(data[0])
print(data[1])
print(data[2])

print('hello world')
