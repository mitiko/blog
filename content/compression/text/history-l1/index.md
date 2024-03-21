+++
title = "L1 History"
date = 2024-03-16

[extra]
math = true
+++

There's a common concept in high-end compressors that has been given various
names <sup>[\[1\]][1] [\[2\]][2] [\[3\]][3]</sup> in different contexts but
refer to the same principle:  
**Indirection allows adaptivity and decorrelation improves compression.**

Text follows a non-stationary distribution. But entropy gives us the lower bound
for stationary sources only. We can use decorrelation techniques (in the case of
text - BWT, context modeling, etc) to extract a bitstream which has a
distribution closer to stationary. It means selecting symbols to be encoded
under the same context/presumption, under a stationary distribution.

{% note() %}
I'll be talking about bitwise models but these techniques apply for any
size symbol alphabet. Examples are for a bytewise alphabet for readability.
{% end %}

{% warning() %}
Heavy abuse of math notation ahead
{% end %}

Consider the entropy of book1.

$$
H(X) = - \sum_{x \in X}{p(x) \log p(x)}
$$
$$
H(\text{book1}) = 
$$

And now consider th entropy of just the symbols following a `th` _context_.

$$
H(X_{th}) = - \sum_{x \in X_{th}}{p(x) \log p(x)}
$$


```
{{ data(path="@/compression/text/history-l1/aux/book1") }}
```

## Mathematical theory

Unless otherwise stated

We know how to build stationary models:

```rust
use helper::{histogram, quantize};

struct StationaryBytewiseModel {
    distribution: [u32; 256],
}

impl StationaryBytewiseModel {
    pub fn new(buf: [u8; 256]) {
        let counts = histogram(buf);
        let distribution = quantize(counts, 1 << 31);
        Self { distribution }
    }

    pub fn predict(&self) -> &[u32; 256] {
        self.distribution
    }
}
```

And you can make it adaptive by doing the counting at "runtime" instead of when
initializing the model:

```rust
use helper::quantize;

struct AdaptiveBytewiseModel {
    counts: [u32; 256],
}

impl AdaptiveBytewiseModel {
    pub fn new() -> Self {
        Self { counts: [0; 256] }
    }

    pub fn update(&mut self, byte: u8) {
        self.counts[usize::from(byte)] += 1;
    }

    pub fn predict(&self) -> [u32; 256] {
        quantize(self.counts, 1 << 31)
    }
}
```

You can even make it bitwise:

```rust
// Example with no alignment for simplicity
struct BitwiseStationaryModel {
    probs: [u16; 256]
}

impl BitwiseStationaryModel {}
impl Model for BitwiseStationaryModel {}
```

</details>

Adaptivity is just a lookup to a stationary model.

One popular idea is that all symbols are a product of a very high order model.
This is certainly true - as we increase the sparsity of the context function,
the size of the L1 history bitsream approaches 1. This is practically what BWT
does too - it captures the symbol following the....

- Static model (entropy)
- Static model (bitwise) o8 = symbolwise o1
- Markovian property of bitwise models
- Adaptive models
- A counter is just a model for L1 history
- SSE is a way of including L0 history in the probability mapping of 

With entropy coding a solved problem models become functions like:
```
history up to a certain point -> probability
```

Probabilities don't need much more than 16 bits of precision.

[1]: https://mattmahoney.net/dc/dce.html#Section_413 "Indirect Models"
[2]: https://mattmahoney.net/dc/dce.html#Section_433 "SSE - Secondary Symbol Estimation"
[3]: https://mattmahoney.net/dc/dce.html#Section_434 "ISSE - Indirect SSE"
