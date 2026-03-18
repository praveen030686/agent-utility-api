# Windows PowerShell Deployment Guide

## 5 Commands for Windows (2 Minutes)

### 1. Install Railway CLI
```powershell
npm install -g @railway/cli
```

### 2. Login to Railway
```powershell
railway login
```
*Browser opens → Click "Authorize"*

### 3. Create Project
```powershell
railway init
```
*Choose: "Create a new project" → Name it "agent-utility-api"*

### 4. Deploy Code
```powershell
railway up
```
*Wait 2-3 minutes for build*

### 5. Set Environment Variables (ONE command, copy all)
```powershell
railway variables set PAYMENT_WALLET=0x41A024c1C89Fd30122c8b184de99cbE751eaC970 BASE_RPC_URL=https://mainnet.base.org PRICE_PER_CALL_USDC=0.001 BYPASS_PAYMENT=true
```

### 6. Generate Domain
```powershell
railway domain
```
*Save this URL!*

---

## Test It Works

```powershell
# Replace YOUR-URL with the URL from step 6
curl https://YOUR-URL.railway.app/health
```

**OR use browser:**
1. Open: `https://YOUR-URL.railway.app/health`
2. Should see: `{"status":"healthy"...}`

---

## Full Test Suite

```powershell
# Get your URL first
railway domain

# Run tests (replace YOUR-URL)
python test_api.py https://YOUR-URL.railway.app
```

---

## Common Windows Commands

```powershell
# View logs
railway logs

# View logs continuously
railway logs --tail

# Check status
railway status

# Open dashboard in browser
railway open

# Redeploy after changes
railway up

# List environment variables
railway variables
```

---

## Windows-Specific Notes

### If using Git Bash instead of PowerShell:
- The Linux/Mac commands work in Git Bash
- Use `&&` operator: `railway init && railway up`

### If using Command Prompt (cmd):
- Use separate commands, no `&&`
- Same as PowerShell instructions above

### If npm command not found:
1. Install Node.js from: https://nodejs.org
2. Choose "LTS" version
3. Restart PowerShell after installation
4. Test: `node --version`

---

## Next Steps

1. **Open docs in browser:**
   ```
   Start browser → https://YOUR-URL.railway.app/docs
   ```

2. **Test endpoints interactively:**
   - Go to /docs page
   - Click "POST /api/slug/generate"
   - Click "Try it out"
   - Enter: `{"text": "Hello World"}`
   - Click "Execute"
   - See result: `{"slug": "hello-world"...}`

3. **Update files with your URL:**
   - Open `README.md` in text editor
   - Find: `https://your-api.railway.app`
   - Replace with: `https://YOUR-ACTUAL-URL.railway.app`
   - Save

4. **Share your API:**
   - See `DETAILED_GUIDE.md` Step 23-26 for sharing instructions
   - Twitter, Reddit, Discord templates included

---

## Troubleshooting Windows Issues

### PowerShell execution policy error:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Railway command not recognized:
```powershell
# Restart PowerShell after installing Railway CLI
# Or close and reopen PowerShell window
```

### Node/npm not found:
1. Download Node.js: https://nodejs.org
2. Run installer (choose default options)
3. Restart PowerShell
4. Test: `node --version` and `npm --version`

### curl command not found (older Windows):
```powershell
# Use Invoke-WebRequest instead:
Invoke-WebRequest -Uri https://YOUR-URL.railway.app/health

# Or just open the URL in your browser
```

---

## Alternative: Use WSL (Windows Subsystem for Linux)

If you prefer Linux commands:

```powershell
# Install WSL (if not installed)
wsl --install

# Restart computer

# Open WSL terminal
wsl

# Now use Linux commands from START_HERE.md
npm install -g @railway/cli
railway login
# etc...
```

---

**Current Status:** Ready for Step 1
**Time Required:** 2 minutes
**Next Action:** Run `npm install -g @railway/cli` in PowerShell

Go! 🚀
