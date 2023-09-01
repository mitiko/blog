+++
title = "Receipts - auth"
date = 2023-08-21
+++

<!-- Intro about rolling your own auth with link to roll-your-own article -->
It's 21:50, and I've had a glass wine, let the hacking begin.
<!-- Insert scene from The Social Network -->

## Choosing a datastore

- many database options (expensive)
- very extensible

Cloudflare KV!!
- networking (private)

Limitations
- Keys are up to 512 bytes
  - SHA256 shall be good enough.
- Values are up to 25MiB
  - can even store images huh
- metadata can be up to 1024 bytes = 1KiB

- expiring keys by default

## Auth

first, let's store a user + password, and hash user + password
..
I was initially thinking sha256 will satisfy but apparently both terraform & the
rust worker support bcrypt, so we're using that.
the tf function bcrypt regenerates a new hash on every apply but I think that's
a rather good thing.
Except it's using 2a?b

We can fix that issue by limiting password length to 72 chars..

## Token generation

Now, that auth works, we need to generate expiring tokens



