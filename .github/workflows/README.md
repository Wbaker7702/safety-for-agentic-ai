# GitHub Actions Workflows

This directory contains GitHub Actions workflows for continuous integration and quality assurance.

## Workflows

### `validate-audit.yml`

Comprehensive validation and audit workflow that runs on:
- Push to any branch
- Pull requests to main
- Manual trigger (workflow_dispatch)
- Daily schedule (2 AM UTC)

**Features:**
- Runs the full validation and audit script
- Uploads audit reports as artifacts
- Comments on PRs with validation results
- Fails the build if validation fails

### `ci.yml`

Main CI pipeline that runs on:
- Push to main branch
- Pull requests to main

**Jobs:**
1. **validate** - Runs the validation script
2. **lint** - Code quality checks (Python syntax, YAML validation)
3. **docker-compose-check** - Validates Docker Compose files (if Docker is available)

## Usage

### Manual Trigger

You can manually trigger the validation workflow from the GitHub Actions tab:
1. Go to Actions → Build, Validate, and Audit
2. Click "Run workflow"
3. Select branch and click "Run workflow"

### Viewing Results

- Check the Actions tab for workflow run status
- Download audit reports from the workflow artifacts
- For PRs, check the PR comments for validation results

## Status Badge

Add this to your README.md to show CI status:

```markdown
![CI](https://github.com/YOUR_ORG/YOUR_REPO/workflows/CI%20Pipeline/badge.svg)
![Validate](https://github.com/YOUR_ORG/YOUR_REPO/workflows/Build,%20Validate,%20and%20Audit/badge.svg)
```
