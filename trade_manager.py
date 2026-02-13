import csv
import os
from datetime import datetime

class TradeManager:
    def __init__(self, filename='trades.csv'):
        self.filename = filename
        self.headers = [
            'Stock Name', 'Trade Type', 'Entry Price', 'Entry Date',
            'Buy Date', 'Sell Date', 'Sell Price', 'Sell Target 1',
            'Sell Target 2', 'Sell Target 3', 'P&L %', 'P&L Amt',
            'Portfolio Impact'
        ]
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        if not os.path.exists(self.filename):
            with open(self.filename, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(self.headers)

    def add_trade(self, trade_data):
        # Calculate P&L if sell price exists
        if trade_data.get('Sell Price') and trade_data.get('Entry Price'):
            try:
                entry_price = float(trade_data['Entry Price'])
                sell_price = float(trade_data['Sell Price'])
                quantity = float(trade_data.get('Quantity', 1)) # Assuming 1 if not specified

                pnl_amt = (sell_price - entry_price) * quantity
                pnl_percent = ((sell_price - entry_price) / entry_price) * 100
                
                trade_data['P&L Amt'] = f"{pnl_amt:.2f}"
                trade_data['P&L %'] = f"{pnl_percent:.2f}%"

                # Calculate Portfolio Impact (Placeholder logic, needs user's total portfolio value)
                total_portfolio_value = 100000 # Example default
                impact = (pnl_amt / total_portfolio_value) * 100
                trade_data['Portfolio Impact'] = f"{impact:.2f}%"

            except ValueError:
                print("Error calculating P&L: Invalid price format.")

        with open(self.filename, 'a', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.headers)
            # Filter out extra keys not in headers
            row = {k: trade_data.get(k, '') for k in self.headers}
            writer.writerow(row)
        print("Trade added successfully!")

    def add_trade_interactive(self):
        print("Enter trade details:")
        trade_data = {}
        trade_data['Stock Name'] = input("Stock Name: ")
        trade_data['Trade Type'] = input("Trade Type (Long/Short): ")
        trade_data['Entry Price'] = float(input("Entry Price: "))
        trade_data['Entry Date'] = input("Entry Date (YYYY-MM-DD): ")
        trade_data['Buy Date'] = input("Buy Date (YYYY-MM-DD): ")
        
        # Optional fields
        sell_price = input("Sell Price (Press Enter if not sold yet): ")
        if sell_price:
            trade_data['Sell Price'] = float(sell_price)
            trade_data['Sell Date'] = input("Sell Date (YYYY-MM-DD): ")
        
        trade_data['Sell Target 1'] = input("Sell Target 1: ")
        trade_data['Sell Target 2'] = input("Sell Target 2: ")
        trade_data['Sell Target 3'] = input("Sell Target 3: ")
        
        self.add_trade(trade_data)

    def list_trades(self):
        if not os.path.exists(self.filename):
            print("No trades found.")
            return

        with open(self.filename, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            print(f"{'Stock':<10} {'Type':<10} {'Entry':<10} {'Sell':<10} {'P&L %':<10} {'P&L Amt':<10} {'Impact':<10}")
            print("-" * 75)
            for row in reader:
                print(f"{row.get('Stock Name', ''):<10} {row.get('Trade Type', ''):<10} {row.get('Entry Price', ''):<10} {row.get('Sell Price', ''):<10} {row.get('P&L %', ''):<10} {row.get('P&L Amt', ''):<10} {row.get('Portfolio Impact', ''):<10}")

if __name__ == "__main__":
    manager = TradeManager()
    
    while True:
        print("\n--- Trade Tracker ---")
        print("1. Add Trade")
        print("2. List Trades")
        print("3. Exit")
        
        choice = input("Select an option: ")
        
        if choice == '1':
            manager.add_trade_interactive()
        elif choice == '2':
            manager.list_trades()
        elif choice == '3':
            break
        else:
            print("Invalid choice. Please try again.")
