---
description: "Validate that the current branch matches the repository branch policy"
---

# Validate Collaborative Branch

Validate that the current Git branch matches this repository's branch policy.

## Prerequisites

- Check if Git is available by running `git rev-parse --is-inside-work-tree 2>/dev/null`
- If Git is not available, output a warning and skip validation:
  ```
  [specify] Warning: Git repository not detected; skipped branch validation
  ```

## Validation Rules

Get the current branch name:

```bash
git rev-parse --abbrev-ref HEAD
```

The branch name must be one of:

1. `main`
2. `front-end`
3. `back-end`

## Execution

If on an allowed branch:
- Output: `✓ On collaborative branch: <branch-name>`
- If `.specify/feature.json` or `SPECIFY_FEATURE_DIRECTORY` is present, the active spec directory may be resolved separately from the branch name

If NOT on an allowed branch:
- Output: `✗ Not on an allowed branch. Current branch: <branch-name>`
- Output: `Allowed branches are: main, front-end, back-end`

## Graceful Degradation

If Git is not installed or the directory is not a Git repository:
- Check the `SPECIFY_FEATURE` environment variable as a fallback
- If set, note that it is only a logical feature identifier, not a git branch
- If not set, skip validation with a warning
