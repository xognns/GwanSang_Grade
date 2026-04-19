---
description: "Allocate a spec feature ID on the current collaborative branch"
---

# Allocate Feature ID

This repository does not allow git feature branches. Instead, keep the current
working branch as `main`, `front-end`, or `back-end`, then allocate a feature ID
under `specs/` for the given specification. The command prepares spec context
without creating or switching git branches.

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Environment Variable Override

If the user explicitly provided `GIT_BRANCH_NAME` (e.g., via environment
variable, argument, or in their request), pass it through to the script by
setting the `GIT_BRANCH_NAME` environment variable before invoking the script.
When `GIT_BRANCH_NAME` is set:
- The script uses the exact value as the feature ID, bypassing prefix/suffix generation
- `--short-name`, `--number`, and `--timestamp` flags are ignored
- `FEATURE_NUM` is extracted from the value if it starts with a numeric prefix, otherwise set to the full value

## Prerequisites

- Verify Git is available by running `git rev-parse --is-inside-work-tree 2>/dev/null`
- If Git is available, the current branch MUST be one of `main`, `front-end`, or `back-end`
- If Git is not available, warn the user and continue with a logical feature ID only

## Branch Numbering Mode

Determine the feature ID numbering strategy by checking configuration in this order:

1. Check `.specify/extensions/git/git-config.yml` for `branch_numbering` value
2. Check `.specify/init-options.json` for `branch_numbering` value (backward compatibility)
3. Default to `sequential` if neither exists

## Execution

Generate a concise short name (2-4 words) for the feature ID:
- Analyze the feature description and extract the most meaningful keywords
- Use action-noun format when possible (e.g., "add-user-auth", "fix-payment-bug")
- Preserve technical terms and acronyms (OAuth2, API, JWT, etc.)

Run the appropriate script based on your platform:

- **Bash**: `.specify/extensions/git/scripts/bash/create-new-feature.sh --json --short-name "<short-name>" "<feature description>"`
- **Bash (timestamp)**: `.specify/extensions/git/scripts/bash/create-new-feature.sh --json --timestamp --short-name "<short-name>" "<feature description>"`
- **PowerShell**: `.specify/extensions/git/scripts/powershell/create-new-feature.ps1 -Json -ShortName "<short-name>" "<feature description>"`
- **PowerShell (timestamp)**: `.specify/extensions/git/scripts/powershell/create-new-feature.ps1 -Json -Timestamp -ShortName "<short-name>" "<feature description>"`

**IMPORTANT**:
- Do NOT pass `--number` — the script determines the correct next number automatically
- Always include the JSON flag (`--json` for Bash, `-Json` for PowerShell) so the output can be parsed reliably
- You must only ever run this script once per feature
- The JSON output will contain the allocated feature ID in `BRANCH_NAME` for backward compatibility
- The script must not create or switch git branches in this repository

## Graceful Degradation

If Git is not installed or the current directory is not a Git repository:
- Branch validation is skipped with a warning
- The script still outputs `BRANCH_NAME` and `FEATURE_NUM` so the caller can reference the logical feature ID

## Output

The script outputs JSON with:
- `BRANCH_NAME`: The feature ID (e.g., `003-user-auth` or `20260319-143022-user-auth`)
- `FEATURE_NUM`: The numeric or timestamp prefix used
- `SPEC_FILE`: The specification file path when the Bash implementation is used
