#!/bin/bash

echo "🚀 Starting Stock P&L Dashboard..."
echo "=================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✅ Python3 found: $(python3 --version)"
echo ""

# Check if required packages are installed
echo "📦 Checking dependencies..."
python3 -c "import streamlit, pandas, yfinance" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "⚠️  Some packages are missing. Installing now..."
    pip3 install -r requirements.txt --break-system-packages
    if [ $? -ne 0 ]; then
        echo "❌ Failed to install packages. Please run: pip3 install -r requirements.txt"
        exit 1
    fi
fi

echo "✅ All dependencies installed"
echo ""

# Check if trades.csv exists
if [ ! -f "trades.csv" ]; then
    echo "⚠️  trades.csv not found. Creating sample file..."
    cat > trades.csv << EOF
Stock Name,Entry Date,Entry Price,Capital,Sell Date,Sell Price,Sell Target 1,Sell Target 2,Sell Target 3
AAPL,2024-01-15,180.50,5000,,,200,220,240
TSLA,2024-02-01,200.00,3000,,,250,300,350
MSFT,2024-01-20,380.00,4000,,,420,450,480
EOF
    echo "✅ Sample trades.csv created"
fi

echo ""
echo "🌐 Launching dashboard..."
echo "=================================="
echo "Dashboard will open in your browser at: http://localhost:8501"
echo "Press Ctrl+C to stop the dashboard"
echo ""

# Run streamlit
streamlit run dashboard.py
