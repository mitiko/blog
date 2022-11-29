+++
title = "On FSMs"
# the world of FSMs in data compression
# !! compressing data with way too many FSMs
# # this isn't as much abt FSMs as it is about contexts and histories..
# History is (almost always) bound to repeat itself
date = 2022-11-15
draft = true

[extra]
katex = true
style = "styles/tech/fsm.css"
+++

We've [established](@/tech/compression/introduction.md) that the problem of compression mostly
boils down to good predictors. The better the prediction, the better the compression ratio.  
The heart of a compressor is its model.

## Static vs Adaptive models

[Predictive models](https://en.wikipedia.org/wiki/Predictive_modelling) generally make the assumption
that future events will happen about as often as they have happened in the past (within a certain context of course).  
There exists a close resemblance to [Markov models](https://en.wikipedia.org/wiki/Markov_model) which satisfy the
[Markov property](https://en.wikipedia.org/wiki/Markov_property):

$$
P(X_n = x_n \mid X_{n-1} = x_{n-1}, ..., X_0 = x_0) = P(X_n = x_n \mid X_{n-1} = x_{n-1})
$$

Where \\(X = \\{X_t: \Omega \rightarrow \mathcal{S}\\}_{t \in \N}\\) is a stochastic process for
some [probability space](https://en.wikipedia.org/wiki/Probability_space) \\(\(\Omega, \mathcal{F}, P\)\\)
and a set of states \\(\mathcal{S}\\).

Except in our case, the [memorylessness](https://en.wikipedia.org/wiki/Memorylessness) property
is defined a bit more generally and the set of states is actually an alphabet of symbols
(could be bits, bytes, UTF-8 codepoints, pixels, etc):

$$
P(X_n = x_n \mid \text{history}) = P(X_n = x_n \mid \text{hash}(\text{history}))
$$

Where \\(\text{history} = (X_{n-1} = x_{n-1}, ..., X_0 = x_0)\\) is a list of the previously encountered symbols and
\\(\text{hash}: \mathcal{S}^* \rightarrow \mathcal{C}\\) is a function that maps histories to contexts.

The main difference between static and adaptive models is how often adaptation is applied.
Static models get updated on a per block basis, whilst adaptive models run updates online.  

When decompressing, adaptive models have to wait for the next symbol to be decoded to make the next prediction.
This dependency chain slows down decompression tremendously. Static models are much faster in this regard but
require the context space be much smaller. Usually \\(\| \mathcal{C} \| \leq 2^{16}\\).
This restriction, however, directly impacts compression ratios.

Thus, static models are often chosen for their superior speed, and adaptive models
when smaller sizes are priority.

It is [possible](http://cbloomrants.blogspot.com/2012/10/10-02-12-small-note-on-adaptive-vs.html)
to achieve stronger compression ratios with static models, as well as speed up adaptive models
but this choice doesn't affect the fundamental problems that need to be solved, and that this article attempts to tackle.  
Note: static models also allow for faster entropy coding (see [Huffman](https://en.wikipedia.org/wiki/Huffman_coding) and
[tANS](https://en.wikipedia.org/wiki/Asymmetric_numeral_systems#Tabled_variant_(tANS))).

## Context vs history

Let's take a look at how one might implement a bitwise model.
-> why bitwise

![Futurama "show me the code" meme](futurama-show-me-the-code.png)

```rust
let ctx = hash(&history);
```

---

# TODO:

From a compressor's POV, at any given point in the data, we have direct access to the history
of all previously processed symbol.
At any point in the file this history is unique (for one. it's of different length).  
To get rid of the noise, we apply some lossy compression, just like the brain:
```rust
let ctx = hash(history);
```

We call this function `hash()` because it must behave much like a hash function does:
- it's deterministic (for decompression to work)
- it distributes evenly across the context space
- it's fast to compute

In practice we may use something as simple as the last 2 bytes.  
In the compression world, this is referred to as a prefix model (also order-n model).

<details>
<summary>Sidenote on order-n models</summary>

Compressors started out as byte-wise processors and order-n meant
having knowledge of the last n bytes:

```rust
fn order0(_: &[u8]) -> usize {
    0 // or any static integer
}

fn order1(history: &[u8]) -> usize {
    history.last().into()
}
```

Nowadays, strong CR (compression ratio) compressors are bitwise predictors due to ease of
storing and manipulating bit distributions, and simplified entropy coding.

When people wrote bitwise models with 8-bit context, it became ambiguous what to call them.
Do we follow the convention of n representing number of symbols knowledge, or do we exclusively use
bytes?  
Since 8-bit context for bitwise models most closely resemble order-0 bytewise models,
the convention is to call them order-0.

But what do we call a 12-bit context in a bitwise model?  
I'd encourage being more verbose in such situations and specifying bitwise vs bytewise coding (vs even nibblewise coding)
and exact number of bits in context.
</details>

In practice, we don't usually keep the whole history if we're only gonna use the last two bytes.
It's simpler to update the context as we go:

```rust
// Bytewise order-2 model
const CTX_SIZE: u32 = 1 << 16;
struct Model {
    ctx: u16,
    stats: [Counter; CTX_SIZE]
}

impl Model {
    fn new() -> Self {
        Self { ctx: 0, stats: [Counter::new(); 1 << 16] }
    }

    fn predict(&self) -> Prediction {
        self.stats[usize::from(self.ctx)].predict()
    }

    fn update(&mut self, byte: u8) {
        self.stats[usize::from(self.ctx)].update(symbol);
        self.ctx = (self.cts << u8::BITS) | u16::from(byte);
    }
}
```

From `/data/book1` let's look at when `ctx = "th"`:

<pre>{{ aux_data(path="content/tech/compression/fsm/aux/book1-th-annotated") }}</pre>

Nasty! Who could've predicted this many matches, given `the` is the most common word in the English language.

Let's just consider the symbols to be predicted:

<pre>{{ aux_data(path="content/tech/compression/fsm/aux/book1-th-postfixes") }}</pre>

In fact, let's look at my python script:

```python
{{ aux_data(path="content/tech/compression/fsm/aux/script.py") }}
```

A simple acceptor might look like this:
<img src="graph1.svg">


Get the counts:

<pre>
22 * <em>0x74_68<span class="s"> </span><span>0110_0101</span></em>
02 * <em>0x74_68<span class="s"> </span><span>0110_0001</span></em>
01 * <em>0x74_68<span class="s"> </span><span>0110_1001</span></em>
01 * <em>0x74_68<span class="s"> </span><span>0110_1111</span></em>
</pre>

In bits:

<pre>
22 * <em>0x74_68<span class="s"> </span><span>0110_0101</span></em>
02 * <em>0x74_68<span class="s"> </span><span>0110_0001</span></em>
01 * <em>0x74_68<span class="s"> </span><span>0110_1001</span></em>
01 * <em>0x74_68<span class="s"> </span><span>0110_1111</span></em>
</pre>

we can conclude:

$$
\forall i \in \{0, 1, 2, 3\}, \quad
P(bit_i = 6_i \mid ctx) = 1
$$

$$
P(bit_5 \mid ctx) = \frac{12}{13}, \quad
P(bit_6 \mid ctx) = \frac{23}{26}
$$

but

$$
P(bit_6 \mid ctx, bit_5 = 1) = \frac{1}{2}, \quad
P(bit_6 \mid ctx, bit_5 = 0) = \frac{11}{12}
$$

## Choosing a good context

-> decorrelation
-> BWT as a decorrelator
-> entropy hashing
-> spatial compression

## References

- secondary models: <https://encode.su/threads/3594-CM-design-discussion?p=69103&viewfull=1#post69103)>
- text is high order: <https://encode.su/threads/3594-CM-design-discussion?p=69106&viewfull=1#post69106>

