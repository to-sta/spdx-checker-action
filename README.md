# SPDX Checker Action

A GitHub Action that checks SPDX license identifiers in your project files using the [`spdx_checker`](https://pypi.org/project/spdx-checker/).


## Usage

```yaml
- name: Check SPDX Licenses
  uses: to-sta/spdx-checker-action@v0.0.3
  with:
    target-license: 'MIT'
    file-paths: 'src/,tests/'
    extensions: 'py,js,ts'
    exclude: 'vendor/,node_modules/'
    continue-on-error: false
    fix: false
```

## Inputs

| Input | Description | Required | Default |
|-------|-------------|----------|---------|
| `target-license` | Target SPDX license identifier to check for | No | `''` |
| `file-paths` | Comma-separated list of directories to scope the check to. On PRs, only changed files within these directories are checked. On push (no changed files), all files in these directories are checked. Leave empty to check all changed files regardless of location. | No | `''` |
| `extensions` | Comma-separated list of file extensions to check (e.g., `py,js`). Do not include the leading dot. | No | `''` (all files) |
| `exclude` | Comma-separated list of glob patterns to exclude (e.g., `**/dist/**,**/node_modules/**`) | No | `''` |
| `continue-on-error` | Continue checking even if errors are found (`true` or `false`) | No | `false` |
| `fix` | Automatically fix license headers (`true` or `false`) | No | `false` |

> **Note:** The `extensions` and `exclude` filtering is applied by the action before passing individual file paths to `spdx_checker`. The library itself only receives resolved file paths.

### Example Workflow

```yaml
name: SPDX License Check

on:
  pull_request:
    branches: [main]
  push:
    branches: [main]

jobs:
  license-check:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v6
      
      - name: Check licenses
        uses: to-sta/spdx-checker-action@v0.0.2
        with:
          target-license: 'MIT'
          file-paths: 'src/,tests/'
          extensions: 'py,js,ts,go'
          exclude: 'vendor/,node_modules/,dist/'
```

## How It Works

The action detects changed files (via `tj-actions/changed-files`) and combines that with the `file-paths` scope:

| `file-paths` set? | Changed files? | Behavior |
|--------------------|----------------|----------|
| Yes | Yes (PR) | Only check changed files **within** the scoped directories |
| Yes | No (push) | Check **all** files in the scoped directories |
| No | Yes (PR) | Check **all** changed files regardless of location |
| No | No | Nothing to check |

After determining which files to check:

1. **Extension filtering** — If `extensions` is provided, only files matching the given extensions are kept.
2. **Exclusion patterns** — Files matching any `exclude` glob pattern are removed.
3. **License check** — The final file list is passed to `spdx_checker.check_license()`, which verifies each file contains the correct `SPDX-License-Identifier` header.

## Development

### Prerequisites

- [act](https://github.com/nektos/act) - Run GitHub Actions locally
- Docker

### Testing Locally with act

1. **Install act**:
   ```bash
   brew install act
   ```

2. **Run the test workflow**:
   ```bash
   act -j test
   ```