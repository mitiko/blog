+++
title = "[tooling] Rerun PR's GHA run from terminal"
date = 2023-12-06
extra.exclude_meta = true
+++

Often I find myself, going to the GUI to re-run the latest Rover workflow on the
PR. This is a snippet to invoke it from my local machine.  
Note it relies on the [GitHub CLI](https://cli.github.com/) to return the runs in order, could update
the jq expression in the future..

Add the following to you `~/.bash_asiases`:

```bash
function gh-rerun {
	branchName=$(git rev-parse --abbrev-ref HEAD)
	runId=$(gh run list -b $branchName -w Rover --limit 1 --json databaseId -q '.[0].databaseId')
	gh run rerun $runId
}
```

### Usage

Just run `git switch <branch_name> && gh-rerun`
