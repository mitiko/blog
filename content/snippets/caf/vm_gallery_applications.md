+++
title = "[config-drift] VM gallery applications"
date = 2023-11-27
extra.exclude_meta = true
+++

Paste the following snippet:

```hcl
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

Then re-order the applications in the order that they appear in the plan.  
Rename `qualys = {`, `kace = {`, `crowd_strike = {` to be `app_01`, `app_02`,
`app_03`

> WARNING: The policy to enable gallery applications only runs once on initial
> VM creation.
