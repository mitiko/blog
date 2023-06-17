+++
title = "Receipts"
date = 2023-05-31
+++

<!-- as of 2023 -->
Technically speaking the modern stack is on a [5$ VPS](https://uberspace.de/en/)
with either PHP, bash CGI, OCaml or a small .NET for backend and HTMX for
frontend.

But not to worry!
We've got serverless with cloudflare, terraform, htmy for frontend, and zola for
.. semi backend?

---

First we create a token for Cloudflare.
I named mine `receipts-r2` and gave it read/write access to Workers R2 Storage.
the interface wasn't the most intuitive but I figured it out rather fast and
it's a one-time job anyway.

I set an env (and make sure not to put it in the history)
```bash
 export CLOUDFLARE_API_TOKEN=0123456789abcdefghij0123456789abcdefghij
```

then we can test the provider

```HCL
terraform {
  required_providers {
    cloudflare = {
      source  = "cloudflare/cloudflare"
      version = "~> 4.7"
    }
  }
}

data "cloudflare_accounts" "mitiko" {
  name = "mitiko"
}

output "account" {
  value = data.cloudflare_accounts.mitiko.accounts
}
```

https://blog.cloudflare.com/getting-started-with-terraform-and-cloudflare-part-1/
Next we want to actually store the state in a bucket as well.

Choosing S3 because it's common. Might switch to D1 later.
Although Alpha is exactly where I should be.

