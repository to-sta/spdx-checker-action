# SPDX Checker Action

A GitHub Action that checks SPDX license identifiers in your project files using the [`spdx_checker`](https://pypi.org/project/spdx-checker/).


## Usage

```yaml
- name: Check SPDX Licenses
  uses: to-sta/spdx-checker-action@v0.0.1
  with:
    target-license: 'MIT'
    file-paths: 'src/,tests/'
    extensions: 'py,js,ts'
    exclude: 'vendor/,node_modules/'
    continue-on-error: true
    fix: false
```

## Inputs

| Input | Description | Required | Default |
|-------|-------------|----------|---------|
| `target-license` | Target SPDX license identifier to check for | No | `''` |
| `file-paths` | Comma-separated list of file paths to check. Leave empty to auto-detect changed files in PR. | No | `''` (auto-detect) |
| `extensions` | Comma-separated list of file extensions to check (e.g., `py,js`) | No | `''` (all files) |
| `exclude` | Comma-separated list of patterns to exclude | No | `''` |
| `continue-on-error` | Continue checking even if errors are found | No | `false` |
| `fix` | Automatically fix license headers | No | `false` |


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
        uses: actions/checkout@v4
      
      - name: Check licenses
        uses: your-username/spdx-checker-action@v1
        with:
          target-license: 'MIT'
          extensions: '.py,.js,.ts,.go'
          exclude: 'vendor/,node_modules/,dist/'
```

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