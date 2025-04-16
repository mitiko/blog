resource "cloudflare_pages_project" "main" {
  account_id        = local.account_id
  name              = "blog"
  production_branch = "main"

  build_config {
    build_command   = "asdf plugin add zola https://github.com/salasrod/asdf-zola && asdf install zola $ZOLA_VERSION &&  asdf global zola $ZOLA_VERSION && zola build"
    destination_dir = "public"
  }

  source {
    type = "github"

    config {
      owner             = "mitiko"
      repo_name         = "blog"
      production_branch = "main"

      # add comments to PRs?
      preview_deployment_setting = "custom"
    }
  }

  deployment_configs {
    preview {
      usage_model        = "standard"
      compatibility_date = "2024-09-02"
      fail_open          = true # no origin in backend
      environment_variables = {
        "ZOLA_VERSION" = local.zola_version
      }
    }
    production {
      usage_model        = "standard"
      compatibility_date = "2024-09-02"
      fail_open          = true # no origin in backend
      environment_variables = {
        "ZOLA_VERSION" = local.zola_version
      }
    }
  }

  lifecycle {
    ignore_changes = [
      build_config[0].web_analytics_tag,
      build_config[0].web_analytics_token,
    ]
  }
}

resource "cloudflare_pages_domain" "main" {
  account_id   = local.account_id
  project_name = cloudflare_pages_project.main.name
  domain       = "mitiko.xyz"
}

import {
  to = cloudflare_pages_project.main
  id = "271d70c872fc142477a92de255c0a75a/blog"
}

import {
  to = cloudflare_pages_domain.main
  id = "271d70c872fc142477a92de255c0a75a/blog/mitiko.xyz"
}
