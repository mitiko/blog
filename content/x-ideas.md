+++
title = "Ideas"
date = 2024-11-07
+++

1. is Fantastico really that much more expensive (price comparison between stores)
2. is it actually cheaper to use disposable cutlery (lazy people perspective)
3. move REFERENCE.md to /ref/blog or /ref/md and /ref/latex
4. breadcrumbs for pages on blog
5. code styling & other themes?
6. D1 for bank-reports?

<!-- https://github.com/not-an-aardvark/lucky-commit/tree/00000002877d35de410890b322e3f76790706390?tab=readme-ov-file#why -->

## Services

Multiple options:

1. subdomain such as {{service}}.mitiko.xyz
2. tooling domain tools.mitiko.xyz/{{service}}
3. underscore path mitiko.xyz/_{{service}}

| Method     | Advantages                             | Disadvantages                                      |
| ---------- | -------------------------------------- | -------------------------------------------------- |
| subdomain  | <ul><li>can host anywhere</li></ul>    | <ul><li>need DNS access for new services</li></ul> |
| tooling    | <ul><li>common for all tools</li><li>new domain</li></ul> | <ul><li>sucks for non-HTTP</li><li>harder to bind when already part of blog</li></ul>               |
| underscode | <ul><li>common for all tools</li><li>differentiates from the rest of the blog</li></ul> | <ul><li>sucks for non-HTTP</li><li>harder to bind</li></ul>               |


### Permalinks

Use: <https://www.crockford.com/base32.html>  
Example: `https://mitiko.xyz/p/000` (15-bit permalink = 32'768 articles, 24 bytes total)

```
// instead of meta redirect pages by zola, I could use a CF function
// it will execute redirect using KV

// 308 redirect /ref/py to /ref/python (aka manage a list of redirects & keep the rest in KV)

// or kv.mitiko.xyz/someKey -> returns someValue
// this way we can return html meta redirect pages? or 307/308 responses?

// key scheme is URI of {{modifier}}:{{keyName}}
// for example permalinks = p, general = g or a or 0, deferred immutable pages = dip
// are / (slashes) allowed? do we use : (colon) instead?

// Cloudflare KV download to SQLite database

-> global file sync
-> distributed: CF cloud, mostly offline systems, backups & data???
```

### Deferred Immutable Pages

Generalte a shortlink such as https://mitiko.xyz/_dip/000 or https://kv.mitiko.xyz/dip:000.  
Again with the 15-bit base 32 id.

### QR codegen

Would be nice to have QR codes for permalinks or DIPs.  
I'd like a general purpose service to grab QR codes for any data + store QRs for my origin so they're fast to retrieve.

```
https://qr.mitiko.xyz/{{type}}?data={{html-encoded data}}
https://mitiko.xyz/_qr/{{type}}?data={{data}}
https://mitiko.xyz/_qr/text?data=hello%20world!
-> support encoding types = numeric, alphanumeric, bytes

check https://kv.mitiko.xyz/qr:{{base32}}
```

Research:

- <https://github.com/rxing-core/rxing-wasm/tree/main?tab=readme-ov-file>
- `cargo install rxing-cli`
- `rxing-cli help`

