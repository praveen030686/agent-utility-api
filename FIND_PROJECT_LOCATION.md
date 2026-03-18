# Finding Your Project Location on Windows

## Quick Methods to Find Your Files

### Method 1: Use File Explorer to Find Path

1. **Open File Explorer**
2. **Navigate to where you saved the files** (Downloads, Desktop, Documents, etc.)
3. **Find the folder** containing `main.py`, `requirements.txt`, etc.
4. **Click on the address bar at the top**
5. **Copy the full path** (it will look like: `C:\Users\YourName\Downloads\agent-utility-api`)

### Method 2: Search for main.py

**In PowerShell:**
```powershell
# Search for main.py in common locations
Get-ChildItem -Path "$env:USERPROFILE\Downloads" -Filter "main.py" -Recurse -ErrorAction SilentlyContinue | Select-Object FullName
Get-ChildItem -Path "$env:USERPROFILE\Desktop" -Filter "main.py" -Recurse -ErrorAction SilentlyContinue | Select-Object FullName
Get-ChildItem -Path "$env:USERPROFILE\Documents" -Filter "main.py" -Recurse -ErrorAction SilentlyContinue | Select-Object FullName
```

This will show you the full path to your files.

### Method 3: Navigate Using cd Without Full Path

**Start from your user folder:**
```powershell
# Go to your home folder
cd ~

# Check if files are in Downloads
cd Downloads
dir
# Look for agent-utility-api folder or main.py file

# Or check Desktop
cd ~/Desktop
dir

# Or check Documents
cd ~/Documents
dir
```

---

## Common Locations

Your files are probably in one of these locations:

**Downloads:**
```powershell
cd C:\Users\YourName\Downloads
# or
cd ~/Downloads
```

**Desktop:**
```powershell
cd C:\Users\YourName\Desktop
# or
cd ~/Desktop
```

**Documents:**
```powershell
cd C:\Users\YourName\Documents
# or
cd ~/Documents
```

**Replace `YourName` with your actual Windows username**

---

## Once You Find the Files

### If files are in a folder called "agent-utility-api":
```powershell
cd C:\Users\YourName\Downloads\agent-utility-api
```

### If files are loose in Downloads (no folder):
```powershell
# Go to Downloads
cd ~/Downloads

# List files to verify
dir main.py
dir requirements.txt

# If you see these files, you're in the right place!
```

---

## Create Folder If Files Are Loose

**If you downloaded files individually to Downloads:**

```powershell
# Go to Downloads
cd ~/Downloads

# Create folder
mkdir agent-utility-api

# Move all files into folder
Move-Item main.py agent-utility-api/
Move-Item requirements.txt agent-utility-api/
Move-Item README.md agent-utility-api/
# ... (move all files)

# Or move everything at once:
Move-Item *.py agent-utility-api/
Move-Item *.txt agent-utility-api/
Move-Item *.md agent-utility-api/
Move-Item *.json agent-utility-api/
Move-Item *.sh agent-utility-api/

# Go into folder
cd agent-utility-api
```

---

## Verify You're in the Right Place

**Check for these files:**
```powershell
dir
```

**You should see:**
- main.py
- requirements.txt
- README.md
- test_api.py
- railway.json
- mcp-manifest.json
- etc.

**If you see these files, you're ready to proceed!**

---

## Next: Run Git Commands

**Once you're in the correct folder, run:**

```powershell
# Initialize git
git init

# Add files
git add .

# Commit
git commit -m "Initial commit"
```

Then continue with GitHub deployment steps.
