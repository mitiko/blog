+++
title = "Next-Gen Cloud"
date = 2024-04-03
+++

Ideas for what an IaC-ready cloud would look like:

- terraform integration built in
  - OIDC for authenticating to public runners
  - remembering runner public ip access
  - documentation + terraform examples
  - resource names mutable
    - underneath, each resource has an immutable id (guid)
      - two types of ids: mutable & non-mutable
      - use mutable ids by default
      - refer & import immutable ids for terraform specific cases
    - if names follow convention, then name is tenant-unique identifier?
  - root account & infrastructure-operator account
  - each API call is a transaction
    - transaction has caller = actor = account id = guid
      - predictable guid for root account / operator account
    - each API request has required permissions listed
      - this makes permissions for a specific scenario fully computable
  - optimizing terraform requests -> merging API calls
    - CISC vs RISC?

- services
  - key-value store (sqlite?)
  - secret store
    - auto-rotate
    - auto-gen
    - import
    - access logs
    - kv store under the hood?
  - key store
  - blob storage (sqlite?)
    - queues?
    - NFS?
  - docker registry
  - redis
  - postgres
  - VM
  - networking
    - network, subnet
    - DNS
  - resolver -> name to id
  - identity
    - users -> kv store
    - groups -> kv store
    - actor id for each transaction
      - roles that give access
      - management level apis
      - data level apis
    - service accounts
      - passwordless (default)
      - external usage
  - log aggregation
  - alerts
  - billing

- naming convention by default
  - resource type in name
  - region in name
  - instance identifier name?
