# Deployment Guide

## 1. Push to GitHub

Since this is a new repository, you need to create it on GitHub first:

1.  Go to [GitHub New Repository](https://github.com/new).
2.  Name it `us-stock-pnl` (or similar).
3.  Do **not** initialize with README, .gitignore, or License (we already have them).
4.  Click "Create repository".

Once created, run the following commands in your terminal (replace `YOUR_USERNAME` with your actual GitHub username):

```bash
git remote add origin https://github.com/YOUR_USERNAME/us-stock-pnl.git
git branch -M main
git push -u origin main
```

## 2. Deploy Local App to the Web

### Option A: Streamlit Community Cloud (Recommended)
This is the easiest and most reliable way to host Streamlit apps. It's free and handles the underlying server requirements (websockets) automatically.

1.  Go to [Streamlit Community Cloud](https://streamlit.io/cloud) and sign up/login with GitHub.
2.  Click **"New app"**.
3.  Select your `us-stock-pnl` repository.
4.  Set the **Main file path** to `dashboard.py`.
5.  Click **"Deploy!"**.

**Note on Data Persistence:**
Streamlit Cloud (and Vercel) does not persist local files like `trades.csv` permanently. If the app restarts (which happens frequently), your trades might reset to the initial state. To fix this for a production app, you should eventually connect a database (like Google Sheets or Supabase).

### Option B: Vercel (Configured via vercel.json)
Your project is now configured with a `vercel.json` file for Python deployment.

1.  Go to [Vercel Dashboard](https://vercel.com/dashboard).
2.  Click **"Add New..."** -> **"Project"**.
3.  Import `codewithdadady/US-P-L`.
4.  **Framework Preset:** Leave as "Other".
5.  **Environment Variables:** You may need to add any API keys if required.
6.  Click **Deploy**.

**Common Vercel Errors:**
- **500 Server Error / Application Error:** Often means Streamlit is trying to use websockets which Vercel Serverless doesn't support well.
- **Timeout:** If the app takes too longer than 10s (Hobby) or 60s (Pro) to start.
- **Module Not Found:** Check `requirements.txt` is in the root.

To fix "Application Error", ensure your `vercel.json` points to the correct entry point (we set it to `dashboard.py`). If it still fails, it confirms Vercel's incompatibility with Streamlit's server model. In that case, **Streamlit Community Cloud is the only viable free alternative.**
