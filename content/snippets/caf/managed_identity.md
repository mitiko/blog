+++
title = "Managed identity support"
date = 2023-11-27
extra.exclude_meta = true
+++

Define the remote_objects in `<module_definition>.tf`:

```terraform
module "<some_module>" {
  source   = "<some_folder>"
  for_each = local.some_object

  remote_objects = {
    managed_identities = local.combined_objects_managed_identities
  }
}
```

<!-- TODO: Copy button for snippet + file name -->
Add the following in `managed_identities.tf`:

```hcl
locals {
  managed_local_identities = flatten([
    for managed_identity_key in try(var.settings.identity.managed_identity_keys, []) : [
      var.remote_objects.managed_identities[var.client_config.landingzone_key][managed_identity_key].id
    ]
  ])

  managed_remote_identities = flatten([
    for lz_key, value in try(var.settings.identity.remote, {}) : [
      for managed_identity_key in value.managed_identity_keys : [
        var.remote_objects.managed_identities[lz_key][managed_identity_key].id
      ]
    ]
  ])

  provided_identities = try(var.settings.identity.managed_identity_ids, [])

  managed_identities = concat(local.provided_identities, local.managed_local_identities, local.managed_remote_identities)
  # optionally, use the first identity as the preferred identity
  # preferred_identity = try(var.settings.identity.type, "") == "UserAssigned" || try(var.settings.identity.type, "") == "SystemAssigned, UserAssigned" ? local.managed_identities[0] : null
}
```

Then use the identity in a dynamic block like so:

```hcl
dynamic "identity" {
  for_each = can(var.settings.identity) ? [1] : []

  content {
    type         = var.settings.identity.type
    identity_ids = local.managed_identities
  }
}
```

TODO: optional validation block

### Usage

With a system assigned identity:

```hcl
identity = {
  type = "SystemAssigned"
}
```

With local managed identities:

```hcl
identity = {
  type                  = "UserAssigned"
  managed_identity_keys = ["<managed_identity_key_01>", "<managed_identity_key_02>"]
}
```

Combined:

```hcl
identity = {
  type                  = "SystemAssigned, UserAssigned"
  managed_identity_keys = ["<managed_identity_key_01>", "<managed_identity_key_02>"]
}
```

With remote identities:

```hcl
identity = {
  type   = "UserAssigned"
  remote = {
    # must be the same as the lz_key of where the idenity has been defined
    level3_non_prod = {
      managed_identity_keys = ["<managed_identity_key_01>"]
    }
    level3_pre_prod = {
      managed_identity_keys = ["<managed_identity_key_02>"]
    }
  }
}
```

Don't forget to add the tfstate file reference!
<!-- TODO: Link to snippet -->


