#!/usr/bin/python3

text = open("book1").read()
print(text)

counts = [0]*(1<<16)
mask = (1 << 16) - 1
ctx = 0

for ch in text:
    byte = ord(ch) & 0xff
    ctx = ((ctx << 8) | byte) & mask
    counts[ctx] += 1

top10 = sorted(range(len(counts)), key=lambda k: counts[k], reverse=True)[:10]
for ctx, count in [(x, counts[x]) for x in top10]:
    print(f"'{chr(ctx >> 8)}{chr(ctx & 0xff)}' - {count}")
