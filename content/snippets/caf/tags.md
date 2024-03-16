+++
title = "[refactor] Tags"
date = 2023-11-27
extra.exclude_meta = true
+++

```terraform
locals {
  tags = var.global_settings.inherit_tags ? merge(
    var.global_settings.tags,
    try(local.resource_group.tags, null),
    try(var.settings.tags, null)
  ) : try(var.settings.tags, null)

  # resource_group = local.remote_objects.resource_groups[...]
}
```

Don't forget to link the [resource group](@/snippets/caf/resource_groups.md).  
Tags are overridable by default.

### Usage:

```hcl
tags = local.tags
```
