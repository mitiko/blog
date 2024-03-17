+++
title = "It's decorrelators all the way down"
date = 2024-03-16

[extra]
math = true
+++

<!-- "for contrast" ? -->
The file size of book1 is 768'771 bytes. The best models can compress that to
about 200'000 bytes.  
But what if we sort it? Then we can take advantage of the sorted order with
[RLE][1] and compress to under 1024 bytes.  
This shows that most of the information content is in the ordering and not the
_ontology_ of bytes. But you knew that already (hopefully).

There are multiple ways of encoding an ordering. The simplest is perhaps
[BWT][2] - a sort of _reversible_ sort, a contextualized sort, which is not a
sort but gets you close enough where the post-transform data becomes much more
compressible with simple models.  
<!-- TODO: m03, BWT, LZ, CM info -->

If you were to encode each symbol (bytes in the case of ascii text, but could be
nibbles or even words) using a code...

---

<!-- ----------------------------------------------------------------------- -->
<!-- This is all introductory level shit. Make the article about decorrelation. -->

A good metric for how compressible data is entropy. However entropy predicts
compression rates far smaller than current state of the art compressors. Why?  
There still exists a lot of redundant information in the ordering of symbols.
Certain symbols often get grouped together. And how words (common groups of
symbols) get ordered is what gives text meaning.  
Up to here, we've only been removing the obvious statistical redundancy of text -
grammar, punctuation, dictionary phrases, repetitions etc.  
The real challenge is harnessing the power of the computer, of AI to..


Text compression is about decorrelating the ordering of bytes.
You can do that by compressing history.



[1]: https://en.wikipedia.org/wiki/Run-length_encoding
[2]: TODO:
