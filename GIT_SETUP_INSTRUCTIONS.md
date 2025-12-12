# Git Repository Setup Instructions

## Method 1: Using GitHub Web Interface

### Step 1: Create Repository on GitHub
1. Go to https://github.com and sign in
2. Click the **"+"** icon in the top right → **"New repository"**
3. Repository name: `CST1510CW2-1` (or your preferred name)
4. Choose **Public** or **Private**
5. **DO NOT** check "Add a README file" or "Add .gitignore"
6. Click **"Create repository"**

### Step 2: Initialize Git and Push (Windows PowerShell/Terminal)

Open PowerShell or Terminal in your project folder and run:

```powershell
# Navigate to your project folder
cd "C:\Users\user\Downloads\CST1510CW2-1"

# Initialize git repository
git init

# Add all files (respects .gitignore)
git add .

# Create first commit
git commit -m "Initial commit: Intelligence Platform"

# Add remote repository (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/CST1510CW2-1.git

# Push to GitHub
git branch -M main
git push -u origin main
```

**Note:** You'll be prompted for your GitHub username and password (use a Personal Access Token, not your password).

---

## Method 2: Using GitHub CLI (gh)

If you have GitHub CLI installed:

```powershell
cd "C:\Users\user\Downloads\CST1510CW2-1"
gh repo create CST1510CW2-1 --public --source=. --remote=origin --push
```

---

## Method 3: Using Git GUI (GitHub Desktop)

1. Download GitHub Desktop: https://desktop.github.com/
2. Sign in with your GitHub account
3. Click **"File"** → **"Add Local Repository"**
4. Browse to: `C:\Users\user\Downloads\CST1510CW2-1`
5. Click **"Publish repository"** in GitHub Desktop
6. Choose name and visibility, then click **"Publish"**

---

## Troubleshooting

### If you get "authentication failed":
- Use a Personal Access Token instead of password:
  1. Go to GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
  2. Generate new token with `repo` permissions
  3. Use the token as your password when pushing

### If you get "remote origin already exists":
```powershell
git remote remove origin
git remote add origin https://github.com/YOUR_USERNAME/CST1510CW2-1.git
```

### If you need to check what will be committed:
```powershell
git status
```

### To see what files are ignored:
```powershell
git status --ignored
```

---

## Verify Your Push

After pushing, check:
1. Go to your repository on GitHub
2. Verify all files are there (except those in .gitignore)
3. Check that `intelligence_platform.db` is NOT in the repository
4. Check that `.streamlit/secrets.toml` is NOT in the repository

---

## Future Updates

To push future changes:
```powershell
git add .
git commit -m "Description of changes"
git push
```


