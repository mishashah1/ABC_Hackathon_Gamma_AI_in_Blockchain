# 2.py
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import yfinance as yf
import tkinter as tk
from tkinter import messagebox

# Set up the style for seaborn
sns.set(style="whitegrid")

# Function to fetch historical price data
def fetch_data(symbol, period="1mo", interval="5m"):
    df = yf.download(symbol, period=period, interval=interval)
    return df

# Function to calculate moving averages
def calculate_moving_averages(df, short_window=5, long_window=20):
    df['Short_MA'] = df['Close'].rolling(window=short_window).mean()
    df['Long_MA'] = df['Close'].rolling(window=long_window).mean()
    return df

# Function to simulate trading
def trade_bot(symbol, initial_investment, trade_duration):
    df = fetch_data(symbol)
    df = calculate_moving_averages(df)

    balance = initial_investment
    crypto_holding = 0
    entry_price = 0

    for index, row in df.iterrows():
        if row['Short_MA'] > row['Long_MA'] and balance > 0:
            entry_price = row['Close']
            crypto_holding = balance / entry_price
            balance = 0
            print(f"Purchased at {entry_price:.2f} on {index.date()}")

        elif row['Short_MA'] < row['Long_MA'] and crypto_holding > 0:
            exit_price = row['Close']
            balance = crypto_holding * exit_price
            profit_percentage = ((exit_price - entry_price) / entry_price) * 100
            print(f"Sold at {exit_price:.2f} on {index.date()}, Profit: {profit_percentage:.2f}%")
            crypto_holding = 0

        if (index - df.index[0]).days >= trade_duration:
            break

    return balance, crypto_holding

# Function to plot the price and moving averages
def plot_graph(df):
    plt.figure(figsize=(14, 7))
    sns.lineplot(data=df, x=df.index, y='Close', label='Close Price', color='blue')
    sns.lineplot(data=df, x=df.index, y='Short_MA', label='Short MA', color='orange')
    sns.lineplot(data=df, x=df.index, y='Long_MA', label='Long MA', color='green')
    plt.title('Cryptocurrency Price with Moving Averages')
    plt.xlabel('Date')
    plt.ylabel('Price (USD)')
    plt.legend()
    plt.show()

# Create a trading bot GUI
def create_trading_bot_gui():
    trading_bot_window = tk.Toplevel()
    trading_bot_window.title("Trading Bot")
    trading_bot_window.geometry("400x300")
    
    tk.Label(trading_bot_window, text="Initial Investment (USD):").pack(pady=5)
    entry_investment = tk.Entry(trading_bot_window)
    entry_investment.pack(pady=5)
    
    tk.Label(trading_bot_window, text="Trade Duration (Days):").pack(pady=5)
    entry_duration = tk.Entry(trading_bot_window)
    entry_duration.pack(pady=5)
    
    def start_trading_bot():
        symbol = "BTC-USD"
        try:
            initial_investment = float(entry_investment.get())
            trade_duration = int(entry_duration.get())

            df = fetch_data(symbol)
            df = calculate_moving_averages(df)
            plot_graph(df)

            final_balance, remaining_crypto = trade_bot(symbol, initial_investment, trade_duration)

            messagebox.showinfo("Trading Bot Results", 
                                f"Final Balance: {final_balance:.2f} USD\n"
                                f"Remaining Crypto Holding: {remaining_crypto:.4f} BTC" if remaining_crypto > 0 else "All crypto sold.")
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numerical values.")
    
    btn_start = tk.Button(trading_bot_window, text="Start Trading Bot", command=start_trading_bot)
    btn_start.pack(pady=20)

# Entry point for standalone execution (if needed)
if __name__ == "__main__":
    root = tk.Tk()
    create_trading_bot_gui()
    root.mainloop()
