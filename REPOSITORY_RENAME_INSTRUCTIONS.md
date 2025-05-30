# Repository Rename Instructions

## Rename Repository from `-everything-db-manager` to `everything-db-manager`

### Step 1: Rename on GitHub (Web Interface)

1. **Go to your repository**: https://github.com/0xnuminous/-everything-db-manager

2. **Access Settings**:
   - Click on the **Settings** tab (top menu bar)
   - Scroll down to the **Repository name** section

3. **Change Repository Name**:
   - Current name: `-everything-db-manager`
   - New name: `everything-db-manager`
   - Click **Rename** button
   - Confirm the rename operation

### Step 2: Update Local Remote URL

After renaming on GitHub, update your local repository:

```bash
# Navigate to your local repository
cd everything

# Update the remote URL to match new repository name
git remote set-url origin https://github.com/0xnuminous/everything-db-manager.git

# Verify the new remote URL
git remote -v

# Test connection with a simple fetch
git fetch

# Push to confirm everything works
git push
```

### Step 3: Update Documentation References

Update any hardcoded URLs in documentation files:

**Files to update**:
- `README.md` - Clone URL and repository references
- `GITHUB_SETUP.md` - Repository URL examples
- `DEPLOYMENT_SUCCESS.md` - Repository URL
- `AI_DEVELOPMENT_PROCESS.md` - Repository URL
- Any other files with hardcoded repository URLs

**Find and replace**:
- Find: `0xnuminous/-everything-db-manager`
- Replace: `0xnuminous/everything-db-manager`

### Step 4: Commit URL Updates

```bash
# After updating documentation files
git add .
git commit -m "docs: update repository URLs after rename

- Update all documentation to use new repository name
- Remove leading dash from repository references
- Ensure all clone and setup instructions are correct"
git push
```

### Step 5: Verification

1. **Check GitHub**: Visit https://github.com/0xnuminous/everything-db-manager
2. **Test Clone**: Clone repository with new URL to verify it works
3. **Update Bookmarks**: Update any bookmarks or external references

### Important Notes

- **Automatic Redirects**: GitHub provides automatic redirects from old URL to new URL
- **Clone Commands**: Update any shared clone commands with new URL
- **CI/CD**: Update any CI/CD configurations if present
- **Documentation**: Ensure all documentation reflects new repository name
- **External Links**: Update any external references to the repository

### New Repository Information

- **Old URL**: https://github.com/0xnuminous/-everything-db-manager
- **New URL**: https://github.com/0xnuminous/everything-db-manager
- **Clone Command**: `git clone https://github.com/0xnuminous/everything-db-manager.git`
- **SSH Clone**: `git clone git@github.com:0xnuminous/everything-db-manager.git`

### Troubleshooting

If you encounter issues:

1. **Remote URL Problems**:
   ```bash
   git remote remove origin
   git remote add origin https://github.com/0xnuminous/everything-db-manager.git
   ```

2. **Permission Issues**: Ensure you have admin access to the repository

3. **Redirect Issues**: Wait a few minutes for GitHub's redirect system to update

The repository rename will be complete once these steps are finished!