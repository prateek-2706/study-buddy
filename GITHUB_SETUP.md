# 📝 Add Code to GitHub - Complete Steps

## Step 1: Create GitHub Account (if you don't have one)
- Go to: https://github.com/signup
- Fill email, password, username
- Verify email
- **Done!**

---

## Step 2: Create Personal Access Token (for authentication)

1. Go to: https://github.com/settings/tokens/new
2. Fill in:
   - **Note**: `study-buddy-token`
   - **Expiration**: 90 days (or more)
   - **Select scopes**: Check `repo` (all sub-options will auto-check)
3. Click **"Generate token"**
4. **Copy the token** (you'll need it later)
5. **Save it somewhere safe** (you won't see it again)

---

## Step 3: Install Git on Your Computer

### Option A: Using Installer (Recommended)
1. Go to: https://git-scm.com/download/win
2. Click the **64-bit Git for Windows Setup** link
3. Run the installer (GitSetup-2.x.x-64-bit.exe)
4. Click **Next** through all screens (defaults are fine)
5. **Finish installation**
6. **Restart PowerShell** (close and reopen)

### Option B: Using Chocolatey (if you have it)
```powershell
choco install git -y
```

### Verify Git installed:
```powershell
git --version
```
Should show: `git version 2.x.x.windows.x`

---

## Step 4: Create Repository on GitHub

1. Go to: https://github.com/new
2. Fill in:
   - **Repository name**: `study-buddy`
   - **Description**: `Agentic AI Study Buddy with FastAPI and LangChain`
   - **Visibility**: Select **Public** ✓
   - **Do NOT** check "Initialize this repository with:"
3. Click **"Create repository"**
4. You'll see a page with commands
5. **Copy the HTTPS URL** (looks like: `https://github.com/YOUR_USERNAME/study-buddy.git`)

---

## Step 5: Push Code to GitHub

### Run these commands in PowerShell:

```powershell
# Go to your project
cd "c:\Users\Prateek Batra\Downloads\paraphraser"

# Initialize git
git init

# Set your name and email (one-time setup)
git config --global user.name "Your Name"
git config --global user.email "your.email@gmail.com"

# Add all files
git add .

# Create a commit
git commit -m "Initial commit: Study Buddy - Agentic AI FastAPI app"

# Add GitHub as remote (replace with YOUR URL from Step 4)
git remote add origin https://github.com/YOUR_USERNAME/study-buddy.git

# Rename branch to main
git branch -M main

# Push to GitHub
git push -u origin main
```

**When it asks for credentials:**
- **Username**: Your GitHub username
- **Password**: Paste the **Personal Access Token** from Step 2 (NOT your GitHub password)

---

## Step 6: Verify on GitHub

1. Go to: https://github.com/YOUR_USERNAME/study-buddy
2. You should see all your files!
3. ✅ Success!

---

## 📋 Example (with real values)

```powershell
cd "c:\Users\Prateek Batra\Downloads\paraphraser"

git init

git config --global user.name "Prateek Batra"
git config --global user.email "prateek@example.com"

git add .

git commit -m "Initial commit: Study Buddy - Agentic AI FastAPI app"

git remote add origin https://github.com/prateekbatra/study-buddy.git

git branch -M main

git push -u origin main
```

When it asks:
- Username: `prateekbatra`
- Password: `ghp_xxxxxxxxxxxxxxxxxxxx` (your token from Step 2)

---

## ✅ After Push is Complete

You'll see:
```
Enumerating objects: ...
Counting objects: ...
Compressing objects: ...
Writing objects: 100% (XX/XX)
...
To https://github.com/YOUR_USERNAME/study-buddy.git
 * [new branch]      main -> main
Branch 'main' set up to track remote branch 'main' from 'origin'.
```

**Now your code is on GitHub!** 🎉

---

## 🚀 Next: Deploy to Railway

1. Go to: https://railway.app/dashboard
2. Click **"New Project"**
3. Select **"Deploy from GitHub"**
4. Authorize Railway → Select `study-buddy` repo
5. Railway auto-deploys!
6. Add `OPENAI_API_KEY` in Variables
7. Get your live URL in 2-3 minutes

---

## ❌ Troubleshooting

| Error | Fix |
|-------|-----|
| `git: command not found` | Install Git from https://git-scm.com/download/win and restart PowerShell |
| `fatal: not a git repository` | Make sure you're in project folder (`cd "c:\Users\Prateek Batra\Downloads\paraphraser"`) |
| `ERROR: Repository not found` | Check your GitHub URL is correct |
| `authentication failed` | Use Personal Access Token (not password) from Step 2 |
| `fatal: A branch named 'main' already exists` | Run `git branch -D main` first, then retry |

---

## 💡 Tips

- Keep your Personal Access Token safe (like a password)
- You only need to configure user.name/user.email **once** (global)
- Each time you make changes, run:
  ```powershell
  git add .
  git commit -m "Your message"
  git push
  ```

---

**Ready? Start from Step 1 and follow each step carefully!**

**Tell me if you get stuck on any step!** 🚀
