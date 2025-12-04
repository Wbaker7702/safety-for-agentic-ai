# Validation and CI/CD Setup

This document describes the validation and CI/CD infrastructure that has been set up for the Safety for Agentic AI project.

## Overview

A comprehensive validation and audit system has been integrated into the project with both local and CI/CD capabilities.

## Components

### 1. Validation Script (`scripts/validate_audit.py`)

A Python script that performs comprehensive validation checks:

- ✅ **Project Structure** - Validates required directories exist
- ✅ **Python Dependencies** - Checks `pyproject.toml` for required dependencies
- ✅ **Docker Compose Files** - Validates syntax and structure
- ✅ **YAML Configurations** - Validates YAML syntax in config files
- ✅ **Python Syntax** - Checks all Python files for syntax errors
- ✅ **Required Files** - Ensures critical files are present
- ✅ **Script Permissions** - Verifies shell scripts are executable

**Usage:**
```bash
python3 scripts/validate_audit.py
# or
make validate
```

**Output:**
- `audit_report.txt` - Human-readable report
- `audit_report.json` - Machine-readable JSON report

### 2. GitHub Actions Workflows

#### `validate-audit.yml`
Comprehensive validation workflow that runs on:
- Push to any branch
- Pull requests to main
- Manual trigger (`workflow_dispatch`)
- Daily schedule (2 AM UTC)

**Features:**
- Runs full validation suite
- Uploads audit reports as artifacts
- Comments on PRs with validation results
- Fails build if validation fails

#### `ci.yml`
Main CI pipeline with multiple jobs:
- **validate** - Runs validation script
- **lint** - Code quality checks (Python syntax, YAML validation)
- **docker-compose-check** - Validates Docker Compose files

### 3. Makefile

Convenience targets for running validation:
```bash
make validate    # Run validation
make audit       # Alias for validate
make build       # Alias for validate
make check       # Alias for validate
make help        # Show available targets
```

### 4. Pre-commit Hook

Optional git pre-commit hook (`.git/hooks/pre-commit`) that runs validation before commits.

To enable:
```bash
chmod +x .git/hooks/pre-commit
```

## CI/CD Integration

### Automatic Triggers

1. **On Push** - Validation runs automatically on every push
2. **On Pull Request** - Full validation suite runs and results are posted as PR comments
3. **Scheduled** - Daily validation runs at 2 AM UTC
4. **Manual** - Can be triggered manually from GitHub Actions UI

### Workflow Artifacts

Each workflow run generates:
- `audit_report.txt` - Human-readable validation report
- `audit_report.json` - Machine-readable JSON report

These are available for download from the GitHub Actions UI for 30 days.

### PR Integration

When a pull request is opened or updated:
1. Validation workflow runs automatically
2. Results are posted as a comment on the PR
3. Build status is shown in the PR checks

## Local Development

### Running Validation Locally

```bash
# Using Makefile (recommended)
make validate

# Direct execution
python3 scripts/validate_audit.py

# View help
make help
```

### Pre-commit Validation

Enable the pre-commit hook to automatically validate before each commit:
```bash
chmod +x .git/hooks/pre-commit
```

## Validation Checks

The validation script performs the following checks:

1. **Project Structure** - Ensures all required directories exist
2. **Python Dependencies** - Validates `pyproject.toml` contains required dependencies
3. **Docker Compose** - Validates YAML syntax and structure
4. **YAML Configs** - Validates configuration files
5. **Python Syntax** - Checks all `.py` files for syntax errors
6. **Required Files** - Ensures critical files are present
7. **Script Permissions** - Verifies shell scripts have execute permissions

## Exit Codes

- `0` - All checks passed ✅
- `1` - One or more checks failed ❌

## Files Created/Modified

### New Files
- `scripts/validate_audit.py` - Main validation script
- `scripts/README.md` - Documentation for validation scripts
- `.github/workflows/validate-audit.yml` - Validation workflow
- `.github/workflows/ci.yml` - Main CI pipeline
- `.github/workflows/README.md` - Workflow documentation
- `Makefile` - Convenience targets
- `VALIDATION_SETUP.md` - This document
- `.git/hooks/pre-commit` - Pre-commit hook (optional)

### Modified Files
- `README.md` - Added CI/CD section
- `CONTRIBUTING.md` - Added validation guidelines
- `.gitignore` - Added audit report files

## Status Badges

Add these to your README.md to show CI status:

```markdown
![CI](https://github.com/YOUR_ORG/YOUR_REPO/workflows/CI%20Pipeline/badge.svg)
![Validate](https://github.com/YOUR_ORG/YOUR_REPO/workflows/Build,%20Validate,%20and%20Audit/badge.svg)
```

## Troubleshooting

### Validation Fails Locally

1. Check Python version (requires 3.10+)
2. Install required dependencies: `pip install pyyaml`
3. Ensure scripts have execute permissions: `chmod +x scripts/*.sh`
4. Run validation with verbose output: `python3 scripts/validate_audit.py`

### CI/CD Workflow Fails

1. Check the Actions tab for detailed error messages
2. Download workflow artifacts to view audit reports
3. Ensure all required files are present
4. Check that YAML files are valid

### Pre-commit Hook Not Working

1. Ensure hook is executable: `chmod +x .git/hooks/pre-commit`
2. Check hook file exists: `ls -la .git/hooks/pre-commit`
3. Test manually: `bash .git/hooks/pre-commit`

## Next Steps

1. ✅ Validation script created and tested
2. ✅ CI/CD workflows integrated
3. ✅ Documentation added
4. ✅ Pre-commit hook available
5. 🔄 Workflows will run automatically on next push/PR

## Support

For issues or questions:
- Check [`.github/workflows/README.md`](.github/workflows/README.md)
- Review [CONTRIBUTING.md](CONTRIBUTING.md)
- Open an issue on GitHub
