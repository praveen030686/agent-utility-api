# GitHub Deployment - Step by Step

## Part 1: Push Code to GitHub (5 minutes)

### Step 1: Check if Git is installed
```powershell
git --version
```

**If you get an error:**
- Download Git from: https://git-scm.com/download/win
- Install with default options
- Restart PowerShell
- Try `git --version` again

### Step 2: Navigate to your project folder
```powershell
cd C:\path\to\agent-utility-api
```

### Step 3: Initialize Git repository
```powershell
git init
```

**Expected output:**
```
Initialized empty Git repository in C:/path/to/agent-utility-api/.git/
```

### Step 4: Configure Git (first time only)
```powershell
# Replace with your name and email
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

### Step 5: Add all files
```powershell
git add .
```

**This adds all files to staging**

### Step 6: Commit files
```powershell
git commit -m "Initial commit: Agent Utility API"
```

**Expected output:**
```
[main (root-commit) abc1234] Initial commit: Agent Utility API
 13 files changed, XXX insertions(+)
 create mode 100644 main.py
 create mode 100644 requirements.txt
 ...
```

---

## Part 2: Create GitHub Repository (3 minutes)

### Step 7: Go to GitHub
1. Open browser: https://github.com
2. Login (or sign up if you don't have account)

### Step 8: Create new repository
1. Click **+** in top-right corner
2. Click **"New repository"**

### Step 9: Fill in repository details
- **Repository name:** `agent-utility-api`
- **Description:** "High-traffic utility endpoints for AI agents"
- **Visibility:** Public (recommended) or Private
- **Do NOT check:** "Initialize repository with README"
- **Do NOT add:** .gitignore or license (you already have these)

### Step 10: Click "Create repository"

### Step 11: Copy the repository URL
After creating, you'll see instructions. Copy the URL that looks like:
```
https://github.com/YOUR-USERNAME/agent-utility-api.git
```

---

## Part 3: Push to GitHub (2 minutes)

### Step 12: Add remote repository
```powershell
# Replace YOUR-USERNAME with your actual GitHub username
git remote add origin https://github.com/YOUR-USERNAME/agent-utility-api.git
```

### Step 13: Rename branch to main
```powershell
git branch -M main
```

### Step 14: Push code to GitHub
```powershell
git push -u origin main
```

**You'll be prompted for credentials:**
- **Username:** Your GitHub username
- **Password:** Use a Personal Access Token (not your GitHub password)

**If you need to create a Personal Access Token:**
1. Go to: https://github.com/settings/tokens
2. Click "Generate new token (classic)"
3. Give it a name: "Railway Deploy"
4. Select scopes: `repo` (full control of private repositories)
5. Click "Generate token"
6. Copy the token (starts with `ghp_`)
7. Use this token as your password when pushing

**Expected output:**
```
Enumerating objects: XX, done.
Counting objects: 100% (XX/XX), done.
...
To https://github.com/YOUR-USERNAME/agent-utility-api.git
 * [new branch]      main -> main
Branch 'main' set up to track remote branch 'main' from 'origin'.
```

### Step 15: Verify on GitHub
1. Refresh your GitHub repository page
2. You should see all your files (main.py, requirements.txt, etc.)

✅ **Code is now on GitHub!**

---

## Part 4: Deploy from GitHub to Railway (5 minutes)

### Step 16: Open Railway Dashboard
1. Go to: https://railway.app
2. Login (use the same account you used with `railway login`)

### Step 17: Create New Project
1. Click **"New Project"** button
2. Select **"Deploy from GitHub repo"**

### Step 18: Authorize GitHub Access (first time only)
1. Click **"Configure GitHub App"**
2. Select which repositories Railway can access:
   - Choose: "Only select repositories"
   - Select: `agent-utility-api`
3. Click **"Install & Authorize"**

### Step 19: Select Your Repository
1. You'll see a list of repositories
2. Click on **`agent-utility-api`**
3. Railway will start deploying automatically

### Step 20: Wait for Deployment
Watch the build logs in Railway dashboard:
- Building... (2-3 minutes)
- Deploying...
- ✅ Deployed

**You'll see:**
```
Build successful
Deployment live at: https://agent-utility-api-production-XXXX.railway.app
```

---

## Part 5: Configure Environment Variables (2 minutes)

### Step 21: Set Environment Variables

**Option A: Via Railway Dashboard**
1. In Railway dashboard, click your service
2. Go to **Variables** tab
3. Click **"+ New Variable"**
4. Add these one by one:
   - `PAYMENT_WALLET` = `0x41A024c1C89Fd30122c8b184de99cbE751eaC970`
   - `BASE_RPC_URL` = `https://mainnet.base.org`
   - `PRICE_PER_CALL_USDC` = `0.001`
   - `BYPASS_PAYMENT` = `true`

