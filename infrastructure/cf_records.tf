resource "cloudflare_record" "main" {
  zone_id = local.zone_id
  name    = "mitiko.xyz"
  type    = "CNAME"
  proxied = true
  content = cloudflare_pages_project.main.subdomain
}

import {
    to = cloudflare_record.main
    id = "b1df4c83881b1414bff6c99c5bc9b31e/6c7dc3c74ceeaece9a1334edb0d82d84"
}
