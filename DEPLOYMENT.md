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

### Option B: Vercel (Advanced/Experimental)
Vercel is optimized for serverless functions and static sites. Streamlit requires a persistent server, so deploying it to Vercel is difficult and often unstable due to timeout limits and websocket issues.

If you strictly require Vercel, you would need to wrap the application in a Docker container (using Vercel's legacy support or a different service) or use a third-party adapter, which is not recommended for this type of financial dashboard.

**Recommendation:** Stick to **Streamlit Community Cloud** or **Render** for a hassle-free experience.
