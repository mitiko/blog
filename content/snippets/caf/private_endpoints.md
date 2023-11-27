+++
title = "Pending private endpoints module refactoring"
date = 2023-11-27
extra.exclude_meta = true
+++

Maybe released in 5.8.1

```bash
rg private_endpoints -l --line-buffered | awk -F "/" '{print $NF}' | sort -u | rg -e \.tfvars$
```
