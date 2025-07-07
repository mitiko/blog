+++
title = "GitHub & GitHub Actions reference"
date = 2023-12-06
aliases = ["/ref/gh"]
+++

### Rerun  workflows

```bash
function gh-rerun {
  workflowName="Rover"
    branchName=$(git rev-parse --abbrev-ref HEAD)
    runId=$(gh run list -b $branchName -w $workflowName --limit 1 --json databaseId -q '.[0].databaseId')
    gh run rerun $runId
}
```

## Workflows

GitHub Actions workflows & common steps with their configurations.

### Rust cache workflow

Place this before `cargo build` and it will automatically cache build
dependencies.

```yaml
- uses: actions/cache@v3
  with:
  path: |
      ~/.cargo/registry
      ~/.cargo/git
      target/
  key: ${{ runner.os }}-cargo-${{ hashFiles('**/Cargo.lock') }}
```
