+++
title = "GitHub & GitHub Actions reference"
date = 2023-12-06
aliases = ["/ref/gh"]
+++

## Rerun  workflows

```bash
function gh-rerun {
  workflowName="Rover"
	branchName=$(git rev-parse --abbrev-ref HEAD)
	runId=$(gh run list -b $branchName -w $workflowName --limit 1 --json databaseId -q '.[0].databaseId')
	gh run rerun $runId
}
```
