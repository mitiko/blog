+++
title = "Getting started"
date = 2022-08-22
draft = true

# [extra]
# subtitle = ""
+++

I've been wanting to start a blog for a while now, it's in every programmer's `TODO` wishlist.  
However, anxiety would often get to me, making me question what's the right platform to use,
what'll give me enough **flexibility** whilst also providing **stability**, ease-of-use, and **carefree** deployments.

One thing I knew, for sure, is I wanted to write my blog posts in <span class="highlight">markdown</span>.  
Back then, when I first got the idea, all I knew was some .NET and JS and it was shortsighted of me
to only consider server-based solutions, when in fact I needed (and this is what I ended up using) an **SSG** - static site generator.

## Static Site Generators

The purpose of an SSG is to give you templating without making you write html, or costing you a bunch of money for cloud compute.

A couple of the more popular ones include: Jekyll (GitHub pages' default), Hugo (written in Go), Gatsby, Eleventy, etc.  
In fact I came across this beautifully compiled list of them [here](https://jamstack.org/generators/).  
Apparently I stumbled upon some movement JAMstack (Javascript, API, Markup) - termed first coined by Mathias Biilmann, CEO of Netlify, as a common *architecture pattern*.

About 6 months ago I had started using Rust (due to rewriting a data compression project).  
There's some beef between Rust and Go for the crown of fastest, bestest, most modern language and that lead me to try out Hugo.

![HUGO logo](https://raw.githubusercontent.com/gohugoio/gohugoioTheme/master/static/images/hugo-logo-wide.svg)

Actually, I had this other side project as I was getting to know Hugo -
a website to hold my *drastically* pruned 12th grade literature notes before finals [lit12.top](https://lit12.top/).

I was very stressed before said exams and couldn't let myself relax enough to work on the blog;
or anything for that matter - I dropped everything for a week to revise in the classic teenage way I so desperately tried to prevent.  

Hugo seemed kinda wacky, like a hacked-up together project and there was also some friction with the GitHub actions I didn't enjoy having to deal with.  
I did learn two things from that experience, though:
1. I hate theme authors
2. I love the Inter font

Regardless of whether there was some negative reinforcement action at play or not, I switched to Zola - the rusty alternative ;)

```bash
$ mkdir -p ~/Documents/Projects/Web/blog
$ ln -s !$ ~/_blog && cd ~/_blog

$ zola init
$ code .
```

I like Zola much better. The doc is a bit all over the place because it's not really a doc but rather a guide.  
Whatever's not in there, I can usually find in the Tera docs - the templating engine used underneath (again written in rust).

## Hosting

I was hesitant to upload anything at first, because.. none of it is ready.  
But another important realization I had was that I'd never be quite happy with my blog -
it would remain being a WIP for a long time, never finished - [like fashion](@/movies/the-social-network-fashion.md).

<!-- TODO: Add an archive link to my first php script -->
Choosing a hosting platform is another one of those choices that you have to do.
In the past I've used [000webhost](https://www.000webhost.com/) just as I was starting to get into the webdev world
(somehow being convinced that since facebook was written in php I must use the same - that's maybe 2014-2015).

Since then, I've been a firm Github pages supporter as my code already gets version controlled and it's easy to get started.  
I have, however, had some issues with GitHub's bias towards Jekyll, particularly, using math in markdown gets messy.


What I've heard the cool kids use these days is Netlify. It's annoyingly simple to setup and I did it in no more than 5 minutes (+troubleshooting the zola version in the config).  
Thus, on the 13th of August at exactly 12:30, through an automatic Netlify deploy, my blog became a reality!

Netlify also has functions which might come in handy for some later more complicated applications.
Although, to be fair, I like the no-js aesthetic and zola's static/compile-time functions are quite powerful.
