# Validation and Audit Scripts

## validate_audit.py

A comprehensive build, validate, and audit script for the Safety for Agentic AI project.

### Usage

```bash
# Direct execution
python3 scripts/validate_audit.py

# Using Makefile
make validate
# or
make audit
# or
make build
# or
make check
```

### What It Validates

The script performs the following checks:

1. **Project Structure** - Verifies all required directories exist
2. **Python Dependencies** - Validates dependencies in `pyproject.toml`
3. **Docker Compose Files** - Validates syntax and structure of Docker Compose files
4. **YAML Configurations** - Validates YAML syntax in configuration files
5. **Python Syntax** - Checks Python syntax in all `.py` files
6. **Required Files** - Ensures all critical files are present
7. **Script Permissions** - Verifies shell scripts have execute permissions

### Output

The script generates two report files:

- `audit_report.txt` - Human-readable text report
- `audit_report.json` - Machine-readable JSON report

### Exit Codes

- `0` - All checks passed
- `1` - One or more checks failed

### Integration

This script can be integrated into CI/CD pipelines to ensure project quality and consistency.
