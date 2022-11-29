#!/usr/bin/python3

import re

out_annotated = open("book1-annotated", "w")
out_postfixes = open("book1-postfixes", "w")

# ctx = "th"
ctx = "an"
postfix_list = [] # use an ordered set for bigger files

# we match the context, and capture the postfix character
pattern = rf'{ctx}(.)'

for line in open("book1"):    
    def _sub(match):
        postfix = match.group(1)
        if postfix not in postfix_list:
            postfix_list.append(postfix)

        # the stylesheet defines colors for _0, _1, _2, _3,
        # others will remain blank
        id = postfix_list.index(postfix)
        repl = f'<span class="_{id}">{postfix}</span>'

        out_postfixes.write(repl)
        return f'<span class="ctx">{ctx}</span>{repl}'

    annotated_line = re.sub(pattern, _sub, line)
    out_annotated.write(annotated_line)
