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
- ✅ Runs the full validation and audit script
- ✅ Uploads audit reports as artifacts (retained for 30 days)
- ✅ Comments on PRs with validation results (updates existing comment if present)
- ✅ **Fails the build if validation fails** - This blocks merges when branch protection is enabled
- ✅ Proper permissions configured for PR comments

**Permissions:**
- `contents: read` - Read repository contents
- `pull-requests: write` - Comment on pull requests

### `ci.yml`

Main CI pipeline that runs on:
- Push to main branch
- Pull requests to main

**Jobs:**
1. **validate** - Runs the validation script (fails on validation errors)
2. **lint** - Code quality checks (Python syntax, YAML validation)
3. **docker-compose-check** - Validates Docker Compose files (if Docker is available)

**Note:** All jobs must pass for the CI pipeline to succeed. If any job fails, the workflow fails and can block merges.

## Merge Protection

To enable merge protection based on these workflows:

1. Go to repository Settings → Branches
2. Add or edit branch protection rule for `main` branch
3. Under "Require status checks to pass before merging":
   - Check "Require branches to be up to date before merging"
   - Select the required status checks:
     - `Validate and Audit Project` (from validate-audit.yml)
     - `Validate Project` (from ci.yml)
     - `Code Quality Checks` (from ci.yml)
     - `Docker Compose Validation` (from ci.yml)

This ensures that:
- ✅ All validation checks must pass
- ✅ PRs cannot be merged if validation fails
- ✅ Workflow must be up to date with base branch

## Usage

### Manual Trigger

You can manually trigger the validation workflow from the GitHub Actions tab:
1. Go to Actions → Build, Validate, and Audit
2. Click "Run workflow"
3. Select branch and click "Run workflow"

### Viewing Results

- **Workflow Status**: Check the Actions tab for workflow run status
- **Artifacts**: Download audit reports from the workflow artifacts (available for 30 days)
- **PR Comments**: For PRs, check the PR comments for validation results
- **Build Status**: See status checks on the PR page

### PR Comment Format

When a PR is opened or updated, a comment is automatically posted with:
- ✅/❌ Status indicator
- Summary of passed/failed checks
- List of errors (if any)
- Detailed results for each check
- Link to full report in artifacts

The comment is updated on subsequent runs (doesn't create duplicate comments).

## Status Badge

Add this to your README.md to show CI status:

```markdown
![CI](https://github.com/YOUR_ORG/YOUR_REPO/workflows/CI%20Pipeline/badge.svg)
![Validate](https://github.com/YOUR_ORG/YOUR_REPO/workflows/Build,%20Validate,%20and%20Audit/badge.svg)
```

Replace `YOUR_ORG` and `YOUR_REPO` with your actual organization and repository names.

## Workflow Behavior

### On Push
- Workflow runs automatically
- Results are available in Actions tab
- Artifacts are uploaded
- **No PR comments** (not a PR event)

### On Pull Request
- Workflow runs automatically
- Results are available in Actions tab
- Artifacts are uploaded
- **Comment is posted/updated on the PR**
- **Build status shown in PR checks**
- **Merge can be blocked if validation fails** (if branch protection enabled)

### On Schedule
- Runs daily at 2 AM UTC
- Useful for catching regressions
- Results available in Actions tab
- Artifacts are uploaded

### Manual Trigger
- Can be triggered from Actions UI
- Useful for testing or re-running validation
- Same behavior as push trigger

## Troubleshooting

### PR Comments Not Appearing

1. Check workflow permissions - ensure `pull-requests: write` is set
2. Verify the workflow ran on a pull_request event
3. Check workflow logs for errors in the comment step
4. Ensure GITHUB_TOKEN has proper permissions (usually automatic)

### Workflow Failing Unexpectedly

1. Check the workflow logs in the Actions tab
2. Download artifacts to view audit reports
3. Run validation locally: `make validate`
4. Verify all required files are present
5. Check YAML syntax of workflow files

### Merge Not Blocked

1. Ensure branch protection is enabled
2. Verify required status checks are selected
3. Check that workflow names match exactly
4. Ensure "Require branches to be up to date" is enabled

## Workflow Files

- `validate-audit.yml` - Main validation workflow with PR comments
- `ci.yml` - CI pipeline with multiple validation jobs
- `README.md` - This documentation
