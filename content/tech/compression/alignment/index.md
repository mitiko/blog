+++
title = "Bit Alignment"
date = 2023-01-20
+++

the bitter lesson: <http://www.incompleteideas.net/IncIdeas/BitterLesson.html>

> all applies to streaming compression only

Compression is about selecting a proper context to make predictions.
Better context = better predictions.
Of course you need good counters to actually make use of the better
group-ification of statistics, you also need a fast enough hash table to store
statistics to make it practical. All those are somewhat solveable problems
they're not a bottleneck in any way.

We can identify two types of information in contexts. There is compressed
history information and metadata.
Compressed history is a shortened representation of the history - esentially it
becomes a compression problem inside the compression problem. Metadata is harder
because it's human centered. The whole split history + metadata.. it's a
construct. Metadata is a part of history in a way...
Anyways. The end goal is to not forget the bitter lesson. However, we're not
quite there with intelligence to apply it directly. It is still more efficient
to have multiple human tweaked models work on text data (paq8), than to task an
overly simplified model (because of RAM & time requirements) with the end-to-end.

**Solve end-to-end with intermediaries.**
Do not forget the bitter lesson.

Search + Learning.

## Metadata in contextes

Let's see how metadate helps improve contexts.

16-bit unaligned model:

```rust
pub struct M16Unaligned {
    stats: Vec<Counter>,
    history: u16,
}

impl Model for M16Unaligned {
    fn predict(&self) -> u16 {
        self.stats[usize::from(self.history)].p()
    }

    fn update(&mut self, bit: u8) {
        self.stats[usize::from(self.history)].update(bit);
        self.history = (self.history << 1) | u16::from(bit);
    }
}
```

13-bit byte-aligned model:

```rust
pub struct M13Aligned {
    stats: Vec<Counter>,
    ctx: u16,
    history: u16,
    alignment: u8,
}

impl Model for M13Aligned {
    fn predict(&self) -> u16 {
        self.stats[usize::from(self.ctx)].p()
    }

    fn update(&mut self, bit: u8) {
        self.stats[usize::from(self.ctx)].update(bit);
        const MASK: u16 = (1 << 14) - 1;
        self.history = ((self.history << 1) | u16::from(bit)) & MASK;
        self.alignment = (self.alignment + 1) & 7;
        self.ctx = u16::from(self.alignment) << 13 | self.history;
    }
}
```

Still thinks this is unfair?
Let's sort the bytes first, so each bit carries more information.
Alphabet sorting.

book1:

| Bits in context | Unaligned | Aligned | AS + Unaligned | AS + Aligned | Best         |
| --------------- | --------- | ------- | -------------- | ------------ | ------------ |
| 03              | 740328    | 547126  | 701045         | 646836       | Aligned      |
| 04              | 721602    | 536050  | 683232         | 505952       | AS + Aligned |
| 05              | 707976    | 517667  | 660869         | 491742       | AS + Aligned |
| 06              | 640341    | 489225  | 628396         | 463907       | AS + Aligned |
| 07              | 563172    | 458016  | 590271         | 440660       | AS + Aligned |
| 08              | 508907    | 444793  | 553455         | 431019       | AS + Aligned |
| 09              | 473541    | 415367  | 504842         | 416334       | Aligned      |
| 10              | 430896    | 404338  | 462193         | 407187       | Aligned      |
| 11              | 396781    | 388051  | 427001         | 397679       | Aligned      |
| 12              | 370391    | 374241  | 395650         | 384246       | Unaligned    |
| 13              | 352888    | 358818  | 374438         | 369778       | Unaligned    |
| 14              | 337972    | 344993  | 356393         | 354581       | Unaligned    |
| 15              | 327175    | 335510  | 342506         | 342769       | Unaligned    |
| 16              | 313698    | 328304  | 326140         | 334589       | Unaligned    |
| 17              | 301753    | 321466  | 310944         | 324559       | Unaligned    |
| 18              | 291328    | 314107  | 300857         | 318502       | Unaligned    |
| 19              | 286797    | 303951  | 292309         | 308738       | Unaligned    |
| 20              | 282894    | 295973  | 286985         | 299518       | Unaligned    |
| 21              | 279919    | 287653  | 282755         | 293032       | Unaligned    |
| 22              | 276948    | 284531  | 278741         | 286936       | Unaligned    |
| 23              | 273424    | 281316  | 276077         | 283274       | Unaligned    |
| 24              | 270054    | 278989  | 273770         | 280144       | Unaligned    |
| 25              | 270083    | 276390  | 273388         | 276885       | Unaligned    |
| 26              | 271357    | 273126  | 273966         | 274977       | Unaligned    |
| 27              | 276170    | 269887  | 276290         | 273195       | Aligned      |
| 28              | 280325    | 269982  | 280994         | 273061       | Aligned      |
| 29              | 284256    | 271294  | 284952         | 273740       | Aligned      |
| 30              | 287290    | 276125  | 289215         | 276166       | Aligned      |
| 31              | 291164    | 280294  | 294425         | 280925       | Aligned      |

Counter is 4 bytes => 1 << 26 bytes = 64 MB

## Conclusion

It seems unwise to trade off history bits for alignment bits when using
uncompressed history as context. After 12-bits the contexts _self-sync_ and
align themselves. And after 24, the contexts become too sparse to capture
relevant data.

<https://dougallj.wordpress.com/2022/07/30/parallelising-huffman-decoding-and-x86-disassembly-by-synchronising-non-self-synchronising-prefix-codes/>

Make it work, Make it strong, make it fast.

Entropy coding is inherently tightly coupled with the bit IO implementation.

Even if you create an abstraction, the coder will become coupled with that
abstraction and the implementation of the abstraction will become trivial, thus
rendering the abstraction useless. (Unless used like me for statistics purposes).
