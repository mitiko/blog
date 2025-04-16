terraform {
  required_providers {
    cloudflare = {
      source  = "cloudflare/cloudflare"
      version = "~>4.44.0"
    }
  }
  # init with `tf init -backend-config=main.tfbackend`
  backend "s3" {
    bucket                      = "terraform"
    key                         = "blog.tfstate"
    endpoints                   = { s3 = "https://271d70c872fc142477a92de255c0a75a.r2.cloudflarestorage.com" }
    region                      = "auto"
    skip_credentials_validation = true
    skip_region_validation      = true
    skip_requesting_account_id  = true
    skip_metadata_api_check     = true
    skip_s3_checksum            = true
    use_path_style              = true
  }
}

provider "cloudflare" {
  api_token = var.cloudflare_api_token
}

locals {
  account_id = "271d70c872fc142477a92de255c0a75a"
  zone_id    = "b1df4c83881b1414bff6c99c5bc9b31e"
}

