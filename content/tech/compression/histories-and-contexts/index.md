+++
title = "Histories and contexts"
# the world of FSMs in data compression
# !! compressing data with way too many FSMs
# # this isn't as much abt FSMs as it is about contexts and histories..
# History is (almost always) bound to repeat itself
date = 2022-11-15
draft = true

[extra]
katex = true
style = "styles/tech/ctx.css"
+++

<!-- Contexts, Histories article first?
Then Counters?
Then APMs? -->

Components of a predictive model:
![compression components](imgs/compression-components.png)

Genetic data from [E.coli](https://en.wikipedia.org/wiki/Escherichia_coli).

History:

<pre>
<span class="aux">n: <span class="count">0</span></span>
<span class="aux">next symbol: <span class="next"></span></span>
<p class="data">{{ aux_data(path="content/tech/compression/histories-and-contexts/aux/E.coli") }}</p></pre>

Context:

<pre>
<span class="aux">n: <span class="count">0</span></span>
<span class="aux">context: <span class="ctx"></span></span>
<span class="aux">next symbol: <span class="next"></span></span>
<p class="data">{{ aux_data(path="content/tech/compression/histories-and-contexts/aux/E.coli") }}</p></pre>

Level 1 history:

<pre>
<span class="aux">n: <span class="count">0</span></span>
<span class="aux">context: <span class="ctx"></span></span>
<span class="aux">next symbol: <span class="next"></span></span>
<span class="aux">level 1 hsitory: <span class="l1"></span></span>
<p class="data">{{ aux_data(path="content/tech/compression/histories-and-contexts/aux/E.coli") }}</p></pre>

<script src="history.js"></script>



