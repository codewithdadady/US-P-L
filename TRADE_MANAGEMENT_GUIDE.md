# 📊 Complete Trade Management Guide

## 🎯 ALL NEW FEATURES

Your dashboard now has **FULL TRADE MANAGEMENT** with:

✅ Open vs Closed trades tracking
✅ Realized P&L (money already made/lost)
✅ Unrealized P&L (current position profit/loss)
✅ Partial position trimming (sell 25%, 33%, 50%, etc.)
✅ Remaining capital after partial exit
✅ Price flashing (green up, red down)
✅ Today's price change
✅ Proper date formatting

---

## 📋 CSV Column Structure

Your `trades.csv` now has these columns:

| Column | Description | Example |
|--------|-------------|---------|
| **Stock Name** | Ticker symbol | AAPL |
| **Entry Date** | Buy date (YYYY-MM-DD) | 2024-01-15 |
| **Entry Price** | Your buy price | 180.50 |
| **Capital** | Initial investment | 5000 |
| **Sell Date** | Exit date (YYYY-MM-DD) | 2024-02-15 |
| **Sell Price** | Exit price | 225.00 |
| **Sell %** | How much sold (0-100) | 33 |
| **Trade Status** | OPEN, PARTIAL, or CLOSED | OPEN |
| **Sell Target 1/2/3** | Your price targets | 200, 220, 240 |

---

## 🎮 HOW TO USE

### **1️⃣ OPEN TRADE (Nothing sold yet)**

```csv
AAPL,2024-01-15,180.50,5000,,,0,OPEN,200,220,240
```

**What happens:**
- Shows **Unrealized P&L** (live profit/loss)
- Current Value updates in real-time
- Status: 🟢 Open
- Realized P&L = $0

**Example in Dashboard:**
```
Ticker: AAPL
Initial Capital: $5,000
Remaining Capital: $5,000
Current Value: $6,234 (if price is $225)
Realized P&L: $0.00
Unrealized P&L: $1,234 (24.7%)
Total P&L: $1,234 (24.7%)
Status: 🟢 Open
```

---

### **2️⃣ PARTIAL EXIT (Trimmed some %)**

```csv
TSLA,2024-02-01,200.00,3000,2024-02-15,250.00,33,PARTIAL,280,300,350
```

**What happens:**
- **Sold 33%** at $250
- **Remaining 67%** still open
- Shows BOTH realized AND unrealized P&L

**Math:**
```
Initial: $3,000 at $200/share = 15 shares

Sold 33%:
- Sold shares: 15 × 0.33 = 4.95 shares
- Sold at: $250
- Realized P&L: (250-200) × 4.95 = +$247.50 ✅

Remaining 67%:
- Remaining: 10.05 shares
- Current price: $210 (example)
- Unrealized P&L: (210-200) × 10.05 = +$100.50 🟡

Total P&L: $247.50 + $100.50 = $348.00
```

**Example in Dashboard:**
```
Ticker: TSLA
Initial Capital: $3,000
Remaining Capital: $2,010 (67% of $3,000)
Current Value: $2,110.50 (10.05 shares × $210)
Realized P&L: $247.50 (from 33% sold)
Unrealized P&L: $100.50 (from 67% remaining)
Total P&L: $348.00 (11.6%)
Status: 🟡 Partial (33% sold)
```

---

### **3️⃣ CLOSED TRADE (100% exited)**

```csv
MSFT,2024-01-10,350.00,3500,2024-02-01,420.00,100,CLOSED,,,
```

**What happens:**
- Entire position closed
- Shows **Realized P&L** only
- No more live updates
- Status: 🔒 Closed

**Math:**
```
Bought: $3,500 at $350/share = 10 shares
Sold: All 10 shares at $420
Realized P&L: (420-350) × 10 = +$700 ✅
```

**Example in Dashboard:**
```
Ticker: MSFT
Initial Capital: $3,500
Remaining Capital: $0
Current Value: $0
Realized P&L: $700.00 (20%)
Unrealized P&L: $0.00
Total P&L: $700.00 (20%)
Status: 🔒 Closed
```

---

## 💡 REAL-WORLD EXAMPLES

### **Example 1: Gradual Exit Strategy**

**Buy NVDA:**
```csv
NVDA,2024-01-20,100.00,10000,,,0,OPEN,150,200,250
```
- Bought 100 shares at $100
- Capital: $10,000

**First Trim (33% at $150):**
```csv
NVDA,2024-01-20,100.00,10000,2024-03-15,150.00,33,PARTIAL,150,200,250
```
- Sold 33 shares at $150
- Realized: (150-100) × 33 = **+$1,650** ✅
- Remaining: 67 shares

**Second Trim (another 33% at $200):**
```csv
NVDA,2024-01-20,100.00,10000,2024-03-15,175.00,66,PARTIAL,150,200,250
```
- *Note: Sell % is cumulative*
- Total sold: 66 shares (33+33)
- Average sell price: $175 (in this example)
- Realized: (175-100) × 66 = **+$4,950** ✅
- Remaining: 34 shares

