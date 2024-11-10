+++
title = "L1 histories"
date = 2024-11-07
+++

When you get into data compression, one of the fist things you learn about is
entropy. It builds this expectation that you can't cheat entropy, yet while a
simple order-0 static (stationary) model compressor fulfills that expectation of
~50% compression ratios, state-of-the-art compressors achieve 11% and less.  
How could that be?

Of course, the informational content of text is much less than just the
statistical probability of individual letters. We know that intuitively but
there's a very simple demonstration to prove it:

Consider the string `eeedeeedecceecdeddecddeebdeebae` consisting of 1 `a`, 2 `b`,
4 `c`, 8 `d`, 16 `e`.
Information theory says entropy is `1.793` bits per character, or a total of
$31 \times 1.793 = 55.583$ bits.  
Yet, we can sort the string and apply RLE using 4 bits for count and assume the
letter order to get just $5 \times 4 = 20$ bits.  
So it **must be** that the other `35.5` bits are in some way encoding order.
That is the cost of our assumptions.

Of course, this example is quite simplistic (and for the purposes of my article,
very small). I still feel like it illustrates my point but if you need further
proof, see for yourself that any simple order-0 / order-1 coders do
significantly better on BWT-encoded text vs the original.  
Why? BWT decorrelates.

---

We need a way to encode what is essentially an index of the list of all
permutations of the input:

```
00 abcd
01 abdc
02 acbd
03 acdb
04 adbc
...
23 dcba
```

Fear no longer, for entropy coding comes to the rescue!

Turns out that's exactly what arithmetic coding / range coding and ANS do. Take
away all the finite-precision math & tricks to make it work for binary alphabets,
entropy coders produce a bitstream that is exactly a variable-length index into
the space of all possible text permutations, provided a probability distribution
for each consecutive symbol.

This transforms the problem of compression to just modeling the probability
distribution of symbols at each position of the text input.  
Compression is an intelligence task. Compression may never be solved (provably
so at least) but better AI = better compression; and AGI = general-purpose
compressor.

---

So, what makes a good model?
Let's start at the source - it us humans that produce text (in response to
living in this world). Undestanding how humans think and write is crucial.

I'll simplify it - **history repeats itself.**  
Evolution favors brains that are also good models, the pattern hungry brains.
All you have to do is notice the patterns. If you drop an apple, it will fall.
If you jump in the river, you'll get wet. If the previous letter in a word is
`q`, you can expect a `u` right after.  
But how do you decide what is relevant. Why doesn't the tree next to the river
have an effect on you getting wet?  
I shall call this **decorrelation**.


Decorrelation is the process of splitting a complex signal into many simpler
ones, each closer to an iid, by reducing cross-correlation between individual
signals.  
Usually this is done by evaluating a context function at each index. This is
how paq8 and most CM compressors work today.

<!-- https://en.wikipedia.org/wiki/Kosambi–Karhunen–Loève_theorem -->
<!-- where the orthogonal functions are {1 if ctx(i) == val, else 0 } -->
<!-- does that mean that {Z_i} are iid? -->

Consider the history of symbols as our text input:

$$
h = [a_0, a_1, a_2, ..., a_n]
$$

and a context function operating on a prefix of the history:

$$
\text{ctx}(h, i) = \text{ctx}([a_0, a_1, ..., a_i])
$$

It is important to note, this context function has a finite codomain.
Also, while not a requirement, we shall consider non-injective functions.

Said simply - the context function compresses the history into a finite set of
bits. This way, different positions in the text may have the same compressed
history and we'll produce the same probability distribution for the next symbol.

$$
\text{ctx}: H \to C
$$

The context function maps history prefixes to context values.

Thus we can finally define level/layer 1 history as:

$$
l_1(h, \text{ctx}, v) = \{a_i: \text{ctx}(h, i) = v\}
$$

Why do I call it level/layer 1 history? Well, because you essentially perform compression on this decorrelated signal, though with a much smaller model.

We shall define the class of all level/layer 1 histories as:

$$
\mathcal{L}_1(h, \text{ctx}) = \{ \forall v \in C, \ l_1(h, \text{ctx}, v) \}
$$

Furthermore, we may define the next layer as well:

$$
l_2(h, c_1, c_2, v_1, v_2) = \{ a_i: c_2(l_1, i) = v_2 \}
$$

What makes adaptivity a better predictor?


Outline:
-> static models take advantage of symbols' statistical probability, order doesn't matter
-> 

Static models take advantage of symbols' statistical probability. From a static
model's perspective order doesn't matter.

But the 
But order of letters in text co

[1]: https://en.wikipedia.org/wiki/Independent_and_identically_distributed_random_variables#Examples "wiki of iid"

'aaaabbbbbbbbcccccccccccccccc'



What makes text compressible?
<!-- How does compression work?
What makes compression feasible? -->
First off, everybody knows that fixed-length encoding is a big waste.
By barely utilizing the statisical probability of letters we can reach
compression ratios of [50% or more](Huffman coding wiki & stats).
Modern entropy coders have transformed the challenge to 





$$
h = ["t", "h", "e", " ", "b", "r", "o", "w", "n", " ", "f", "o", "x"]
$$

context: (symbol[]) -> value

l1 = (symbol[], context_fn, context_val) -> symbol[]

l2 = (symbol[], context_fn, context_val) -> symbol[]

counter: (symbol[]) -> state[]
(symbol) -> state

predictor: (state[], symbol[], context_fn) -> probability[]
(state, context) -> probability

P(symbol = guess | context) x P(context) > P(symbol = guess)

P(symbol) * log(P(guess))

P(guess) = P(symbol)

entropy coding is a unique way to encode index of permutation
most of data is held in the order of letters, not their probabilities

-> list of wikipedia articles
-> based on random seed, decide which X articles to include
-> 



// novel approaches:
// -> how do we map symbol[] to state[] to probability[]
// what is a state?
// can states be learned?

model = 

compressor = (byte[]) -> byte[]