**Option B: Via Railway CLI**
```powershell
railway variables set PAYMENT_WALLET=0x41A024c1C89Fd30122c8b184de99cbE751eaC970
railway variables set BASE_RPC_URL=https://mainnet.base.org
railway variables set PRICE_PER_CALL_USDC=0.001
railway variables set BYPASS_PAYMENT=true
```

### Step 22: App Auto-Restarts
After setting variables, Railway automatically restarts your app (30 seconds)

---

## Part 6: Get Your URL & Test (2 minutes)

### Step 23: Get Deployment URL

**Option A: Railway Dashboard**
- Look at the top of the page
- Copy the URL: `https://agent-utility-api-production-XXXX.railway.app`

**Option B: Railway CLI**
```powershell
railway domain
```

### Step 24: Test Your API
```powershell
# Replace with your actual URL
curl https://YOUR-PROJECT.railway.app/health
```

**Expected response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-03-18T10:30:00.000000",
  "version": "1.0.0"
}
```

### Step 25: Open API Documentation
In browser, go to:
```
https://YOUR-PROJECT.railway.app/docs
```

You should see Swagger UI with all 5 endpoints!

### Step 26: Run Full Test Suite
```powershell
python test_api.py https://YOUR-PROJECT.railway.app
```

All 9 tests should pass ✅

---

## Part 7: Future Updates (Easy!)

### How to Update Your API:

```powershell
# 1. Make changes to main.py or any file

# 2. Commit changes
git add .
git commit -m "Updated slug generation endpoint"

# 3. Push to GitHub
git push

# 4. Railway automatically detects push and redeploys!
# No need to run railway up
```

**That's it!** Railway watches your GitHub repo and auto-deploys on every push.

---

## Summary - What You Did

✅ Pushed code to GitHub
✅ Connected Railway to GitHub
✅ Automatic deployment from GitHub
✅ Set environment variables
✅ API is live and tested

**Your API URL:** `https://YOUR-PROJECT.railway.app`
**GitHub Repo:** `https://github.com/YOUR-USERNAME/agent-utility-api`

---

## Next Steps

1. **Add custom domain** (optional)
   - See `CUSTOM_DOMAIN_GUIDE.md`

2. **Share your API**
   - Update README with your URL
   - Post on Twitter/Reddit/Discord
   - Register on CDP Bazaar

3. **Monitor usage**
   ```powershell
   railway logs
   railway status
   ```

---

## Troubleshooting

**"Repository not found" when pushing:**
- Check repository URL: `git remote -v`
- Verify username in URL is correct

**"Authentication failed":**
- Use Personal Access Token (not password)
- Create at: https://github.com/settings/tokens

**Railway can't find repository:**
- Click "Configure GitHub App" in Railway
- Grant access to your repository

**Build fails on Railway:**
```powershell
# Check build logs in Railway dashboard
# Common fixes:
# - Add runtime.txt if needed: echo "python-3.11" > runtime.txt
# - Verify requirements.txt is correct
```

---

## Benefits of GitHub Deployment

✅ No Windows file permission issues
✅ Auto-deploy on every git push
✅ Version control (can rollback anytime)
✅ Team collaboration (if needed)
✅ GitHub as backup of your code
✅ Professional workflow

---

**Current Step:** Part 1, Step 1
**Start here:** `git --version`

Let me know when you're ready to start or if you hit any issues!
