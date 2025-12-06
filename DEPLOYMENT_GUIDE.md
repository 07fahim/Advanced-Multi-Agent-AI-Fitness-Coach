# 🚀 Streamlit Cloud Deployment Guide

Complete step-by-step guide to deploy your AI Fitness Coach app to Streamlit Cloud with CI/CD.

---

## 📋 Prerequisites

- GitHub account (free)
- Streamlit Cloud account (free)
- Your API keys ready:
  - `GROQ_API_KEY`
  - `ASTRA_DB_APPLICATION_TOKEN`
  - `ASTRA_ENDPOINT`

---

## Step 1: Prepare Your Code

### 1.1 Check Your Files

Make sure you have these files in your project:
- ✅ `main.py` (your main app file)
- ✅ `requirements.txt` (dependencies)
- ✅ `.gitignore` (should include `.env`)

### 1.2 Verify .gitignore

Your `.gitignore` should include:
```
.env
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
venv/
env/
.venv
*.log
.DS_Store
```

**⚠️ Important:** Never commit your `.env` file to GitHub!

---

## Step 2: Create GitHub Repository

### 2.1 Create New Repository

1. Go to [GitHub.com](https://github.com) and sign in
2. Click the **"+"** icon in top right → **"New repository"**
3. Fill in details:
   - **Repository name:** `fitness-app` (or your preferred name)
   - **Description:** "AI-Powered Fitness Coach with Streamlit"
   - **Visibility:** Public (required for free Streamlit Cloud) or Private (paid plan)
   - **⚠️ DO NOT** check "Initialize with README" (if you already have code)
4. Click **"Create repository"**

### 2.2 Initialize Git (if not already done)

Open terminal in your project folder and run:

```bash
# Check if git is initialized
git status

# If not initialized, run:
git init
git add .
git commit -m "Initial commit: AI Fitness Coach app"
```

### 2.3 Connect to GitHub

```bash
# Add your GitHub repository (replace with your repo URL)
git remote add origin https://github.com/YOUR_USERNAME/fitness-app.git

# Push your code
git branch -M main
git push -u origin main
```

**Replace `YOUR_USERNAME` with your actual GitHub username!**

---

## Step 3: Set Up Streamlit Cloud

### 3.1 Sign Up for Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click **"Sign up"** or **"Sign in"**
3. Choose **"Continue with GitHub"** (recommended)
4. Authorize Streamlit Cloud to access your GitHub

### 3.2 Deploy Your App

1. Once logged in, click **"New app"**
2. Fill in the deployment form:
   - **Repository:** Select `YOUR_USERNAME/fitness-app`
   - **Branch:** `main` (or `master`)
   - **Main file path:** `main.py`
   - **App URL:** (auto-generated, or customize)
3. Click **"Deploy"**

---

## Step 4: Configure Environment Variables

### 4.1 Add Secrets in Streamlit Cloud

1. In your Streamlit Cloud dashboard, click on your app
2. Click **"⚙️ Settings"** (gear icon) or **"Manage app"**
3. Scroll down to **"Secrets"** section
4. Click **"Edit secrets"** or **"New secret"**
5. Add your environment variables:

```toml
GROQ_API_KEY = "your-groq-api-key-here"
ASTRA_DB_APPLICATION_TOKEN = "your-astra-token-here"
ASTRA_ENDPOINT = "your-astra-endpoint-here"
```

**Format:** Use TOML format (key = "value" in quotes)

### 4.2 Save and Restart

1. Click **"Save"**
2. Your app will automatically restart with new environment variables

---

## Step 5: Verify Deployment

### 5.1 Check App Status

1. Go to your Streamlit Cloud dashboard
2. Check app status:
   - ✅ **Running** = Success!
   - ❌ **Error** = Check logs

### 5.2 View Logs (if errors)

1. Click on your app
2. Click **"Manage app"** → **"Logs"**
3. Check for error messages
4. Common issues:
   - Missing environment variables
   - Import errors
   - API connection issues

### 5.3 Test Your App

1. Open your app URL (e.g., `https://fitness-app.streamlit.app`)
2. Test all features:
   - User selection
   - Profile creation
   - AI chat
   - Macro generation

---

## Step 6: Enable CI/CD (Automatic Deployment)

### 6.1 How It Works

Streamlit Cloud automatically:
- ✅ Detects pushes to your main branch
- ✅ Rebuilds your app
- ✅ Redeploys with latest code
- ✅ Shows deployment status

### 6.2 Test CI/CD

1. Make a small change to your code
2. Commit and push:
   ```bash
   git add .
   git commit -m "Test CI/CD deployment"
   git push origin main
   ```
3. Go to Streamlit Cloud dashboard
4. Watch your app automatically redeploy! 🎉

---

## 🔧 Troubleshooting

### Issue: App won't start

**Solution:**
- Check logs in Streamlit Cloud
- Verify all environment variables are set
- Ensure `requirements.txt` is correct
- Check that `main.py` is the correct entry point

### Issue: Import errors

**Solution:**
- Verify all dependencies in `requirements.txt`
- Check Python version compatibility
- Ensure all files are pushed to GitHub

### Issue: API errors

**Solution:**
- Double-check environment variable names
- Verify API keys are correct
- Check API service status

### Issue: Database connection errors

**Solution:**
- Verify `ASTRA_DB_APPLICATION_TOKEN` and `ASTRA_ENDPOINT`
- Check if AstraDB allows connections from Streamlit Cloud IPs
- Review AstraDB connection settings

---

## 📝 Quick Reference

### Git Commands (for updates)

```bash
# Make changes to your code
git add .
git commit -m "Your commit message"
git push origin main
# App auto-deploys! ✨
```

### Environment Variables Format

In Streamlit Cloud Secrets, use TOML format:
```toml
GROQ_API_KEY = "your-key"
ASTRA_DB_APPLICATION_TOKEN = "your-token"
ASTRA_ENDPOINT = "your-endpoint"
```

### Important Files

- `main.py` - Your app entry point
- `requirements.txt` - Python dependencies
- `.gitignore` - Files to exclude from Git
- `.streamlit/config.toml` - Optional Streamlit config

---

## 🎉 Success Checklist

- [ ] Code pushed to GitHub
- [ ] Streamlit Cloud account created
- [ ] App deployed to Streamlit Cloud
- [ ] Environment variables configured
- [ ] App running successfully
- [ ] CI/CD tested (push → auto-deploy works)

---

## 🔗 Useful Links

- [Streamlit Cloud Documentation](https://docs.streamlit.io/streamlit-community-cloud)
- [Streamlit Cloud Dashboard](https://share.streamlit.io)
- [GitHub](https://github.com)
- [Streamlit Docs](https://docs.streamlit.io)

---

## 💡 Pro Tips

1. **Use branches:** Create feature branches, test locally, then merge to main
2. **Monitor logs:** Check logs regularly for issues
3. **Version control:** Use meaningful commit messages
4. **Backup secrets:** Keep your API keys safe (never in code!)
5. **Test locally:** Always test changes locally before pushing

---

**🎊 Congratulations!** Your app is now live with automatic CI/CD deployment!

Every time you push to GitHub, your app will automatically update on Streamlit Cloud.

