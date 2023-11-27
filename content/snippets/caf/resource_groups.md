+++
title = "[add] Resource groups & location"
date = 2023-11-27
extra.exclude_meta = true
+++

Define the remote_objects in `<module_definition>.tf`:

```terraform
module "<some_module>" {
  source   = "<some_folder>"
  for_each = local.some_object

  remote_objects = {
    resource_groups = local.combined_objects_resource_groups
  }
}
```

Define the locals:

```hcl
resource_group      = var.remote_objects.resource_groups[try(var.settings.resource_group.lz_key, var.client_config.landingzone_key)][try(var.settings.resource_group_key, var.settings.resource_group.key)]
resource_group_name = try(var.settings.resource_group_name, local.resource_group.name)
location            = can(var.settings.region) ? var.global_settings.regions[var.settings.region] : local.resource_group.location
```

### Usage:

Standard:

```hcl
resource_group_key = "<some_rg_reference>"
```

Remote landingzone:

```hcl
resource_group = {
  lz_key = "<some_lz_reference>"
  key    = "<some_rg_reference>"
}
```

Override location (by default inherits the resource group's):

```hcl
resource_group_key = "<some_rg_reference>"
region             = "ca_region1"
```

Explicitly name the resource group:

```hcl
resource_group_name = "<explicitly_the_rg_name>"
region              = "ca_region1"
```
