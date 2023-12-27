+++
title = "mitiko"

[extra]
tree = true
+++

Hi, this is my corner of the internet.

```bash
# WIP
alias mitiko="Dimitar Rusev"
```

This site is built with [Zola](https://getzola.org), and hosted on [Cloudlfare Pages](https://pages.cloudflare.com/).

## Sitemap

<nav>

[home](@/_index.md)
- [tech articles](@/tech/_index.md)
  - [compression](@/todo/_index.md)
- [favs](@/favs/_index.md)
  - [music](@/music/_index.md)
  - [movies](@/favs/movies/_index.md)
- [lore](@/lore/_index.md)
</nav>

## About

### Contact

You can email me at <a id="email">email obfusctated by js</a>.


<script>
// obfuscate email so it's harder on the web crawlers
const rot13 = (str) => str.replace(/[a-z]/gi, x => String.fromCharCode(x.charCodeAt(0) + (x.toLowerCase() <= 'm' ? 13 : -13)));
let obfsName = "zvgvxbqri";
let addr = rot13(obfsName) + "@" + "gmail.com";
let emailEl = document.getElementById("email");
emailEl.innerText = addr;
emailEl.href = "mailto:" + addr;
</script>

