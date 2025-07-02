# Security Checklist for Public Repository

## Before Making Repository Public

### ✅ Configuration Files
- [ ] `config.yaml` is in `.gitignore`
- [ ] `config.example.yaml` exists with placeholder values
- [ ] No API keys are hardcoded in source code
- [ ] No channel IDs that should be private are in example files

### ✅ Sensitive Data
- [ ] No actual YouTube API keys in any files
- [ ] No personal channel IDs in example configurations
- [ ] No downloaded videos or metadata committed
- [ ] No log files with potentially sensitive information

### ✅ Git History
- [ ] Check git history for accidentally committed credentials:
  ```bash
  git log --all --grep="api" --grep="key" --grep="secret" -i
  git log --all -S "youtube_api_key" --source --all
  ```
- [ ] If credentials found in history, consider using `git filter-branch` or BFG Repo-Cleaner

### ✅ Documentation
- [ ] README.md explains how to set up configuration
- [ ] Clear instructions for obtaining API keys
- [ ] Security notes included in documentation
- [ ] Example configuration file provided

### ✅ Environment Variables (Optional Enhancement)
Consider supporting environment variables for sensitive data:
- [ ] `YOUTUBE_API_KEY` environment variable support
- [ ] Document environment variable usage
- [ ] Fallback to config file if env vars not set

## After Making Repository Public

### 🔄 Ongoing Security
- [ ] Regularly rotate API keys
- [ ] Monitor for accidental commits of sensitive data
- [ ] Review pull requests for potential credential leaks
- [ ] Keep dependencies updated

### 🚨 If Credentials Are Accidentally Committed
1. **Immediately** rotate the exposed credentials
2. Remove the credentials from git history
3. Update `.gitignore` to prevent future occurrences
4. Consider the credentials compromised and replace them

## Commands to Check for Sensitive Data

```bash
# Search for potential API keys in files
grep -r -i "api.key\|secret\|token\|password" . --exclude-dir=.git

# Search git history for sensitive patterns
git log --all --grep="api" --grep="key" --grep="secret" -i --oneline

# Check for binary files that might contain sensitive data
find . -type f -exec file {} \; | grep -E "binary|data"
```
