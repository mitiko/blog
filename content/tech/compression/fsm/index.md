+++
title = "Compressing Data With Entirely Too Many FSMs"
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

We've [established](@/tech/compression/introduction.md) that the problem of optimal compression mostly
boils down to good predictors. The better the predictions, the better the compression ratio.  
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

Where \\(\text{history} = (x_0, ..., x_{n-1})\\) is a list of the previously encountered symbols and
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

![Futurama "show me the code" meme](futurama-show-me-the-code.png)

## Context, History and Counters

Let's take a look at how one might implement a model.  
With the above definitions, you may be tempted to write something like:

```rust
use std::collections::VecDeque;

struct Model {
    // Basically a ring buffer
    history: VecDeque<Symbol>,
    stats: Vec<Counter>,
}

impl Model {
    fn new() -> Self { todo!() }
    fn predict(&self) -> Prediction {
        // context is often shortened to ctx/cxt
        let ctx = hash(&self.history);
        self.stats[ctx].predict()
    }

    fn update(&mut self, sym: Symbol) {
        let ctx = hash(&self.history);
        self.stats[ctx].update(sym);

        self.history.pop_front();
        self.history.push_back(sym);
    }
}

fn hash(history: &VecDeque<Symbol>) -> usize { todo!() }
```

To store statistics we use counters. Imagine this as an abstract storage type for now,
we'll get into how to implement one in a minute.

