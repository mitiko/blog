+++
title = "List of CAF tf and tfvars snippets"
sort_by = "date"
+++

Some common remote objects:
```terraform
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

## Snippets for CAF
