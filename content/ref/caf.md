+++
title = "Azure Cloud Adaption Framework"
date = 2023-11-27
extra.exclude_meta = true
+++

Reference for Azure CAF, useful when refactoring.

## Common remote objects

Set variable in `<module>.tf`
```
remote_objects = {
  resource_groups      = local.combined_objects_resource_groups
  vnets                = local.combined_objects_networking
  private_dns          = local.combined_objects_private_dns
  keyvaults            = local.combined_objects_keyvaults
  keyvault_keys        = local.combined_objects_keyvault_keys
  application_insights = local.combined_objects_application_insights
  container_registries = local.combined_objects_container_registry
  storage_accounts     = local.combined_objects_storage_accounts
  managed_identities   = local.combined_objects_managed_identities
}
```

## Resource groups

Define locals in `<module>/main.tf`:
```
var.remote_objects.resource_groups[try(var.settings.resource_group.lz_key, var.client_config.landingzone_key)][try(var.settings.resource_group_key, var.settings.resource_group.key)]
resource_group_name = try(var.settings.resource_group_name, local.resource_group.name)
location            = can(var.settings.region) ? var.global_settings.regions[var.settings.region] : local.resource_group.location
```

## Tags

```
locals {
  tags = var.global_settings.inherit_tags ? merge(
    var.global_settings.tags,
    try(local.resource_group.tags, null),
    try(var.settings.tags, null)
  ) : try(var.settings.tags, null)
}
```

## Managed identities

Define locals in `<module>/managed_identities.tf`:
```
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

Usage (in module):
```
dynamic "identity" {
  for_each = can(var.settings.identity) ? [1] : []

  content {
    type         = var.settings.identity.type
    identity_ids = local.managed_identities
  }
}
```

Usage (in tfvars):
```
# system assigned identity
identity = {
  type = "SystemAssigned"
}

# local managed identities
identity = {
  type                  = "UserAssigned"
  managed_identity_keys = ["<managed_identity_key_01>", "<managed_identity_key_02>"]
}

# combined
identity = {
  type                  = "SystemAssigned, UserAssigned"
  managed_identity_keys = ["<managed_identity_key_01>", "<managed_identity_key_02>"]
}

# remote
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

## Private endpoints migration from main

```bash
rg private_endpoints -l --line-buffered | awk -F "/" '{print $NF}' | sort -u | rg -e \.tfvars$
```

## VM gallery applications

There's a policy which enables gallery applications on VM creation, and these
often need to be backfilled in. Make sure to put them in the right order as the
plan shows and rename them to `app_01`, `app_02`, `app_03` to keep the order the
same (this is different than the order property).
```
gallery_applications = {
  qualys = {
    order      = 0
    version_id = "/subscriptions/24e2024f-2621-4943-af06-7b1da03d289c/resourceGroups/rg-iac-ig-pr-eu2-01/providers/Microsoft.Compute/galleries/gimgiaccafpreu201/applications/Qualys_Ubuntu.Deb/versions/4.6.16"
  }
  kace = {
    order      = 0
    version_id = "/subscriptions/24e2024f-2621-4943-af06-7b1da03d289c/resourceGroups/rg-iac-ig-pr-eu2-01/providers/Microsoft.Compute/galleries/gimgiaccafpreu201/applications/Kace_Ubuntu.Deb/versions/12.1.52"
  }
  crowd_strike = {
    order      = 0
    version_id = "/subscriptions/24e2024f-2621-4943-af06-7b1da03d289c/resourceGroups/rg-iac-ig-pr-eu2-01/providers/Microsoft.Compute/galleries/gimgiaccafpreu201/applications/CrowdStike_Ubuntu.Deb/versions/6.31.14505"
  }
}
```
