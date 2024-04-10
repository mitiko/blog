+++
title = "Plan"
date = 2024-04-10
+++

BDD tests for management plane - API v0.1
Implement KV in rust, no optimizations. Management server in .NET

Priority list of tasks:
- naming convention
- resource rename support
- functionality
  - put (insert & update new entry)
  - get (fetch entry)
  - find (simple linear search for now)
- properties
  - total entries
  - number of get ops
  - number of put ops
  - number of find ops
  - pricing
  - total space usage
- terraform resource
- migration
  - region change
  - version upgrade

Stack:
- management plane API & server: dotnet (kestrel)
  - return toml by default?
  - return json when header set
- data plane API & resource: rust
- terraform provider: Go (go client)
- networking
  - docker-compose for now
