# After Downloading Files

## Step 1: Download All Files

Click the download button on each file above. You should have:

**Core Application:**
- main.py
- requirements.txt
- .env.example
- railway.json
- Dockerfile
- .gitignore

**Testing & Tools:**
- test_api.py
- start.sh
- deploy-railway.sh

**Configuration:**
- mcp-manifest.json
- openapi-agent-guidance.json

**Documentation:**
- README.md
- GITHUB_DEPLOY_STEPS.md
- WINDOWS_GUIDE.md
- START_HERE.md

---

## Step 2: Organize Files

### Option A: Create folder in Downloads

```powershell
# Open PowerShell
cd ~/Downloads

# Create project folder
mkdir agent-utility-api

# Move all downloaded files into this folder
Move-Item main.py agent-utility-api/
Move-Item requirements.txt agent-utility-api/
Move-Item *.md agent-utility-api/
Move-Item *.json agent-utility-api/
Move-Item *.py agent-utility-api/
Move-Item railway.json agent-utility-api/
Move-Item Dockerfile agent-utility-api/
Move-Item .gitignore agent-utility-api/
Move-Item .env.example agent-utility-api/
Move-Item *.sh agent-utility-api/

# Go into folder
cd agent-utility-api
```

### Option B: Create folder elsewhere

```powershell
# Create in a simple location
mkdir C:\projects\agent-utility-api

# Move files (from Downloads)
cd ~/Downloads
Move-Item *.py C:\projects\agent-utility-api\
Move-Item *.txt C:\projects\agent-utility-api\
Move-Item *.md C:\projects\agent-utility-api\
Move-Item *.json C:\projects\agent-utility-api\
# etc...

# Go there
cd C:\projects\agent-utility-api
```

---

## Step 3: Verify Files

```powershell
# Check you have all files
dir

# Should see:
# main.py
# requirements.txt
# README.md
# test_api.py
# railway.json
# etc.
```

---

## Step 4: Deploy to GitHub + Railway

**Now follow GITHUB_DEPLOY_STEPS.md:**

```powershell
# 1. Initialize Git
git init

# 2. Configure Git (use your info)
git config --global user.name "Your Name"
git config --global user.email "your@email.com"

# 3. Add files
git add .

# 4. Commit
git commit -m "Initial commit: Agent Utility API"

# 5. Create GitHub repo (in browser)
# Go to github.com → New Repository → agent-utility-api

# 6. Push to GitHub (replace YOUR-USERNAME)
git remote add origin https://github.com/YOUR-USERNAME/agent-utility-api.git
git branch -M main
git push -u origin main

# 7. Deploy on Railway
# Go to railway.app → New Project → Deploy from GitHub repo
# Select agent-utility-api

# 8. Set environment variables
railway variables set PAYMENT_WALLET=0x41A024c1C89Fd30122c8b184de99cbE751eaC970 BASE_RPC_URL=https://mainnet.base.org PRICE_PER_CALL_USDC=0.001 BYPASS_PAYMENT=true

# 9. Get URL
railway domain

# 10. Test
curl https://YOUR-URL.railway.app/health
```

---

## Quick Reference

**After organizing files, read in this order:**
1. START_HERE.md (overview)
2. GITHUB_DEPLOY_STEPS.md (detailed deployment)
3. WINDOWS_GUIDE.md (Windows-specific commands)

**Current location after download:** `~/Downloads/`  
**Where you should organize them:** `~/Downloads/agent-utility-api/` or `C:\projects\agent-utility-api\`

**Next action:** Download all files above, then run Step 2 commands to organize them.

---

## Need Help?

- See GITHUB_DEPLOY_STEPS.md for complete walkthrough
- See WINDOWS_GUIDE.md for Windows-specific instructions
- See TROUBLESHOOTING.md if you hit issues

**Once files are downloaded and organized, you're ready to deploy in 15 minutes!**
