# Contributing to Safety for Agentic AI

Thank you for your interest in contributing! This document provides guidelines and instructions for contributing to this project.

## Development Setup

1. Clone the repository
2. Install dependencies (see main README)
3. Run validation to ensure your environment is set up correctly:
   ```bash
   make validate
   ```

## Code Quality and Validation

Before submitting a pull request, please ensure:

1. **Run validation locally:**
   ```bash
   make validate
   # or
   python3 scripts/validate_audit.py
   ```

2. **All validation checks pass:**
   - Project structure is correct
   - Python dependencies are valid
   - Docker Compose files are valid
   - YAML configurations are valid
   - Python syntax is correct
   - Required files are present
   - Script permissions are correct

3. **Code follows project conventions:**
   - Python code follows PEP 8 style guidelines
   - YAML files are properly formatted
   - Shell scripts have execute permissions

## Pre-commit Hooks

A pre-commit hook is available to automatically run validation before commits. To enable it:

```bash
chmod +x .git/hooks/pre-commit
```

The hook will run validation automatically before each commit. If validation fails, the commit will be blocked.

## Pull Request Process

1. Create a feature branch from `main`
2. Make your changes
3. Run validation: `make validate`
4. Ensure all tests pass
5. Submit a pull request

The CI/CD pipeline will automatically:
- Run validation checks
- Generate audit reports
- Comment on your PR with results

## CI/CD Integration

This project uses GitHub Actions for continuous integration:

- **On every push**: Validation runs automatically
- **On pull requests**: Full validation suite runs and results are posted as comments
- **Daily**: Scheduled validation runs to catch regressions

See [`.github/workflows/README.md`](.github/workflows/README.md) for more details.

## Reporting Issues

If you find a bug or have a suggestion:

1. Check existing issues first
2. Create a new issue with:
   - Clear description
   - Steps to reproduce (if applicable)
   - Expected vs actual behavior
   - Environment details

## Questions?

Feel free to open an issue or discussion for any questions about contributing.