This code is ~~bad~~ un-ergonomic for two reasons.  
**First**, in state of the art compressors, the main model used for prediction is actually a mix of many sub-models.
If each sub-model held its own copy of the history, that'd be very memory inefficient; and for strong compressors
we'd like to allocate as much memory as possible to holding statistics (more sub-models = better compression).  
**Second**, good counters are really *really* hard to implement for multi-symbol alphabets.
Predictions also tend to be hard to quantize well (which directly impacts compression ratios).
Entropy coders ([rANS](https://en.wikipedia.org/wiki/Asymmetric_numeral_systems#Range_variants_(rANS)_and_streaming),
[AC](https://en.wikipedia.org/wiki/Arithmetic_coding), [RC](https://en.wikipedia.org/wiki/Range_coding))
require computing the [CDF](https://en.wikipedia.org/wiki/Cumulative_distribution_function) for the symbol to be coded
and often the total to be \\(2^n\\) for divisionless coding.

Although, there're various ingenious tricks ([mixing CDFs](https://fgiesen.wordpress.com/2015/02/20/mixing-discrete-probability-distributions/),
[precomputing divison tables](https://github.com/rygorous/ryg_rans/blob/master/rans_byte.h#L180-L195),
[vector decoding CDFs](https://encode.su/threads/3542-AVX2-nibble-decoding-(SIMD-horizontal-scan)))
to get around a lot of the issues, bitwise coding offers more simplicity without sacrificing too much speed.  
The bottleneck of strong compressors is memory latency (cache misses on hashtable context lookups) not entropy coding.

Instead, [without loss of generality](https://en.wikipedia.org/wiki/Without_loss_of_generality) (for our purposes),
let's consider the binary case. To further simplify and give a general idea of what a context looks like,
let's write a prefix model.

Prefix models take the last n bytes of the history as context. Such models are also called order-n models
(you may even see them referred to as o1, o2, etc). Here's the simplest order-2 bitwise model:

```rust
struct Model {
    ctx: u16,
    stats: Vec<Counter>
}

impl Model {
    fn new() -> Self { todo!() }
    fn predict(&self) -> u16 {
        self.stats[ctx].predict()
    }

    fn update(&mut self, bit: u8) {
        self.stats[ctx].update(bit);
        self.ctx = (self.ctx << 1) | u16::from(bit);
    }
}
```

Prefix models are really easy to write because of how simple the *context function* is.
This one still suffers from not being byte-aligned but we'll fix that later, let's run it now.

Here's a highlight of `/data/book1` (very common test file) from the [Calgary corpus](http://www.data-compression.info/Corpora/CalgaryCorpus/)
when `ctx = "th"`:

<pre>{{ aux_data(path="content/tech/compression/fsm/aux/book1-th-annotated") }}</pre>

Awesome! It's expected we see a lot of matches for `th` since `the` is the most common word in the English language.
Let's take a look at the actual symbols to be predicted:

<pre>[th]: {{ aux_data(path="content/tech/compression/fsm/aux/book1-th-postfixes") }}</pre>

It's mostly `eee`-s.  
Let's take a look at another, how about `ctx = "im"`:

<pre>{{ aux_data(path="content/tech/compression/fsm/aux/book1-im-annotated") }}</pre>

This one's not as common and the symbols that follow are much more diverse.

<pre>[im]: {{ aux_data(path="content/tech/compression/fsm/aux/book1-im-postfixes") }}</pre>

It's precisely the counter's responsibility now to model these *postfixes*.  
So how does a counter look like?

```rust
// equivalent to interface/template in other languages
trait CounterTrait {
    fn new() -> Self;
    fn predict(&self) -> u16;
    fn predict(&mut self, bit: u8);
}
```

Notice how it has exactly the same methods as a model! That's the hack of it!  
We can (almost) plug any ordinary predictor in here and model the *postfixes*.

The data compression community doesn't exactly have a very good definition of what a **history**,
a **context**, a **counter**, or these *postfix symbols* are. We call them that based on how
they're used, much like any other naturally evolving word in a language.

So let me introduce a bit of a formal definition.
![A formally dressed frog](formal-frog.jpg)

## Levels of history

The key here is that these so-called *postfix symbols* are a history of their own.

We previously defined \\(\text{history}\\) as the list of all previously processed symbols.  
We also defined \\(\text{context}\\) to be the output of a hash-like function
\\(h: \mathcal{S}^* \rightarrow \mathcal{C}\\) which maps histories to contexts.
We may also call this function the **context function**.

We'll go on to define a class of histories \\(\mathcal{L} = \\{ l_i \\}\\) at each level \\(i\\).  
We define the 0-th level of history to be the list of symbols up to the point we've processed,
just like our previous definition of \\(\text{history}\\).  
Note, it is implicitly assumed we've processed \\(n\\) symbols so far.

$$
l_0 = (x_0, x_1, ..., x_n)
$$

To further continue, we must define \\(\text{data}\\) to be the (possibly infinite) list of all symbols.
$$
\text{data} = (x_0, x_1, x_2, ...) = \\{ x_t \mid x_t \in \mathcal{S} \\}_{t \in \N}
$$

We'll also define an indexing operation on this list:
$$
\text{data}[t] = x_t
$$

Another important function, gives us the prefixes of a list:
$$
\text{prefixes}(l_0) = \\{(), (x_0), (x_0, x_1), ..., l_0\\}
$$

maybe even
$$
l_1 = \\{ \text{data}[\text{length}(p)] \mid p \in \text{prefixes}(l_0),\ h(p) = h(l_0) \\}
$$

Then for an indexing operator on histories:
$$
l_i[r] = x_{j_r},
$$

$$
l_i = \\{ x_{j_0}, x_{j_1}, x_{j_2}, ..., x_{j_k} \\}
$$

We may inductively define
$$
l_{i+1} = \\{ l_i[\text{length}(p)] \mid p \in \text{prefixes}(l_i),\ h(p) = h(l_i) \\}
$$

---
# Not finished...

-> bits pred
-> fix ctx (o0 align)


Let's take a look at another, how about `ctx = "oo"`:

<pre>{{ aux_data(path="content/tech/compression/fsm/aux/book1-oo-annotated") }}</pre>

That's a lot less matches, but the symbols we ought to predict 

Nasty!


[X] bitwise?
[ ] bitwise sliding (8 steps) instead of 1
0001_1000 0110_1001
----t---- ----e----
[ ] ctx = hash(&history) -> you have direct access to history, but it's easier to just propagate the symbol update to submodels?
[ ] list of postfixes = level 1 history
[ ] context is just a hash of history, aka l0 context, l0 history
[ ] history & context are assumed to be l0 if not specified
[ ] symbol update vs direct access is crucial actually
[ ] fsms for symbol updates
[ ] reinforce binary vs bytewise
[ ] counter
[ ] no l0 counter, or order0 doesn't use history at all
[ ] differences between order0 and order1, and prefix models in general
[ ] GDCC's T5 (Shielwen) competition
 -> variant 1) better l0 context with fixed l1 counter
 -> variant 2) better l1 context with fixed l0 context hash/function
[ ] introduce APMs
[ ] history, context, context function, counter, APM/SPM



```rust
let ctx = hash(&history);
```


-> why bitwise


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

## The an variant

<pre>{{ aux_data(path="content/tech/compression/fsm/aux/book1-an-annotated") }}</pre>

And the postfixes:

<pre>{{ aux_data(path="content/tech/compression/fsm/aux/book1-an-postfixes") }}</pre>


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

