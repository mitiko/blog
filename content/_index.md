+++
title = "mitiko"

[extra]
tree = true
+++

Hi, my name is **Dimitar Rusev** and this is my corner of the internet.

```bash
# online, my moniker is mitiko
alias mitiko="Dimitar Rusev"
```

This site is built with [Zola](https://getzola.org), and hosted on [Cloudlfare Pages](https://pages.cloudflare.com/).

## Sitemap

<nav>

[{{ color1(str="~/") }} home](/)
- [{{ color1(str="~/tech") }} articles](/tech)
  - [{{ color1(str="~/tech/compression") }} making things smol](/tech/compression)
- [{{ color1(str="~/favs") }} dopamine providers](/favs)
  - [{{ color1(str="~/favs/music") }} (lyrics included)](/favs/music)
  - [{{ color1(str="~/favs/movies") }} (rewatched 3+)](/favs/movies)
- [{{ color1(str="~/lore") }} non-ephemeral content](/lore)
</nav>

## About

### Contact

You can email me <a id="email">obfusctated by js</a>.


<script>
// obfuscate email so it's harder on the web crawlers
const rot13 = (str) => str.replace(/[a-z]/gi, x => String.fromCharCode(x.charCodeAt(0) + (x.toLowerCase() <= 'm' ? 13 : -13)));
let obfsName = "zvgvxbqri";
let addr = rot13(obfsName) + "@" + "gmail.com";
let emailEl = document.getElementById("email");
emailEl.innerText = addr;
emailEl.href = "mailto:" + addr;
</script>

