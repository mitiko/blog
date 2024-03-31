#!/usr/bin/env python3

import re
import matplotlib.pyplot as plt

data = []


def parse_nanos(s: str):
    if s.endswith('ns'):
        return float(s[:-2])
    if s.endswith('µs'):
        return float(s[:-2]) * 1_000
    if s.endswith('ms'):
        return float(s[:-2]) * 1_000_000
    if s.endswith('s'):
        return float(s[:-1]) * 1_000_000_000
    raise Exception('Unknown time unit')


patterns = {
    # [ac-over-huff] [hsize:  7, ctx: 11, align: 0] csize: 388436 (ratio: 0.505), ctime: 54.287041ms (9ns per bit)
    'ac-over-huff': re.compile(
        r'^\[ac-over-huff\] '
        r'\[hsize:\s+(?P<hsize>\d+), ctx:\s+(?P<ctx>\d+), align: 0\] '
        r'csize: (?P<csize>\d+) \(ratio: (?P<ratio>[\d\.]+)\), '
        r'ctime: (?P<ctime>[\w\.]+) \((?P<btime>[\w]+) per bit\)$'
    ),
    # [eh-ac] [ctx:  8, align: 0] csize: 687637 (ratio 0.894), ctime: 876.99425ms (143ns per bit)
    'eh-ac': re.compile(
        r'^\[eh-ac\] '
        r'\[ctx:\s+(?P<ctx>\d+), align:\s+(?P<align>\d+)\] '
        r'csize: (?P<csize>\d+) \(ratio (?P<ratio>[\d\.]+)\), '
        r'ctime: (?P<ctime>[\w\.]+) \((?P<btime>[\w\.]+) per bit\)$'
    ),
    # [eh-ac] [ctx:  8, align: 0, cache: 12] csize: 687637 (ratio 0.894), ctime: 730.138291ms (119ns per bit)
    'eh-ac-cached': re.compile(
        r'^\[eh-ac\] '
        r'\[ctx:\s+(?P<ctx>\d+), align:\s+(?P<align>\d+), cache:\s+(?P<cache>\d+)\] '
        r'csize: (?P<csize>\d+) \(ratio (?P<ratio>[\d\.]+)\), '
        r'ctime: (?P<ctime>[\w\.]+) \((?P<btime>[\w\.]+) per bit\)$'
    ),
    # [eh-huff] [rem_hsize:  7, hsize:  7, ctx:  8] csize: 414561 (ratio: 0.539), ctime: 118.488417ms (19ns per bit)
    'eh-huff': re.compile(
        r'^\[eh-huff\] '
        r'\[rem_hsize:\s+(?P<rem_hsize>\d+), hsize:\s+(?P<hsize>\d+), ctx:\s+(?P<ctx>\d+)\] '
        r'csize: (?P<csize>\d+) \(ratio: (?P<ratio>[\d\.]+)\), '
        r'ctime: (?P<ctime>[\w\.]+) \((?P<btime>[\w\.]+) per bit\)$'
    ),
    # [ordern] [ctx:  8, align: 0] csize: 508907 (ratio: 0.662), ctime: 106.565458ms (17ns per bit)
    'ordern': re.compile(
        r'^\[ordern\] '
        r'\[ctx:\s+(?P<ctx>\d+), align:\s+(?P<align>\d+)\] '
        r'csize: (?P<csize>\d+) \(ratio: (?P<ratio>[\d\.]+)\), '
        r'ctime: (?P<ctime>[\w\.]+) \((?P<btime>[\w\.]+) per bit\)$'
    ),
}

algs = ['ac-over-huff', 'eh-ac', 'eh-ac-cached', 'eh-huff', 'ordern']
parse_funcs = {
    alg: {
        'ctx': int,
        'csize': int,
        'ratio': float,
        'ctime': parse_nanos,
        'btime': parse_nanos,
    }
    for alg in algs
}
params = {
    'ac-over-huff': {'hsize': int},
    'eh-ac': {'align': int},
    'eh-ac-cached': {'align': int, 'cache': int},
    'eh-huff': {'rem_hsize': int, 'hsize': int},
    'ordern': {'align': int},
}
for alg in algs:
    parse_funcs.update(params[alg])

print('Reading logs...')
for alg in algs:
    for line in open(f'{alg}.book1.log').read().split('\n'):
        x = patterns[alg].match(line)
        if x is None:
            continue
        obj = x.groupdict()
        for key, func in parse_funcs[alg].items():
            obj[key] = func(obj[key])
        obj['alg'] = alg
        data.append(obj)

x1 = [x for x in data if x['alg'] == algs[0]][0]
x2 = [x for x in data if x['alg'] == algs[1]][0]
x3 = [x for x in data if x['alg'] == algs[2]][0]
x4 = [x for x in data if x['alg'] == algs[3]][0]
print(x1)
print(x2)
print(x3)
print(x4)

print('Plotting...')

# plot ctx vs csize
for alg in algs:
    if alg == 'eh-ac-cached':
        continue
    d = [x for x in data if x['alg'] == alg]
    xdata = list({x['ctx'] for x in d})
    xdata.sort()
    ydata = [min([x['csize'] for x in d if x['ctx'] == ctx]) for ctx in xdata]
    plt.plot(xdata, ydata, label=alg, marker='o', markersize=2)

plt.legend(loc='upper right')
plt.xlabel('ctx size (in bits)')
plt.ylabel('csize')
plt.savefig('ctx_vs_csize.png', dpi=300)
plt.close()

# TODO: fix
# plot ratio vs ctime
for alg in algs:
    d = [x for x in data if x['alg'] == alg]
    ctxs = list({x['ctx'] for x in d})
    ctxs.sort()
    xdata = [min([x['ratio'] for x in d if x['ctx'] == ctx]) for ctx in ctxs]
    xdata.sort()
    ydata = [min([x['ctime'] for x in d if x['ratio'] == ratio]) for ratio in xdata]
    plt.plot(xdata, ydata, label=alg, marker='o', markersize=2)
    # plt.plot(xdata, ydata, label=alg)

plt.yscale('log')
plt.gca().invert_xaxis()
plt.legend(loc='upper left')
plt.xlabel('ratio')
plt.ylabel('ctime (in ns)')
plt.savefig('ratio_vs_ctime.png', dpi=300)
plt.close()

print('Done')
