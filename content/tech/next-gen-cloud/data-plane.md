+++
title = "Data plane"
date = 2024-04-10
+++

Stricter access control. Invisible DR. Simple migrations.
Fast & Versatile - few resource types, many use-cases, one fit-all solutions
(optimized_for property).

Resources:
- KV
  - optimized_for:
    - none (hashmap)
    - prefix search (tree?)
    - value search?
    - big files (blob integration)
  - size requirements on key
  - size requirements on value (none with big files)
  - SQL-like query language
  - export to
    - SQLite
    - Postgres
    - CSV (under X MiB) -> pay per export
    - JSON (under Y MiB) -> pay per export
  - backup to blobs
    - full
    - incremental
- Blobs
  - optimized_for
    - retention of storage: hot, warm, cold
    - auto transition, customizable
    - (optional) compression
    - registry (docker, npm, nuget, crate, etc)
  - general purpose storage
    - store tfstate
    - store images
  - retention days
- NFS
  - optimized_for
    - read or write?
  - disk & blobs
- Serverless
  - deploy singular functions & store state in KV
  - deploy code: dotnet, rust, js/ts, python?
- Containers
  - docker
  - docker-compose
  - tiny k8s
  - container registry
- Logging
  - log collector (blob)
  - log viewer (function?)
- Alerts
  - email
  - notification (from the app)
  - webhook
- Database
  - minimal options postgres
  - minimal options SQLite
