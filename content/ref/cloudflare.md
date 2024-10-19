+++
title = "Cloudflare"
date = 2024-10-19
aliases = ["/ref/cf"]
+++

### Storing Terraform state in an R2 bucket

R2 is S3-compatible but you need to set it up properly to work with Terraform.

First, create an R2 bucket. I conveniently called mine `terraform`.  
Then, [create an R2 scoped token](https://dash.cloudflare.com/?to=/:account/r2/api-tokens).  
It's important to create a token from here, rather than a general API token as
this page will give you the secret key and access key to use for the S3 API.

```
terraform {
  required_providers {
    cloudflare = {
      source  = "cloudflare/cloudflare"
      version = "~>4.44.0"
    }
  }
  backend "s3" {
    bucket = "terraform"
    key    = "main.tfstate"

    endpoints  = { s3 = "https://<ACCOUNT_ID>.r2.cloudflarestorage.com" }
    region     = "auto"
    access_key = "<ACCESS_KEY>"
    secret_key = "<SECRET_KEY>"

    skip_credentials_validation = true
    skip_region_validation      = true
    skip_requesting_account_id  = true
    skip_metadata_api_check     = true
    skip_s3_checksum            = true
    use_path_style              = true
  }
}
```

It's also important to set the endpoint be `${account_id}.r2.cloudflarestorage.com`
as this is the only S3-compatible endpoint and custom domains will not work.

### Hosting on Cloudflare Pages

Configure infrastructure with Cloudflare Pages. First push afterwards will
trigger a deployment.

```
terraform {
  required_providers {
    cloudflare = {
      source  = "cloudflare/cloudflare"
      version = "~>4.44.0"
    }
  }
  # init with `tf init -backend-config=main.tfbackend`
  backend "s3" {}
}

variable "cloudflare_api_token" { sensitive = true }
provider "cloudflare" {
  api_token = var.cloudflare_api_token
}

locals {
  account_id = "271d70c872fc142477a92de255c0a75a"
  zone_id    = "b1df4c83881b1414bff6c99c5bc9b31e"
}

resource "cloudflare_pages_project" "main" {
  account_id        = local.account_id
  name              = "<PROJECT_NAME>"
  production_branch = "main"

  build_config {
    destination_dir = "dest/"
  }

  source {
    type = "github"

    config {
      owner             = "mitiko"
      repo_name         = "<REPO_NAME>"
      production_branch = "main"
    }
  }
}

resource "cloudflare_pages_domain" "main" {
  account_id   = local.account_id
  project_name = cloudflare_pages_project.main.name
  domain       = "<SUBDOMAIN>.mitiko.xyz"
}

resource "cloudflare_record" "main" {
  zone_id = local.zone_id
  name    = "<SUBDOMAIN>"
  type    = "CNAME"
  proxied = true
  content = cloudflare_pages_project.main.subdomain
}
```
