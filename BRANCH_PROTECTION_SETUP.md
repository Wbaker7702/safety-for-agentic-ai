# Branch Protection Setup Guide

## Enable Branch Protection for Main Branch

To ensure that merges are blocked when validation fails, follow these steps:

### Step 1: Navigate to Branch Protection Settings

1. Go to your repository on GitHub: `https://github.com/Wbaker7702/safety-for-agentic-ai`
2. Click on **Settings** (top navigation bar)
3. Click on **Branches** (left sidebar)
4. Under **Branch protection rules**, click **Add rule** or **Edit** if a rule exists for `main`

### Step 2: Configure Branch Protection Rule

**Branch name pattern:** `main`

#### Required Settings:

1. ✅ **Require a pull request before merging**
   - Check this option
   - Optionally set minimum number of approvals

2. ✅ **Require status checks to pass before merging**
   - **Check this option** (critical for validation blocking)
   - Check **"Require branches to be up to date before merging"**
   
3. **Select Required Status Checks:**
   Add the following status checks (they will appear after workflows run):
   - ✅ `Validate and Audit Project` (from `validate-audit.yml`)
   - ✅ `Validate Project` (from `ci.yml`)
   - ✅ `Code Quality Checks` (from `ci.yml`)
   - ✅ `Docker Compose Validation` (from `ci.yml`)

4. ✅ **Require conversation resolution before merging** (optional but recommended)
   - Ensures all PR comments are addressed

5. ✅ **Do not allow bypassing the above settings** (recommended)
   - Prevents admins from bypassing protection

6. ✅ **Include administrators** (recommended)
   - Applies rules to everyone including admins

### Step 3: Save the Rule

Click **Create** or **Save changes** to apply the branch protection rule.

### Step 4: Verify Protection

After setting up branch protection:

1. Create a test PR that would fail validation
2. Verify that the merge button is disabled/grayed out
3. Check that the PR shows required status checks
4. Verify that merge is blocked until all checks pass

## What This Achieves

With branch protection enabled:

- ✅ **Merges are blocked** if validation fails
- ✅ **Status checks must pass** before merging
- ✅ **Branches must be up to date** with main
- ✅ **No bypassing** of validation checks
- ✅ **Consistent quality** across all merges

## Required Status Checks

After workflows run at least once, these checks will be available:

| Check Name | Workflow | Purpose |
|------------|----------|---------|
| `Validate and Audit Project` | `validate-audit.yml` | Main validation workflow |
| `Validate Project` | `ci.yml` | CI validation job |
| `Code Quality Checks` | `ci.yml` | Linting and syntax checks |
| `Docker Compose Validation` | `ci.yml` | Docker Compose validation |

## Troubleshooting

### Status Checks Not Appearing

If status checks don't appear in the dropdown:

1. **Wait for workflows to run** - Checks appear after first workflow run
2. **Check workflow names** - Ensure workflow names match exactly
3. **Verify workflow syntax** - Check Actions tab for errors
4. **Refresh the page** - Sometimes a refresh is needed

### Merge Still Allowed After Setup

If merges are still allowed after setting up protection:

1. Verify branch name pattern matches exactly (`main`)
2. Check that "Require status checks" is enabled
3. Ensure "Require branches to be up to date" is checked
4. Verify required checks are selected
5. Check that "Do not allow bypassing" is enabled

## Quick Setup Command (GitHub CLI)

If you have GitHub CLI installed and authenticated:

```bash
# Note: This requires GitHub CLI with proper permissions
# You may need to do this via the web UI instead

gh api repos/Wbaker7702/safety-for-agentic-ai/branches/main/protection \
  --method PUT \
  --field required_status_checks='{"strict":true,"contexts":["Validate and Audit Project","Validate Project","Code Quality Checks","Docker Compose Validation"]}' \
  --field enforce_admins=true \
  --field required_pull_request_reviews='{"required_approving_review_count":0}' \
  --field restrictions=null
```

**Note:** The status check contexts will only be available after workflows have run at least once.

## Alternative: Manual Setup via Web UI

The web UI is the most reliable method:

1. Go to: `https://github.com/Wbaker7702/safety-for-agentic-ai/settings/branches`
2. Click **Add rule** or edit existing rule for `main`
3. Configure as described above
4. Save changes

---

*After setting up branch protection, test it by creating a PR that would fail validation to ensure merges are properly blocked.*
