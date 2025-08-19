+++
title = "Text Compression"
+++

Mostly will be talking about high-CR algorithms.

```rust
pub trait Model {
    fn predict(&self) -> u16;
    fn update(&mut self, bit: u8);
}
```
