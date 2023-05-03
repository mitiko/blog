+++
title = "Huffman coding"
date = 2023-05-04

[extra]
math = true
+++

Huffman coding is an algorithm for devising the optimal prefix code for
a set of symbols with a particular probability distribution.?

![David Huffman holding origami](david-huffman.jpg)

- What
- Why
- Shannon Fano and prior work
- Story
- Optimality
- AC, patents

## Coding it

<!-- TODO - a bunch -->
I have reviewed a [bunch][1] of crates that are doing Huffman coding in Rust.
Most use some sort of custom sort and a custom arena allocators.
Rust is a pretty [bad idea][2] for a tree algorithm tbh.

<!-- is balanced the right word -->
Binary trees usually have optional children nodes, but huffman trees are always
balanced, and we do not require such functionality.

```rust
enum HuffmanTree {
    Leaf(u8, u32), // byte, count
    Node(Box<HuffmanTree>, Box<HuffmanTree>),
}
```

Let's think about the interfaces for a second here.
We want to construct a tree from a frequency/counts table, then convert it to a
table, then encode or decode with that table.

```rust
impl HuffmanTree {
    fn from_table(table: &[u32; 256]) -> Self {
        todo!()
    }
}
```

First we must initialize our leafs.
Easy enough. We want to skip non-occuring bytes. In practice, we always want to
account for the possibility that a byte doesn't occure, but we're building the
model statically and it will only be used to compress the data source that
generated it.

```rust
fn from_table(table: &[u32; 256]) -> Self {
    let nodes: Vec<_> = table
        .iter()
        .enumerate()
        .filter(|&(_, &count)| count > 0)
        .map(|(i, count)| (u8::try_from(i).unwrap(), count))
        .map(|(byte, &count)| HuffmanTree::Leaf(byte, count))
        .collect();

    todo!()
}
```

Well, at any given time, we want to have the last two (least common) nodes,
and merge them together. we can sort this `Vec` each time, or we could just use
a binary heap. All we need to do is implement `std::cmp::Ord` for `HuffmanTree`
to tell it how to sort its elements.

We want to sort by the sum of all children in a node, so let's implement that
first quickly. Just a recursive DFS will do the trick, our tree isn't growing
too big.

```rust
impl HuffmanTree {
    fn get_count(&self) -> u32 {
        match self {
            HuffmanTree::Leaf(_, count) => *count,
            HuffmanTree::Node(left, right) => left.get_count() + right.get_count(),
        }
    }
}
```

We're also required to implement `PartialOrd`, `PartialEq`, `Eq`, which are
trivial and can be auto-derived, except `PartialOrd` which has a slightly
different default implementation that doesn't rely on `Ord`.

```rust
#[derive(PartialEq, Eq)]
enum HuffmanTree { /* ... */ }

impl Ord for HuffmanTree {
    fn cmp(&self, other: &Self) -> std::cmp::Ordering {
        self.get_count().cmp(&other.get_count())
    }
}

impl PartialOrd for HuffmanTree {
    fn partial_cmp(&self, other: &Self) -> Option<std::cmp::Ordering> {
        Some(self.cmp(other))
    }
}
```

Now we can just collect the leafs in a binary heap:

```rust
fn from_table(table: &[u32; 256]) -> Self {
    use std::collections::BinaryHeap;
    let mut heap: BinaryHeap<_> = table
        .iter()
        .enumerate()
        .filter(|&(_, &count)| count > 0)
        .map(|(i, count)| (u8::try_from(i).unwrap(), count))
        .map(|(byte, &count)| HuffmanTree::Leaf(byte, count))
        .collect();

    todo!()
}
```

However, rust's standard library uses a max binary heap by default. No worries,
we can just reverse the comparison function:

```rust
impl Ord for HuffmanTree {
    fn cmp(&self, other: &Self) -> std::cmp::Ordering {
        self.get_count().cmp(&other.get_count()).reverse()
    }
}
```

Now we can fill in the actual algorithm:

```rust
fn from_table(table: &[u32; 256]) -> Self {
    /* ... */
    while heap.len() >= 2 {
        todo!()
    }

    heap.pop().unwrap()
}
```

We'll loop over the elemenets and merge them one by one until only one root node
remains. Something like:

```rust
fn from_table(table: &[u32; 256]) -> Self {
    /* ... */
    while heap.len() >= 2 {
        let left = heap.pop().unwrap();
        let right = heap.pop().unwrap()
        heap.push(HuffmanTree::Node(Box::new(left), Box::new(right)))
    }

    heap.pop().unwrap()
}
```

Awesome, that should do it!


## Sources

- https://github.com/Treeniks/huff_rs
- https://github.com/sagalasan/huffman-rust
- https://github.com/edg-l/rustyman/
- https://github.com/beling/bsuccinct-rs
- https://github.com/WanzenBug/huffman_coding

[1]: https://github.com/niklasf/rust-huffman-compress/
[2]: https://rust-unofficial.github.io/too-many-lists/
