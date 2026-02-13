import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
import time
import plotly.graph_objects as go
import numpy as np
from calendar import month_abbr

st.set_page_config(page_title="Trading Analytics Dashboard", page_icon="📊", layout="wide")

# CSS with FLASHING ANIMATIONS
st.markdown("""
    <style>
    table {font-size: 13px !important;}
    thead tr th {
        background-color: #2d2d2d !important;
        color: white !important;
        font-weight: bold !important;
        text-align: center !important;
        padding: 10px !important;
    }
    tbody tr {background-color: transparent !important;}
    tbody tr:hover {background-color: #1e1e1e !important;}
    .stButton > button {
        border-radius: 5px;
        padding: 5px 15px;
        margin: 2px;
    }
    
    /* PRICE FLASH ANIMATIONS */
    @keyframes flash-green {
        0% { background-color: rgba(0, 255, 136, 0.4); }
        50% { background-color: rgba(0, 255, 136, 0.6); }
        100% { background-color: transparent; }
    }
    @keyframes flash-red {
        0% { background-color: rgba(255, 68, 68, 0.4); }
        50% { background-color: rgba(255, 68, 68, 0.6); }
        100% { background-color: transparent; }
    }
    .price-flash-up {
        animation: flash-green 1s ease-in-out;
        color: #00ff88 !important;
        font-weight: bold;
    }
    .price-flash-down {
        animation: flash-red 1s ease-in-out;
        color: #ff4444 !important;
        font-weight: bold;
    }
    
    /* DISABLE DIMMING */
    .stApp {
        transition: none !important;
        pointer-events: auto !important;
    }
    header, footer {
        visibility: hidden !important;
    }
    div[data-testid="stStatusWidget"], div.stSpinner {
        visibility: hidden !important;
        display: none !important;
    }
    /* Main container opacity fix */
    .main {
        opacity: 1 !important;
    }
    /* Stop any opacity changes on elements */
    .element-container, .stMarkdown, .stDataFrame, .stMetric, .stPlotlyChart {
        opacity: 1 !important;
        transition: none !important;
    }
    /* Overall app container opacity fix */
    div[data-testid="stAppViewContainer"] {
        opacity: 1 !important;
    }
    div[data-testid="stDecoration"] {
        display: none !important;
    }
    div[data-testid="stToolbar"] {
        opacity: 1 !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("📊 Trading Analytics Dashboard")
st.markdown("---")

# Initialize session state for tracking price and P&L changes
if 'previous_prices' not in st.session_state:
    st.session_state.previous_prices = {}
if 'previous_pnl' not in st.session_state:
    st.session_state.previous_pnl = {}
if 'price_flash' not in st.session_state:
    st.session_state.price_flash = {}
if 'pnl_flash' not in st.session_state:
    st.session_state.pnl_flash = {}
if 'chart_period' not in st.session_state:
    st.session_state.chart_period = 'MAX'

def parse_date_strict(date_val):
    if pd.isna(date_val) or str(date_val).strip() in ['', 'None', 'nan']:
        return ''
    date_str = str(date_val).strip()
    try:
        parsed = pd.to_datetime(date_str, dayfirst=False, errors='coerce')
        if pd.notna(parsed):
            return parsed.strftime('%Y-%m-%d')
    except:
        pass
    formats = ['%Y-%m-%d', '%d/%m/%y', '%d/%m/%Y', '%m/%d/%Y', '%m/%d/%y', '%Y/%m/%d', '%d-%m-%Y', '%d-%m-%y']
    for fmt in formats:
        try:
            parsed = datetime.strptime(date_str, fmt)
            if parsed.year < 100:
                parsed = parsed.replace(year=2000 + parsed.year)
            return parsed.strftime('%Y-%m-%d')
        except:
            continue
    return ''

def load_trades():
    try:
        df = pd.read_csv('trades.csv')
        df = df.dropna(how='all')
        required = ['Stock Name', 'Entry Date', 'Entry Price', 'Capital', 'Sell Date', 'Sell Price', 'Sell %', 'Trade Status']
        for col in required:
            if col not in df.columns:
                df[col] = ''
        df['Entry Date'] = df['Entry Date'].apply(parse_date_strict)
        df['Sell Date'] = df['Sell Date'].apply(parse_date_strict)
        return df
    except FileNotFoundError:
        df = pd.DataFrame(columns=['Stock Name', 'Entry Date', 'Entry Price', 'Capital', 'Sell Date', 'Sell Price', 'Sell %', 'Trade Status', 'Sell Target 1', 'Sell Target 2', 'Sell Target 3'])
        df.to_csv('trades.csv', index=False)
        return df

def get_stock_data(ticker):
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period='2d')
        if not hist.empty:
            current_price = round(hist['Close'].iloc[-1], 2)
            previous_close = round(hist['Close'].iloc[-2], 2) if len(hist) >= 2 else current_price
            return current_price, previous_close
        return None, None
    except:
        return None, None

def get_benchmark_history(symbol, start_date):
    try:
        ticker = yf.Ticker(symbol)
        hist = ticker.history(start=start_date, end=datetime.now())
        if not hist.empty:
            hist.index = hist.index.tz_localize(None)
        return hist
    except:
        return pd.DataFrame()

def calculate_position(row, current_price):
    try:
        entry_price = float(row['Entry Price'])
        initial_capital = float(row['Capital'])
        initial_shares = initial_capital / entry_price
        sell_pct = 0
        if 'Sell %' in row and row['Sell %'] and str(row['Sell %']).strip():
            try:
                sell_pct = float(row['Sell %'])
            except:
                sell_pct = 0
        trade_status = str(row.get('Trade Status', '')).upper().strip()
        sell_price = row.get('Sell Price', '')
        
        if trade_status == 'CLOSED' or sell_pct >= 100:
            if sell_price and str(sell_price).strip():
                sell_val = float(sell_price)
            else:
                sell_val = current_price if current_price else entry_price
            realized_pnl = (sell_val - entry_price) * initial_shares
            realized_pnl_pct = (realized_pnl / initial_capital) * 100
            return {
                'type': 'CLOSED', 'initial_capital': initial_capital, 'initial_shares': initial_shares,
                'remaining_shares': 0, 'remaining_capital': 0, 'current_value': 0,
                'realized_pnl': realized_pnl, 'realized_pnl_pct': realized_pnl_pct,
                'unrealized_pnl': 0, 'unrealized_pnl_pct': 0,
                'total_pnl': realized_pnl, 'total_pnl_pct': realized_pnl_pct,
                'avg_sell_price': sell_val, 'status': '🔒 Closed'
            }
        
        elif sell_pct > 0 and sell_pct < 100:
            if not sell_price or not str(sell_price).strip():
                sell_pct = 0
            else:
                sell_val = float(sell_price)
                sold_shares = initial_shares * (sell_pct / 100)
                sold_capital = initial_capital * (sell_pct / 100)
                realized_pnl = (sell_val - entry_price) * sold_shares
                realized_pnl_pct = (realized_pnl / sold_capital) * 100 if sold_capital > 0 else 0
                remaining_shares = initial_shares - sold_shares
                remaining_capital = initial_capital - sold_capital
                if current_price:
                    current_value = remaining_shares * current_price
                    unrealized_pnl = current_value - remaining_capital
                    unrealized_pnl_pct = (unrealized_pnl / remaining_capital) * 100 if remaining_capital > 0 else 0
                else:
                    current_value = remaining_capital
                    unrealized_pnl = 0
                    unrealized_pnl_pct = 0
                total_pnl = realized_pnl + unrealized_pnl
                total_pnl_pct = (total_pnl / initial_capital) * 100
                return {
                    'type': 'PARTIAL', 'initial_capital': initial_capital, 'initial_shares': initial_shares,
                    'remaining_shares': remaining_shares, 'remaining_capital': remaining_capital,
                    'current_value': current_value, 'realized_pnl': realized_pnl,
                    'realized_pnl_pct': realized_pnl_pct, 'unrealized_pnl': unrealized_pnl,
                    'unrealized_pnl_pct': unrealized_pnl_pct, 'total_pnl': total_pnl,
                    'total_pnl_pct': total_pnl_pct, 'avg_sell_price': sell_val,
                    'status': f'🟡 Partial ({sell_pct:.0f}% sold)'
                }
        
        if current_price:
            current_value = initial_shares * current_price
            unrealized_pnl = current_value - initial_capital
            unrealized_pnl_pct = (unrealized_pnl / initial_capital) * 100
        else:
            current_value = initial_capital
            unrealized_pnl = 0
            unrealized_pnl_pct = 0
        return {
            'type': 'OPEN', 'initial_capital': initial_capital, 'initial_shares': initial_shares,
            'remaining_shares': initial_shares, 'remaining_capital': initial_capital,
            'current_value': current_value, 'realized_pnl': 0, 'realized_pnl_pct': 0,
            'unrealized_pnl': unrealized_pnl, 'unrealized_pnl_pct': unrealized_pnl_pct,
            'total_pnl': unrealized_pnl, 'total_pnl_pct': unrealized_pnl_pct,
            'avg_sell_price': 0, 'status': '🟢 Open'
        }
    except:
        return None

def calculate_equity_curve(trades_df):
    if trades_df.empty:
        return pd.DataFrame()
    
    valid_dates = pd.to_datetime(trades_df['Entry Date'], errors='coerce').dropna()
    if valid_dates.empty:
        return pd.DataFrame()
    
    start_date = valid_dates.min()
    end_date = datetime.now()
    date_range = pd.date_range(start=start_date, end=end_date, freq='D')
    
    equity_data = []
    
    for date in date_range:
        daily_capital = 0
        daily_pnl = 0
        
        for idx, row in trades_df.iterrows():
            entry_date = pd.to_datetime(row['Entry Date'], errors='coerce')
            if pd.isna(entry_date) or date < entry_date:
                continue
            
            try:
                entry_price = float(row['Entry Price'])
                capital = float(row['Capital'])
                shares = capital / entry_price
                
                sell_date = pd.to_datetime(row['Sell Date'], errors='coerce') if row['Sell Date'] and str(row['Sell Date']).strip() else None
                
                if pd.notna(sell_date) and date >= sell_date:
                    sell_price = float(row['Sell Price']) if row['Sell Price'] and str(row['Sell Price']).strip() else entry_price
                    pnl = (sell_price - entry_price) * shares
                    daily_pnl += pnl
                else:
                    daily_capital += capital
            except:
                continue
        
        total_equity = daily_capital + daily_pnl
        equity_data.append({'Date': date, 'Equity': total_equity if total_equity > 0 else 0})
    
    df = pd.DataFrame(equity_data)
    if not df.empty:
        df['Date'] = pd.to_datetime(df['Date'])
    return df

def calculate_monthly_performance(trades_df):
    equity_curve = calculate_equity_curve(trades_df)
    if equity_curve.empty:
        return pd.DataFrame()
    
    equity_curve['YearMonth'] = pd.to_datetime(equity_curve['Date']).dt.to_period('M')
    monthly_equity = equity_curve.groupby('YearMonth').last().reset_index()
    
    monthly_returns = []
    for i in range(len(monthly_equity)):
        if i == 0:
            ret = 0
        else:
            prev_equity = monthly_equity.iloc[i-1]['Equity']
            curr_equity = monthly_equity.iloc[i]['Equity']
            ret = ((curr_equity - prev_equity) / prev_equity * 100) if prev_equity > 0 else 0
        
        period = monthly_equity.iloc[i]['YearMonth']
        monthly_returns.append({'Year': period.year, 'Month': period.month, 'Return': ret})
    
    df_monthly = pd.DataFrame(monthly_returns)
    if df_monthly.empty:
        return pd.DataFrame()
    
    pivot_table = df_monthly.pivot(index='Year', columns='Month', values='Return')
    pivot_table = pivot_table.fillna(0)
    
    month_names = {i: month_abbr[i].upper() for i in range(1, 13)}
    pivot_table = pivot_table.rename(columns=month_names)
    pivot_table['TOTAL'] = pivot_table.sum(axis=1)
    
    return pivot_table

def calculate_cagr(start_value, end_value, years):
    if start_value <= 0 or years <= 0:
        return 0
    return ((end_value / start_value) ** (1/years) - 1) * 100

def calculate_sharpe_ratio(returns, risk_free_rate=0.02):
    if len(returns) < 2:
        return 0
    excess_returns = returns - (risk_free_rate / 252)
    return (excess_returns.mean() / excess_returns.std()) * np.sqrt(252) if excess_returns.std() != 0 else 0

def calculate_max_drawdown(equity_curve):
    if equity_curve.empty:
        return 0
    cummax = equity_curve['Equity'].cummax()
    drawdown = (equity_curve['Equity'] - cummax) / cummax * 100
    return drawdown.min()

def filter_by_period(df, period):
    if df.empty:
        return df
    
    end_date = datetime.now()
    
    if period == '1D':
        start_date = end_date - timedelta(days=1)
    elif period == '1W':
        start_date = end_date - timedelta(weeks=1)
    elif period == '1M':
        start_date = end_date - timedelta(days=30)
    elif period == '6M':
        start_date = end_date - timedelta(days=180)
    elif period == 'YTD':
        start_date = datetime(end_date.year, 1, 1)
    elif period == '1Y':
        start_date = end_date - timedelta(days=365)
    elif period == '5Y':
        start_date = end_date - timedelta(days=365*5)
    else:  # MAX
        return df
    
    return df[df['Date'] >= start_date]

# Controls
col1, col2 = st.columns([1, 2])
with col1:
    auto_refresh = st.checkbox("🔄 Auto-Refresh", value=False)
with col2:
    refresh_interval = st.slider("Refresh (seconds)", 5, 60, 15)

st.markdown("---")

trades_df = load_trades()

if not trades_df.empty:
    total_invested = 0
    total_current_value = 0
    total_realized = 0
    total_unrealized = 0
    closed_trades = []
    
    display_data = []
    
    for idx, row in trades_df.iterrows():
        ticker = str(row['Stock Name']).strip().upper()
        if not ticker or ticker == 'NAN' or ticker == '0':
            continue
        
        entry_price = float(row['Entry Price'])
        entry_date = row.get('Entry Date', '')
        current_price, previous_close = get_stock_data(ticker)
        pos = calculate_position(row, current_price)
        if not pos:
            continue
        
        total_invested += pos['initial_capital']
        total_current_value += pos['current_value']
        total_realized += pos['realized_pnl']
        total_unrealized += pos['unrealized_pnl']
        
        if pos['type'] == 'CLOSED':
            closed_trades.append({'pnl': pos['realized_pnl'], 'pnl_pct': pos['realized_pnl_pct']})
        
        # Track price changes for FLASHING
        price_flash_class = ''
        if current_price:
            if ticker in st.session_state.previous_prices:
                prev_price = st.session_state.previous_prices[ticker]
                if current_price > prev_price:
                    price_flash_class = 'price-flash-up'
                    st.session_state.price_flash[ticker] = '🟢'
                elif current_price < prev_price:
                    price_flash_class = 'price-flash-down'
                    st.session_state.price_flash[ticker] = '🔴'
                else:
                    price_flash_class = ''
                    st.session_state.price_flash[ticker] = '⚪'
            st.session_state.previous_prices[ticker] = current_price
        
        # Track P&L changes for FLASHING
        pnl_flash_class = ''
        current_pnl = pos['total_pnl']
        if ticker in st.session_state.previous_pnl:
            prev_pnl = st.session_state.previous_pnl[ticker]
            if current_pnl > prev_pnl:
                pnl_flash_class = 'price-flash-up'
                st.session_state.pnl_flash[ticker] = '🟢'
            elif current_pnl < prev_pnl:
                pnl_flash_class = 'price-flash-down'
                st.session_state.pnl_flash[ticker] = '🔴'
            else:
                pnl_flash_class = ''
                st.session_state.pnl_flash[ticker] = '⚪'
        st.session_state.previous_pnl[ticker] = current_pnl
        
        # Day change
        if current_price and previous_close:
            day_change = current_price - previous_close
            day_change_pct = (day_change / previous_close) * 100
            day_str = f"🟢 +${day_change:.2f} (+{day_change_pct:.2f}%)" if day_change > 0 else f"🔴 ${day_change:.2f} ({day_change_pct:.2f}%)" if day_change < 0 else "⚪ $0.00 (0.00%)"
        else:
            day_str = "N/A"
        
        # Add flash indicator to price
        price_display = f"{st.session_state.price_flash.get(ticker, '')} ${current_price:.2f}" if current_price else 'N/A'
        
        # Add flash indicator to P&L
        pnl_display = f"{st.session_state.pnl_flash.get(ticker, '')} ${pos['total_pnl']:,.2f} ({pos['total_pnl_pct']:.2f}%)"
        
        display_data.append({
            'Ticker': ticker,
            'Entry Date': entry_date,
            'Entry Price': f"${entry_price:.2f}",
            'Current Price': price_display,
            'Today Change': day_str if pos['type'] != 'CLOSED' else 'Closed',
            'Initial Capital': f"${pos['initial_capital']:,.2f}",
            'Remaining Capital': f"${pos['remaining_capital']:,.2f}",
            'Current Value': f"${pos['current_value']:,.2f}",
            'Realized P&L': f"${pos['realized_pnl']:,.2f} ({pos['realized_pnl_pct']:.2f}%)",
            'Unrealized P&L': f"${pos['unrealized_pnl']:,.2f} ({pos['unrealized_pnl_pct']:.2f}%)",
            'Total P&L': pnl_display,
            'Status': pos['status']
        })
    
    total_pnl = total_realized + total_unrealized
    total_pnl_pct = (total_pnl / total_invested * 100) if total_invested > 0 else 0
    
    # POSITIONS TABLE
    st.subheader("💼 Current Positions")
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric("💰 Total Invested", f"${total_invested:,.2f}")
    with col2:
        st.metric("📊 Current Value", f"${total_current_value:,.2f}")
    with col3:
        st.metric("✅ Realized P&L", f"${total_realized:,.2f}")
    with col4:
        st.metric("⏳ Unrealized P&L", f"${total_unrealized:,.2f}")
    with col5:
        st.metric("💵 Total P&L", f"${total_pnl:,.2f}", delta=f"{total_pnl_pct:.2f}%")
    
    if display_data:
        df_display = pd.DataFrame(display_data)
        st.dataframe(df_display, use_container_width=True, height=300, hide_index=True)
    
    st.caption(f"⏰ Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    st.markdown("---")
    
    # EDIT TRADES
    with st.expander("✏️ Edit Trades"):
        edited_df = st.data_editor(trades_df, num_rows="dynamic", use_container_width=True, hide_index=True)
        col1, col2 = st.columns([1, 5])
        with col1:
            if st.button("💾 Save", type="primary"):
                edited_df = edited_df.dropna(subset=['Stock Name', 'Entry Price', 'Capital'])
                edited_df['Entry Date'] = edited_df['Entry Date'].apply(parse_date_strict)
                edited_df['Sell Date'] = edited_df['Sell Date'].apply(parse_date_strict)
                edited_df.to_csv('trades.csv', index=False)
                st.success("✅ Saved!")
                time.sleep(0.5)
                st.rerun()
    
    st.markdown("---")
    st.markdown("---")
    
    # PERFORMANCE ANALYTICS
    st.subheader("📊 Performance Analytics")
    
    equity_curve = calculate_equity_curve(trades_df)
    
    if not equity_curve.empty and len(equity_curve) > 1:
        start_equity = total_invested
        end_equity = total_invested + total_pnl
        days_trading = (datetime.now() - pd.to_datetime(trades_df['Entry Date'].min())).days
        years_trading = max(days_trading / 365, 0.01)
        cagr = calculate_cagr(start_equity, end_equity, years_trading)
        
        daily_returns = equity_curve['Equity'].pct_change().dropna()
        sharpe = calculate_sharpe_ratio(daily_returns)
        max_dd = calculate_max_drawdown(equity_curve)
    else:
        cagr = 0
        sharpe = 0
        max_dd = 0
    
    win_rate = (len([t for t in closed_trades if t['pnl'] > 0]) / len(closed_trades) * 100) if closed_trades else 0
    
    # METRICS
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    with col1:
        st.metric("Net Profit", f"{total_pnl_pct:.1f}%")
    with col2:
        st.metric("Total Trades", len(display_data))
    with col3:
        st.metric("Win Rate", f"{win_rate:.1f}%")
    with col4:
        st.metric("CAGR", f"+{cagr:.1f}%" if cagr > 0 else f"{cagr:.1f}%")
    with col5:
        st.metric("Sharpe Ratio", f"{sharpe:.2f}")
    with col6:
        st.metric("Max Drawdown", f"{max_dd:.1f}%")
    
    st.markdown("---")
    
    # MONTHLY PERFORMANCE
    st.subheader("📅 Monthly Performance")
    monthly_perf = calculate_monthly_performance(trades_df)
    
    if not monthly_perf.empty:
        def color_negative_red(val):
            if isinstance(val, (int, float)):
                color = '#00ff88' if val > 0 else '#ff4444' if val < 0 else 'white'
                return f'color: {color}; font-weight: bold'
            return ''
        
        styled_monthly = monthly_perf.style.applymap(color_negative_red)
        st.dataframe(styled_monthly, use_container_width=True, height=200)
    else:
        st.info("Add more trades!")
    
    st.markdown("---")
    
    # EQUITY CURVE WITH BENCHMARKS
    st.subheader("📈 Equity Curve vs Benchmarks")
    
    # TIME PERIOD SELECTOR
    col1, col2, col3, col4, col5, col6, col7, col8 = st.columns(8)
    periods = ['1D', '1W', '1M', '6M', 'YTD', '1Y', '5Y', 'MAX']
    
    for col, period in zip([col1, col2, col3, col4, col5, col6, col7, col8], periods):
        with col:
            if st.button(period, key=f"period_{period}"):
                st.session_state.chart_period = period
                st.rerun()
    
    if not equity_curve.empty:
        filtered_equity = filter_by_period(equity_curve, st.session_state.chart_period)
        
        if not filtered_equity.empty:
            start_date = filtered_equity['Date'].min()
            
            spy_hist = get_benchmark_history('SPY', start_date)
            qqq_hist = get_benchmark_history('QQQ', start_date)
            
            portfolio_start_value = filtered_equity['Equity'].iloc[0]
            portfolio_end_value = filtered_equity['Equity'].iloc[-1]
            portfolio_return = ((portfolio_end_value - portfolio_start_value) / portfolio_start_value) * 100
            
            spy_return = 0
            if not spy_hist.empty and len(spy_hist) > 0:
                spy_start_value = spy_hist['Close'].iloc[0]
                spy_end_value = spy_hist['Close'].iloc[-1]
                spy_return = ((spy_end_value - spy_start_value) / spy_start_value) * 100
            
            qqq_return = 0
            if not qqq_hist.empty and len(qqq_hist) > 0:
                qqq_start_value = qqq_hist['Close'].iloc[0]
                qqq_end_value = qqq_hist['Close'].iloc[-1]
                qqq_return = ((qqq_end_value - qqq_start_value) / qqq_start_value) * 100
            
            filtered_equity['Normalized'] = (filtered_equity['Equity'] / portfolio_start_value) * 100
            
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x=filtered_equity['Date'],
                y=filtered_equity['Normalized'],
                mode='lines',
                name=f'Portfolio ({portfolio_return:+.2f}%)',
                line=dict(color='#00ff88', width=3),
                fill='tozeroy',
                fillcolor='rgba(0, 255, 136, 0.1)'
            ))
            
            if not spy_hist.empty:
                spy_normalized = (spy_hist['Close'] / spy_start_value) * 100
                fig.add_trace(go.Scatter(
                    x=spy_hist.index,
                    y=spy_normalized,
                    mode='lines',
                    name=f'S&P 500 ({spy_return:+.2f}%)',
                    line=dict(color='#3b82f6', width=2, dash='dash')
                ))
            
            if not qqq_hist.empty:
                qqq_normalized = (qqq_hist['Close'] / qqq_start_value) * 100
                fig.add_trace(go.Scatter(
                    x=qqq_hist.index,
                    y=qqq_normalized,
                    mode='lines',
                    name=f'NASDAQ ({qqq_return:+.2f}%)',
                    line=dict(color='#f59e0b', width=2, dash='dot')
                ))
            
            fig.update_layout(
                template='plotly_dark',
                height=500,
                margin=dict(l=0, r=0, t=30, b=0),
                xaxis_title='Date',
                yaxis_title='Normalized Return (%)',
                hovermode='x unified',
                legend=dict(
                    orientation="h",
                    yanchor="top",
                    y=-0.15,
                    xanchor="center",
                    x=0.5
                )
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("#### 📊 Performance Comparison")
            comparison_data = [
                {'Index': 'Portfolio', 'Return': f"{portfolio_return:+.2f}%"},
                {'Index': 'S&P 500', 'Return': f"{spy_return:+.2f}%"},
                {'Index': 'NASDAQ', 'Return': f"{qqq_return:+.2f}%"}
            ]
            
            df_comparison = pd.DataFrame(comparison_data)
            st.dataframe(df_comparison, use_container_width=True, hide_index=True)
        else:
            st.info(f"No data for {st.session_state.chart_period}")
    else:
        st.info("Add trades!")
    
    if auto_refresh:
        time.sleep(refresh_interval)
        st.rerun()

else:
    st.warning("⚠️ No trades")
    with st.expander("✏️ Add First Trade", expanded=True):
        sample = pd.DataFrame({
            'Stock Name': ['AAPL'], 'Entry Date': ['2024-01-15'], 'Entry Price': [180.50],
            'Capital': [5000], 'Sell Date': [''], 'Sell Price': [''], 'Sell %': [0],
            'Trade Status': ['OPEN'], 'Sell Target 1': [200], 'Sell Target 2': [220], 'Sell Target 3': [240]
        })
        new_df = st.data_editor(sample, num_rows="dynamic", use_container_width=True, hide_index=True)
        if st.button("💾 Save", type="primary"):
            new_df = new_df.dropna(subset=['Stock Name', 'Entry Price', 'Capital'])
            if not new_df.empty:
                new_df['Entry Date'] = new_df['Entry Date'].apply(parse_date_strict)
                new_df.to_csv('trades.csv', index=False)
                st.success("✅ Saved!")
                time.sleep(0.5)
                st.rerun()
