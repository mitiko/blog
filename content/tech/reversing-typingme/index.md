+++
title = "Reverse engineering 'typingme.com'"
date = 2023-01-04
draft = true

[taxonomies]
tags = ["hacking"]
+++

One of my 2023 resolutions is to learn to type with 10 fingers (and then learn vim).
A quick search for `typing with 10 fingers` and <https://typingme.com> ranks third on google.

I am immediately drawn to it, the design looks very 90-ish and functional.  
I test it out and bookmark it (this is happening on 29.12.2022). I then proceeded to
make an irresponsible (but totally worth it) financial decision of getting a [K380](https://www.logitech.com/en-eu/products/keyboards/k380-multi-device.html)
because the design is very sleek and I need to treat myself.

I'm currently on lesson 3 and it takes me about an hour of uninterrupted typing to pass each lesson.
While typing my mind often wanders off:

```
Hmm, I wonder if they collect stats on the mistakes you make?
They probably don't. Would be cool if they did though.
What if.. No! Focus!
This will take too much time, you're better off.. *gets focused again*
```

Of course, eventually, I gave in; *clearly*.

<!-- ## Step 1 - Look at the code -->
## Step 1. Look at the code

A quick `Ctrl+C` and hover over the start button.

```html
<button id="other" onclick="start()">Start Exercise</button>
```

Not much obfuscation - that's why I like the old internet.  
Time to find `start()`. Take a look at the sources tab, and search for js files.

```js
// file: new-starts-eng.js.pagespeed.ce.Ks7Z36XAVC.js

// ...
function start() {
    // ... <code omitted>
    for (var a = 0; a < 4; a++)
        txt(arson[a], artext[a]);
    // ... <code omitted>
    realStart(artext[0], arson[0], arilk[0])
}

artext = new Array;
arson = new Array("son0","son1","son2","son3");
arilk = new Array("ilk0","ilk1","ilk2","ilk3");
dmm = 0;
artext[0] = a.line0;
artext[1] = a.line1;
artext[2] = a.line2;
artext[3] = a.line3;
// ...
```

Tip: there's a prettify button in the bottom left corner of the code explorer.

Looks like there's might be some caching involved because of `.Ks7Z36XAVC.js`, or
that could have to do with [Pagespeed](https://pagespeed.web.dev/) - some google bloat.

The `realStart()` is just hilarious to me. Also [arson](https://en.wikipedia.org/wiki/Arson)
is a great variable name, I think.  
Enough mocking, let's try and understand the logic.

```js
// file: new-starts-eng.js.pagespeed.ce.Ks7Z36XAVC.js
function txt(a, b) {
    return hasInnerText ? document.getElementById(a).innerText = b : document.getElementById(a).textContent = b
}
```

Whoa, long line there. Refactor!  
(I also tried ChatGPT on this, and it sucked.)

```js
// file: new-starts-eng.js.pagespeed.ce.Ks7Z36XAVC.js
const txt = (a, b) => hasInnerText ?
    document.getElementById(a).innerText = b :
    document.getElementById(a).textContent = b;
```

This helper function sets the contents of an element. Exploring the DOM tree state while typing,
each line is divided in 2 parts: `"son{i}"` and `"ilk{i}"`. We compare the first character of the first buffer
with the currently typed character. If they don't match, show an error message. Otherwise, move it to the "done"
buffer.

Ok, cool, all fine, but I really wanna see how the words are generated.  
Well, we copy them here:

```js
for (var a = 0; a < 4; a++)
    txt(arson[a], artext[a]);
```

And we fill the `artext` array later below:

```js
artext[0] = a.line0;
artext[1] = a.line1;
artext[2] = a.line2;
artext[3] = a.line3;
```

But what the fuck is `a` in this context. It's nowhere to be found in this file.  
I worry it might be one of those [DOM clobbering](https://www.youtube.com/watch?v=dZXaQKEE3A8&ab_channel=LiveOverflow)
bad js scary stuff.

Well, `a` is available in the console even before we call `start()` (or `realStart()` for that matter).
Maybe it's hidden in some other global script.

Indeed.

```html
<head>
<!-- meta tags -->
<script type="text/javascript">
    // formatted :))
    var a = {
        "line0": "faff dd assss asa ssaas dsd ssds dsad asdf ssaa ",
        "line1": "sssa dasa dsd sfadf sfa dfss asss affs afdd fas ",
        "line2": "dda sddfs ssds ff fsd sda fsfs sfs fsdda da asdff ",
        "line3": "daa ddd dad ffs fsssa aafd ffd ddf ssf aad daf",
        "snippet1": "keyInput = e.key",
        "snippet2": "hasInnerText ? ilkId.innerText += keyInput : ilkId.textContent += keyInput"
    };
</script>
<!-- analytics and stuff -->
</head>
```

Ok, so just hardcoded, huh?

Fuck! Pay attention to the URL:  
https://typingme.com/touch-typing/typing-lesson-3.**php**  
It's a php page. This means, the words are probably generated serverside.

## Step 2. Research

At this point I turned to GitHub. Maybe the project is open source; perhaps it was
named something else before.

But then again.. - they run ads on it; that's a bad sign.

We find someone's [bookmarks](https://github.com/JimySheepman/TechStack/blob/9600bb0cbc21d1af551da4df81f1c0d133dd5f2c/bookmarks.md),
an [issue & PR](https://github.com/AdguardTeam/AdguardFilters/pull/80321) to and adblock blacklist repo,
and what is probably one of the strangest abandonned
[repositories](https://github.com/hitkon/OpenX2/blob/7a79873e21aae1d58c4035c23f6a1548e609e13c/Task1/json2/freegames66.com.json)
I've seen in a while, containing json-s for ads that someone is running / being paid to run?

Why would that be public? Maybe someone did an oopsie, but the internet is a wild place, who could really tell.
At least we get a name - Umit Batu. Time to follow the track.

Search for `"Umit Batu" github` and we get some turkish course [introduction](https://github.com/polatengin/polatengin.github.io/blob/master/_posts/2016-08-27-acikakademi-asp-net-mvc-ile-ileri-seviyede-web-programlama-ogrenmek-istiyorum-egitimi-2016.md)
where the author mentions Batu as his friend who helped him film it.
Funny, cause this is .NET and we're hoping for a PHP guy.

Also I now remember, some of the code has "mesaj", "yanlis", "saniye" which are the turkish
words for "message", "wrong", and "second". Maybe this is our guy after all.
I sent an email to his alleged friend - Engin Polat, and now I can only wait to find out.

Another connection between Polat and Batu is on [Medium](https://medium.com/@mitbatu), where they follow each other.
Ironically, his profile picture on there is a quote that reads:
"Remember that sometimes not getting what you want is a wonderful stroke of luck. - Dalai Lama."

Sure, let it be that way.

## Step 3. Scraping the words ourselves

If you think about it, this php page is really just an API with a lot of extra junk in it, we don't care about.
Let's query it up, write a parser, get the words, and reverse the algorithm to generate them.
Relevant xkcd:

![xkcd 1481 - websites are technically APIs](https://imgs.xkcd.com/comics/api.png)

At first I thought maybe it's a limited set. They seem so perfectly chosen when I'm doing an exercise
that I can foul myself they're stored in a database somewhere but if we involve
[Occam's razor](https://en.wikipedia.org/wiki/Occam%27s_razor), it's more likely a good random generator.

My weapon of choice is `curl`, and my second hand is always `grep`
(or [ripgrep](https://github.com/BurntSushi/ripgrep) really, cuz we love Rust):

```bash
curl -s https://typingme.com/touch-typing/typing-lesson-3.php | rg "var a=\{"
```

Great! Let's not build a lengthy one-liner though, we'll paly around with it a lot anyway.  
With a little help from [StackOverflow](https://superuser.com/questions/272265/getting-curl-to-output-http-status-code#862395)
we pull this magnificient snippet:

```bash
#!/bin/bash

lesson=$1
url="https://typingme.com/touch-typing/typing-lesson-$lesson.php"

# follow redirects, be quiet, write http status code
exec 3>&1 # create fd 3, which redirects to std out 1
status_code=$(curl -L -s -w "%{http_code}" -o >(cat >&3) $url)

# if status_code is 200...
```

Well, I'm not that good at bash, this was actually discouraging.  
I really need to keep a set of the words that we scrape (or so I thought) and
the only way I can think of to do that in bash would be `sort + uniq` (or `sort -u` as I later found out).

We turn to our savior - python.  
(I did [AOC2022](https://github.com/Mitiko/AOC2022) in python and learned to love it)

```py
#!/usr/bin/python3

import requests
import re

lesson = 3
url = f'https://typingme.com/touch-typing/typing-lesson-{lesson}.php'
resp = requests.get(url, headers=headers).text
print(resp)

# and then some regex magic
```

Oops, [403 Forbidden](https://en.wikipedia.org/wiki/HTTP_403). Cloudflare is catching our "bot".
Fuck, ok. How does it go through with curl though?

```bash
curl -v https://typingme.com/touch-typing/typing-lesson-3.php

> GET /touch-typing/typing-lesson-3.php HTTP/2
> Host: typingme.com
> user-agent: curl/7.81.0
> accept: */*
>
```

There's not a lot of headers. Is it *really* the user agent?

```py
headers = {
    'Connection': 'keep-alive',
    'User-Agent': 'curl/7.81.0', # emulate curl
    'Cache-Control': 'max-age=0', # pretend we're a fancy browser
    'Accept-Encoding': 'gzip, deflate, br', # whoo, compression!
}

url = f'https://typingme.com/touch-typing/typing-lesson-{lesson}.php'
resp = requests.get(url, headers=headers).text

# the words are stored in a script in the variable `a` as JSON
match = re.search(r'var a\s?=\s?(\{.+\});', resp)
```

We probably don't need all the headers but I feel like we're cheating the cloudflare detection system more this way.
I did come across this [module](https://github.com/VeNoMouS/cloudscraper) which bypasses cloudflare with many
more sophisticated mechanisms but if it works with just the requests, let's keep it lightweight.

Also, sidenote, the requests API for python has the best logo ever:
logo here
<!-- TODO: make this small -->
<!-- ![pyhton's request module logo](https://requests.readthedocs.io/en/latest/_static/requests-sidebar.png). -->

<!-- TODO: replace that link with my git commit where I fix that -->
However, I really dislike python's regex module. I mean, it's cool and all, but I always
prefer to do `findall()` instead of `match()`, and I completely forget `search()`.
It's good practice to use `search()` here, and an even better practice would be to
[compile the regex only once](@/todo/_index.md)
since we'll be doing many requests.

```py
def flatten(l):
    return [item for sublist in l for item in sublist]

import json

if match is not None:
    data = json.loads(match.groups()[0])
    lines = [data[f'line{i}'] for i in range(4)]
    words = flatten([line.strip().split(' ') for line in lines])
```

Now, put this in a function an collect all the unique words:

```py
def get_words(lesson):
    # ...
    return words

lesson = 3
all_words = set()

for _ in range(100):
    words = get_words(lesson)
    all_words |= set(words)
    print(len(all_words))
```

The count just keeps going up; at this point, I'm starting to realize, this is not a database.
Alright then, even cooler, let's get some statistics going and reverse the
sampling algorithm.

## Step 4. Reversing the sampling algorithm

