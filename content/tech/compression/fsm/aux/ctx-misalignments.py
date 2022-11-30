#!/usr/bin/python3

# printable ascii: http://facweb.cs.depaul.edu/sjost/it212/documents/ascii-pr.htm
chars = [ord(' ') + x for x in range(ord('~') - ord(' '))]
search_ctx = (ord('t') << 8) | ord('h')
total_matches = 0

for i in range(len(chars)):
    for j in range(len(chars)):
        for k in range(len(chars)):
            a, b, c = chars[i], chars[j], chars[k]
            bin_repr = (a << 16) | (b << 8) | c

            # skip obvious matches
            if b == ord('t') and c == ord('h'):
                continue

            for offset in range(8):
                if (bin_repr >> offset) & 0xff_ff == search_ctx:
                    total_matches += 1
                    print(f"Found match for '{chr(a)}', '{chr(b)}', '{chr(c)}'")

if total_matches != 0:
    print(f"{total_matches} total matches")