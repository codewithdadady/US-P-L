# 📈 Real-Time Stock P&L Dashboard

A lightweight, real-time portfolio tracker built with Python and Streamlit. Track your stock investments with live price updates, P&L calculations, and an intuitive dashboard interface.

![Status](https://img.shields.io/badge/Status-Tested%20%26%20Working-brightgreen)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Platform](https://img.shields.io/badge/Platform-macOS-lightgrey)

---

## 🌐 Deployment & Cloud Hosting

### ❓ Why Vercel doesn't work for this app
Vercel is designed for **Serverless Functions** (short-lived scripts that run for a few seconds). 
Streamlit apps require a **Persistent Server** (a computer that stays on) to:
1.  Maintain a **WebSocket connection** for live updates.
2.  Remember variables (like `st.session_state`) between clicks.

If you deploy to Vercel, the server "shuts down" after every interaction, causing the app to crash or reset immediately.

### ✅ How to Setup your Free Streamlit URL
Since your code is already on GitHub, you can get a live URL in 2 minutes:

1.  Go to **[share.streamlit.io](https://share.streamlit.io/)**
2.  Click **"Sign in with GitHub"**.
3.  Click the blue **"New app"** button.
4.  **Repository:** Select `codewithdadady/US-P-L`
5.  **Main file path:** `dashboard.py`
6.  Click **"Deploy!"**

Your app will be live at a URL like `https://us-p-l-codewithdadady.streamlit.app`.

---

## 🌟 Features

### Real-Time Tracking
- ⚡ **Live Price Updates** - Fetches current stock prices every 15 seconds
- 📊 **Auto-Refresh** - Dashboard updates automatically (configurable interval)
- 🔄 **Real-Time P&L** - Instant profit/loss calculations

### Portfolio Management
- 💰 **Portfolio Summary** - Total capital, current value, and overall P&L
- 📈 **Individual Trade Tracking** - Monitor each position separately
- 🎯 **Price Targets** - Set and track multiple sell targets per stock

### User Interface
- 🟢 **Color-Coded Indicators** - Green for profit, red for loss
- ✏️ **Editable Trades** - Modify positions directly in the dashboard
- 📱 **Responsive Design** - Works on desktop and tablet browsers
- 🎨 **Clean Layout** - Organized tables with metrics cards

### Data Features
- 💾 **CSV-Based Storage** - Simple, portable data format
- 📝 **Easy Editing** - Edit trades in Excel or any text editor
- 🔒 **Local Storage** - All data stays on your machine

---

## 🖼️ Dashboard Preview

The dashboard displays:
1. **Portfolio Summary Cards** - Total capital, current value, total P&L, portfolio hit %
2. **Live Stock Table** - Real-time prices, P&L amounts, P&L percentages
3. **Trade Editor** - Inline editing capabilities
4. **Auto-Refresh Controls** - Toggle and adjust refresh rate

---

## 🚀 Quick Start

### Installation

```bash
# 1. Navigate to project folder
cd ~/stock_dashboard

# 2. Install dependencies
pip3 install -r requirements.txt

# 3. Run the dashboard
./run_dashboard.sh
```

### Or use Streamlit directly:
```bash
streamlit run dashboard.py
```

Dashboard opens automatically at `http://localhost:8501`

---

## 📋 Setup Guide

### 1. **Edit Your Trades**

Open `trades.csv` and add your stock positions:

```csv
Stock Name,Entry Date,Entry Price,Capital,Sell Date,Sell Price,Sell Target 1,Sell Target 2,Sell Target 3
AAPL,2024-01-15,175.25,10000,,,190,200,210
TSLA,2024-02-01,195.50,5000,,,220,250,280
MSFT,2024-01-20,375.80,8000,,,410,430,450
```

**Required Fields:**
- `Stock Name` - Ticker symbol (e.g., AAPL, TSLA, MSFT)
- `Entry Date` - Purchase date (YYYY-MM-DD)
- `Entry Price` - Your average buy price
- `Capital` - Total amount invested

**Optional Fields:**
- `Sell Date`, `Sell Price` - Fill when position is closed
- `Sell Target 1/2/3` - Your price targets

### 2. **Run the Dashboard**

```bash
./run_dashboard.sh
```

### 3. **Start Tracking**

- Dashboard fetches real-time prices automatically
- P&L updates every refresh cycle
- Edit trades directly in the dashboard or CSV file

---

## 🔧 Configuration

### Change Refresh Interval

In the dashboard:
1. Adjust the "Refresh Interval" slider (5-60 seconds)
2. Toggle "Auto-Refresh" on/off

In code (`dashboard.py`):
```python
refresh_interval = st.slider("Refresh Interval (seconds)", 5, 60, 15)
# Change 15 to your preferred default
```

### Supported Stock Exchanges

- **US Markets:** `AAPL`, `TSLA`, `MSFT` (default format)
- **Indian Markets:** `RELIANCE.NS`, `TCS.NS`, `INFY.NS`
- **Other Markets:** Check [Yahoo Finance](https://finance.yahoo.com) for ticker format

### Change Port

```bash
streamlit run dashboard.py --server.port 8502
```

### Access from Network

```bash
streamlit run dashboard.py --server.address 0.0.0.0
```

Then access via: `http://YOUR_MAC_IP:8501`

---

## 📊 Dashboard Calculations

### P&L Amount
```
P&L Amount = (Current Price × Shares) - Capital Invested
where Shares = Capital Invested / Entry Price
```

### P&L Percentage
```
P&L % = (P&L Amount / Capital Invested) × 100
```

### Portfolio Hit
```
Portfolio Hit % = (Total Current Value - Total Capital) / Total Capital × 100
```

---

## 🛠️ Technical Details

### Tech Stack
- **Frontend:** Streamlit (Python)
- **Data Source:** Yahoo Finance API (yfinance)
- **Data Processing:** Pandas
- **Storage:** CSV files

### Data Flow
1. Dashboard reads `trades.csv`
2. For each ticker, fetches latest price from Yahoo Finance
3. Calculates P&L based on entry price and capital
4. Updates display with color-coded indicators
5. Auto-refreshes at specified interval

### Price Update Frequency
- **Yahoo Finance Free Tier:** Typically 15-minute delayed
- **Major US Stocks:** Often near real-time
- **Dashboard Refresh:** User-configurable (5-60 seconds)

---

## 🐛 Troubleshooting

### "No data for ticker"
- ✅ Verify ticker symbol on Yahoo Finance
- ✅ Check internet connection
- ✅ Ensure ticker is active and not delisted

### "Permission denied"
```bash
chmod +x run_dashboard.sh
```

### "Port already in use"
```bash
# Kill existing process
lsof -ti:8501 | xargs kill -9

# Or use different port
streamlit run dashboard.py --server.port 8502
```

### "Package not found"
```bash
pip3 install -r requirements.txt --upgrade
```

### Prices not updating
- Check internet connection
- Reduce refresh frequency (might be rate-limited)
- Restart dashboard

---

## 📁 File Structure

```
stock_dashboard/
├── dashboard.py           # Main application code
├── trades.csv            # Your portfolio data
├── requirements.txt      # Python dependencies
├── run_dashboard.sh      # Launch script
├── INSTALLATION_GUIDE.md # Detailed setup instructions
└── README.md            # This file
```

---

## 🔒 Privacy & Security

- ✅ **100% Local** - All data stored on your Mac
- ✅ **No Account Required** - No login or registration
- ✅ **No Data Sharing** - Only fetches public market data
- ✅ **Open Source** - Review the code yourself
- ✅ **Portable** - Take your data anywhere

---

## 💡 Pro Tips

1. **Backup your trades.csv** - Keep copies before major edits
2. **Use reasonable refresh intervals** - 15-30 seconds optimal
3. **Monitor rate limits** - Yahoo Finance may throttle frequent requests
4. **Check ticker formats** - Different exchanges use different formats
5. **Test with sample data first** - Verify everything works before adding real trades

---

## 🆕 Future Enhancements (Ideas)

- [ ] Add charts and graphs
- [ ] Export to PDF/Excel
- [ ] Multiple portfolio support
- [ ] Stock alerts and notifications
- [ ] Historical P&L tracking
- [ ] Dividend tracking
- [ ] Tax calculation tools
- [ ] Mobile app version

---

## ❓ FAQ

**Q: Does this work for Indian stocks?**  
A: Yes! Use NSE format: `RELIANCE.NS`, `TCS.NS`, etc.

**Q: Is internet required?**  
A: Yes, to fetch real-time prices. Historical data is not cached.

**Q: Can I track crypto?**  
A: Yes! Use ticker format: `BTC-USD`, `ETH-USD`, etc.

**Q: How accurate are the prices?**  
A: Yahoo Finance typically has 15-min delay for free tier, but major stocks are often real-time.

**Q: Can I run multiple instances?**  
A: Yes! Use different ports and separate CSV files.

**Q: Is this production-ready?**  
A: It's a personal tool. For production use, consider adding error handling, logging, and data validation.

---

## 📞 Support

Having issues? Check:
1. **INSTALLATION_GUIDE.md** - Detailed setup instructions
2. **Troubleshooting section** - Common problems and solutions
3. **Requirements** - Python 3.8+, internet connection

---

## 📄 License

Free to use for personal portfolio tracking.

---

## 🙏 Acknowledgments

- **Streamlit** - For the amazing dashboard framework
- **yfinance** - For Yahoo Finance API access
- **Pandas** - For data manipulation

---

## 📝 Changelog

### v1.0.0 (Feb 2026)
- ✅ Initial release
- ✅ Real-time price tracking
- ✅ Auto-refresh functionality
- ✅ P&L calculations
- ✅ CSV-based storage
- ✅ Inline trade editing
- ✅ Portfolio summary metrics
- ✅ Color-coded indicators

---

**Built with ❤️ for retail investors**

Track your gains, minimize your losses! 📈💰
