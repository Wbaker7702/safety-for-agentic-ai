# Workflow Monitoring Guide

## How to Monitor CI/CD Workflow Results

### 1. View Workflow Runs

**GitHub Actions Tab:**
- Go to: `https://github.com/Wbaker7702/safety-for-agentic-ai/actions`
- You'll see all workflow runs listed
- Click on any run to see detailed logs

**What to Look For:**
- ✅ Green checkmark = Workflow passed
- ❌ Red X = Workflow failed
- 🟡 Yellow circle = Workflow in progress
- ⚪ Gray circle = Workflow queued

### 2. Check PR Comments

**On Pull Requests:**
- Open any PR: `https://github.com/Wbaker7702/safety-for-agentic-ai/pulls`
- Look for comments from the GitHub Actions bot
- Comments show validation results automatically

**Comment Format:**
```
## 🔍 Validation and Audit Results

✅ All validation checks passed!

### Summary
- ✅ Passed: 7/7
- ❌ Failed: 0/7

### Detailed Results
✅ Project Structure: PASSED
✅ Python Dependencies: PASSED
...
```

### 3. Download Audit Reports

**From Workflow Artifacts:**
1. Go to Actions tab
2. Click on a workflow run
3. Scroll down to **Artifacts** section
4. Download `audit-report` artifact
5. Extract to view `audit_report.txt` and `audit_report.json`

**Artifact Contents:**
- `audit_report.txt` - Human-readable report
- `audit_report.json` - Machine-readable JSON report

### 4. Check Build Status

**On Pull Requests:**
- Look at the PR checks section (below PR description)
- See status indicators:
  - ✅ = All checks passing
  - ❌ = Checks failing
  - 🟡 = Checks in progress

**Status Checks:**
- `Validate and Audit Project`
- `Validate Project`
- `Code Quality Checks`
- `Docker Compose Validation`

### 5. Monitor Workflow Logs

**View Detailed Logs:**
1. Go to Actions tab
2. Click on a workflow run
3. Click on a job (e.g., "Validate and Audit Project")
4. Click on a step to see detailed output

**What to Check:**
- Validation script output
- Error messages (if any)
- Execution time
- Exit codes

## Monitoring Checklist

### After Creating a PR:

- [ ] Workflows appear in Actions tab
- [ ] Workflows start running automatically
- [ ] PR comment is posted (may take a few minutes)
- [ ] Build status appears in PR checks
- [ ] Artifacts are generated and available

### After Workflow Completes:

- [ ] Check workflow status (✅ or ❌)
- [ ] Review PR comment for results
- [ ] Download and review audit reports
- [ ] Verify all checks passed
- [ ] Check execution time (should be reasonable)

### If Workflow Fails:

- [ ] Check workflow logs for errors
- [ ] Review validation script output
- [ ] Check which validation check failed
- [ ] Fix the issue and push again
- [ ] Verify workflow passes on retry

## Quick Links

- **Actions:** https://github.com/Wbaker7702/safety-for-agentic-ai/actions
- **Pull Requests:** https://github.com/Wbaker7702/safety-for-agentic-ai/pulls
- **Test PR:** Check the PR created for testing

## Expected Workflow Behavior

### On PR Creation:
1. Workflows trigger automatically (within seconds)
2. Validation runs (takes ~1-2 minutes)
3. Artifacts are uploaded
4. PR comment is posted (within 2-3 minutes)
5. Build status updates

### On PR Update:
1. Workflows trigger again
2. PR comment is updated (not duplicated)
3. New artifacts are generated
4. Build status updates

### On Push to Main:
1. Workflows trigger automatically
2. Validation runs
3. Artifacts are uploaded
4. No PR comment (not a PR event)

## Troubleshooting

### Workflows Not Running

**Check:**
- Workflow files are in `.github/workflows/`
- YAML syntax is valid
- Workflow triggers are correct
- GitHub Actions is enabled for repository

### PR Comments Not Appearing

**Check:**
- Workflow completed successfully
- PR comment step didn't error
- Check workflow logs for comment step
- Verify permissions are set correctly

### Artifacts Not Available

**Check:**
- Workflow completed (artifacts upload even on failure)
- Check artifacts section in workflow run
- Verify artifact names match workflow configuration
- Check retention period (30 days)

---

*Monitor workflows regularly to ensure CI/CD is working correctly and catching issues early.*
