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

### Option B: Render.com (Highly Recommended Alternative)

If Streamlit Cloud is having issues, **Render** is the best free alternative for Python apps. It supports persistent servers natively.

1.  Go to **[render.com](https://render.com/)** and sign up/login with GitHub.
2.  Click **"New +"** -> **"Web Service"**.
3.  Connect to your repository: `codewithdadady/US-P-L`.
4.  **Name:** `us-stock-pnl` (or similar).
5.  **Region:** Select one close to you (e.g., Singapore or Oregon).
6.  **Runtime:** "Python 3".
7.  **Build Command:** `pip install -r requirements.txt` (Render usually auto-detects this).
8.  **Start Command:** `streamlit run dashboard.py --server.port $PORT --server.address 0.0.0.0` (or leave blank, as we added a `Procfile` which Render will read automatically).
9.  **Instance Type:** "Free".
10. Click **"Create Web Service"**.

**Note:** The Free Tier on Render spins down after 15 minutes of inactivity. It will take about 50 seconds to "wake up" when you visit it again. This is normal for free hosting.

