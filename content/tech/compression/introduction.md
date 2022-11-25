+++
title = "Introduction"
date = 2022-10-24
draft = true
template = "sections/todo.html"

[extra]
katex = true
+++

From [wikipedia](https://en.wikipedia.org/wiki/Data_compression):
> In information theory, data compression is the process of encoding information using fewer bits than the original representation.
> 
> Compression can be either lossy or lossless.  
> No information is lost in lossless compression.


Let \\(s = \Alpha^*\\) be a string over an alphabet of symbols \\(\Alpha\\).

In practice symbols are unicode codepoints, bytes, LZ match pairs, nibbles, or just bits.


Lossless compression is achieved iff:
$$
D(E(s)) = s
$$
