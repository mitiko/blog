+++
title = "Introduction"
date = 2022-10-24
draft = true
template = "sections/todo.html"

[extra]
katex = true
+++

There are three parts of any compression algorithm:
- Decoupling - making symbols independent
- Probability estimation - predicting future symbols
- Encoding - transforming symbols & their probabilites into bits

It's hard to draw the line at what counts as a decoupler & what counts as
an estimator, so those two are often merged into a single model.

Where we have the following spaces:
- \\(\mathcal{A}^*\\) - observed history
- \\(\mathcal{C}\\) - context space
- \\(\mathcal{S}\\) - counter/state space
- \\(\mathcal{P}\\) - probability space

And the functions that map between them:
- \\(f: \mathcal{A}^* \rightarrow \mathcal{C}\\) - context function
- \\(s: \mathcal{C} \rightarrow \mathcal{S}\\) - \[context\] lookup function
- \\(p: \mathcal{S} \rightarrow \mathcal{P}\\) - probability mapping

Each of these on its own does a sort of [lossy compression](https://en.wikipedia.org/wiki/Lossy_compression) on its input.