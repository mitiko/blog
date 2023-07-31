+++
title = "Prefix codes"
date = 2023-07-30
+++

Assuming you've read my Huffman post or know enough about Huffman coding.

Ok.

Huffman codes are optimal prefix codes for a given distribution of symbols,
however optimality incurs a cost - unlimited code length.

The fix? Package-Merge!

- variable length codes
- uniquely decodeable codes
- prefix codes
- kraft's inequality
- Huffman codes
- canonical Huffman codes


## Rules

What are prefix codes?
No code is a prefix of any other code. This makes variable length codes uniquely
decodable.

variables codes -> uniquely decodable codes -> prefix codes

Package-Merge gives us the optimal length-limited codes while other techniques
compensate optimality with simplicity & speed.

Each prefix code can be represented uniquely by a binary tree.
And each normalized binary tree can be mapped to a prefix code.

### Kraft's inequality

Kraft's inequality gives a necessary and sufficient condition for the existence
of prefix codes for given codeword lengths. Equality means optimality.

- proof
- implications

### Canonical Huffman

A Huffman code that is describable only by the codeword lengths.
Makes it easier to store & manipulate.
Each Huffman code can be permutated to its canonical form.

### Speed

There are two main ways of producing length-limited prefix codes:
- through Huffman reduction(s)
- by construction (Package-Merge)

Any set of codeword lengths that conforms to Kraft's inequality will produce at
least one prefix code.
Since most algorithms use Kraft's inequality (either directly or indirectly)
it's more useful to hold the codeword lengths rather than specific codes.
Thus algorithms that first construct the Huffman code may convert it to its
canonical form, then do optimization passes.

## 

## Package-Merge

Let's start by implementng
