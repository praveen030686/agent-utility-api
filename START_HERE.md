# START HERE

## You Have 2 Options:

### Option A: Automated Script (Easiest)
```bash
# Run the deployment script
./deploy-railway.sh

# Follow prompts, done in 2 minutes
```

### Option B: Manual Commands (Step-by-step)
Follow the 5 commands below.

---

## 5 Commands to Deploy (2 Minutes)

### 1. Install Railway CLI
```bash
npm install -g @railway/cli
```
*If you don't have npm, install Node.js first from https://nodejs.org*

### 2. Login to Railway
```bash
railway login
```
*Your browser will open. Click "Authorize". Done.*

### 3. Create Project & Deploy
```bash
railway init && railway up
```
*Creates new Railway project and deploys your code. Takes 2-3 minutes.*

### 4. Configure Environment
```bash
railway variables set PAYMENT_WALLET=0x41A024c1C89Fd30122c8b184de99cbE751eaC970 BASE_RPC_URL=https://mainnet.base.org PRICE_PER_CALL_USDC=0.001 BYPASS_PAYMENT=true
```
*Sets up payment config. BYPASS_PAYMENT=true for testing.*

### 5. Get Your URL
```bash
railway domain
```
*Generates public URL. Copy this - you'll need it!*

---

## Test It Works (1 Minute)

```bash
# Replace YOUR-URL with the URL from step 5
curl https://YOUR-URL.railway.app/health

# Should return:
# {"status":"healthy","timestamp":"...","version":"1.0.0"}
```

**If you see this ↑ you're done! API is live.**

---

## What's Next?

1. **Open docs in browser:**
   ```bash
   # Replace YOUR-URL with your actual URL
   open https://YOUR-URL.railway.app/docs
   ```

2. **Run full test suite:**
   ```bash
   python test_api.py https://YOUR-URL.railway.app
   ```

3. **Read detailed guide:**
   - See `DETAILED_GUIDE.md` for full walkthrough
   - See `CHECKLIST.md` for progress tracking
   - See `TROUBLESHOOTING.md` if issues

---

## Common Issues

**"railway: command not found"**
→ Install Node.js first: https://nodejs.org

**"502 Bad Gateway"**
→ Wait 30 seconds, app is still deploying

**"Connection refused"**
→ Check logs: `railway logs`

**Other issues:**
→ See `TROUBLESHOOTING.md`

---

## Support

- **Quick commands:** `COMMANDS.md`
- **Troubleshooting:** `TROUBLESHOOTING.md`
- **Full guide:** `DETAILED_GUIDE.md`
- **Railway docs:** https://docs.railway.app
- **Railway Discord:** https://discord.gg/railway

---

**Current Status:** Ready to deploy
**Time Required:** 2 minutes
**Next Action:** Run command #1 above

Go! 🚀
