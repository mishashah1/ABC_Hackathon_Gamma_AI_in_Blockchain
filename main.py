# main.py
import tkinter as tk
from tkinter import messagebox
import subprocess

# Main window for selecting between two options
def main_window():
    window = tk.Tk()
    window.title("Cryptocurrency Tool")
    window.geometry("400x200")
    
    # Button to open the statistics GUI
    def open_statistics_gui():
        subprocess.Popen(["python", "1.py"])  # Opens the statistics GUI
    
    btn_statistics = tk.Button(window, text="Open Statistics GUI", command=open_statistics_gui)
    btn_statistics.pack(pady=20)
    
    # Button to open the trading bot GUI
    def open_trading_bot_gui():
        subprocess.Popen(["python", "2.py"])  # Opens the trading bot GUI
    
    btn_trading_bot = tk.Button(window, text="Open Trading Bot", command=open_trading_bot_gui)
    btn_trading_bot.pack(pady=20)

    # Button to open the user registration and crypto purchase GUI
    def open_user_gui():
        subprocess.Popen(["python", "3.py"])  # Opens the user management GUI
    
    btn_user_management = tk.Button(window, text="Open User Management", command=open_user_gui)
    btn_user_management.pack(pady=20)

    window.mainloop()

# Run the program
if __name__ == "__main__":
    main_window()