**Final Exit (100%):**
```csv
NVDA,2024-01-20,100.00,10000,2024-04-20,220.00,100,CLOSED,,,
```
- Sold all 100 shares
- Average exit: $220
- Realized: (220-100) × 100 = **+$12,000** ✅

---

### **Example 2: Stop Loss Hit**

```csv
Stock Name,Entry Date,Entry Price,Capital,Sell Date,Sell Price,Sell %,Trade Status
COIN,2024-02-01,150.00,3000,2024-02-10,120.00,100,CLOSED
```

**Result:**
- Realized P&L: (120-150) × 20 shares = **-$600** ❌
- Status: 🔒 Closed
- Loss captured

---

## 📊 DASHBOARD METRICS EXPLAINED

### **Portfolio Summary (Top Cards)**

1. **💰 Total Invested**
   - Sum of ALL initial capital (open + partial + closed)
   - Example: $5,000 + $3,000 + $3,500 = $11,500

2. **📊 Current Value**
   - Value of REMAINING positions only
   - Closed trades = $0
   - Example: AAPL ($6,234) + TSLA ($2,111) = $8,345

3. **✅ Realized P&L**
   - Profit/loss from SOLD portions
   - Money already in your pocket (or lost)
   - Example: TSLA trim +$248 + MSFT closed +$700 = $948

4. **⏳ Unrealized P&L**
   - Profit/loss on REMAINING positions
   - Paper gains/losses (not yet realized)
   - Example: AAPL +$1,234 + TSLA remaining +$101 = $1,335

5. **💵 Total P&L**
   - Realized + Unrealized
   - Your total performance
   - Example: $948 + $1,335 = $2,283

---

## 🎯 HOW TO RECORD DIFFERENT SCENARIOS

### **Scenario 1: Regular Full Exit**
```csv
AAPL,2024-01-15,180.50,5000,2024-03-20,225.00,100,CLOSED
```

### **Scenario 2: Trim 50%, Hold 50%**
```csv
TSLA,2024-02-01,200.00,4000,2024-02-20,260.00,50,PARTIAL
```

### **Scenario 3: Trim 25%, Trim 25%, Hold 50%**
```csv
NVDA,2024-01-10,500.00,10000,2024-02-15,600.00,50,PARTIAL
```
*Note: Record cumulative %. First trim 25%, second trim = 50% total*

### **Scenario 4: Scale Out Completely**
```csv
MSFT,2024-01-05,350.00,7000,2024-03-15,420.00,100,CLOSED
```

### **Scenario 5: Average Down, Then Exit**
*Just add as separate entries:*
```csv
META,2024-01-15,300.00,3000,2024-04-01,380.00,100,CLOSED
META,2024-02-20,250.00,2500,2024-04-01,380.00,100,CLOSED
```

---

## 🔢 IMPORTANT RULES

1. **Sell %:**
   - 0 = Nothing sold (open)
   - 1-99 = Partial exit
   - 100 = Fully closed

2. **Sell Price:**
   - REQUIRED if Sell % > 0
   - Use average exit price if multiple sells

3. **Trade Status:**
   - OPEN = Position still active
   - PARTIAL = Some sold, some remaining
   - CLOSED = Fully exited

4. **Dates:**
   - Always use YYYY-MM-DD format
   - Entry Date required
   - Sell Date optional (only if sold)

---

## 📈 STATISTICS YOU GET

1. **🟢 Open Positions** - Active trades
2. **🟡 Partial Exits** - Trimmed but not fully closed
3. **🔒 Closed Trades** - Completed exits
4. **✅ Profitable** - Trades with positive P&L
5. **❌ Losing** - Trades with negative P&L
6. **📈 Win Rate** - % of profitable trades
7. **Avg P&L/Trade** - Average profit per position

---

## 🚀 QUICK START

1. **Open Trade:**
   - Fill: Stock Name, Entry Date, Entry Price, Capital
   - Leave: Sell Date, Sell Price, Sell % blank
   - Set: Trade Status = OPEN (or leave blank)

2. **Trim Position:**
   - Enter: Sell Date, Sell Price, Sell % (e.g., 33)
   - Set: Trade Status = PARTIAL

3. **Close Trade:**
   - Enter: Sell Date, Sell Price
   - Set: Sell % = 100, Trade Status = CLOSED

---

## ✨ EVERYTHING YOU ASKED FOR IS HERE!

✅ Open vs Closed tracking
✅ Realized P&L (money made/lost)
✅ Unrealized P&L (paper gains/losses)
✅ Partial trimming (33%, 50%, etc.)
✅ Remaining capital after trim
✅ Balance position tracking
✅ Price flashing (green/red)
✅ Today's change %
✅ Proper date formatting
✅ Fast saving
✅ Portfolio breakdown
✅ Win rate calculation

---

**Enjoy your professional trading dashboard!** 📊💰
