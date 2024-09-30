# 3.py
import bcrypt
import sqlite3
import time
import json
import random
import tkinter as tk
from tkinter import messagebox

# Create users table
def create_db():
    conn = sqlite3.connect('crypto_trading.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE,
            password TEXT,
            balance REAL DEFAULT 10000.0
        )
    ''')
    conn.commit()
    conn.close()

# Hash password
def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

# Verify password
def verify_password(stored_password, provided_password):
    return bcrypt.checkpw(provided_password.encode('utf-8'), stored_password)

# User registration
def register_user(username, password):
    conn = sqlite3.connect('crypto_trading.db')
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hash_password(password)))
        conn.commit()
        return "Registration successful."
    except sqlite3.IntegrityError:
        return "Username already exists."
    finally:
        conn.close()

# User login
def login_user(username, password):
    conn = sqlite3.connect('crypto_trading.db')
    c = conn.cursor()
    c.execute("SELECT password FROM users WHERE username = ?", (username,))
    user = c.fetchone()
    conn.close()
    
    if user and verify_password(user[0], password):
        return True
    return False

# Function to simulate fetching cryptocurrency price
def get_crypto_price(cryptocurrency):
    return random.uniform(10, 100)  # Random price between 10 and 100

# Function to buy cryptocurrency
def buy_crypto(username, cryptocurrency, amount):
    conn = sqlite3.connect('crypto_trading.db')
    c = conn.cursor()
    c.execute("SELECT balance FROM users WHERE username = ?", (username,))
    user = c.fetchone()

    if user:
        current_balance = user[0]
        total_cost = amount * get_crypto_price(cryptocurrency)

        if current_balance >= total_cost:
            new_balance = current_balance - total_cost
            c.execute("UPDATE users SET balance = ? WHERE username = ?", (new_balance, username))
            conn.commit()
            conn.close()
            return f"Successfully purchased {amount} of {cryptocurrency}. New balance: {new_balance:.2f}"
        else:
            conn.close()
            return "Insufficient balance."
    else:
        conn.close()
        return "User not found."

# Create the GUI for user registration, login, and cryptocurrency buying
def create_user_gui():
    def register():
        username = entry_username.get()
        password = entry_password.get()
        message = register_user(username, password)
        messagebox.showinfo("Registration", message)

    def login():
        username = entry_username.get()
        password = entry_password.get()
        if login_user(username, password):
            messagebox.showinfo("Login", "Login successful!")
            # Allow the user to buy crypto after login
            cryptocurrency = entry_crypto.get()
            amount = entry_amount.get()
            if amount:  # Ensure amount is provided
                try:
                    amount = float(amount)
                    message = buy_crypto(username, cryptocurrency, amount)
                    messagebox.showinfo("Transaction", message)
                except ValueError:
                    messagebox.showerror("Error", "Please enter a valid amount.")
        else:
            messagebox.showerror("Login", "Invalid username or password.")

    window = tk.Toplevel()
    window.title("Crypto Trading App")
    window.geometry("400x400")

    tk.Label(window, text="Username:").pack(pady=5)
    entry_username = tk.Entry(window)
    entry_username.pack(pady=5)

    tk.Label(window, text="Password:").pack(pady=5)
    entry_password = tk.Entry(window, show='*')
    entry_password.pack(pady=5)

    tk.Button(window, text="Register", command=register).pack(pady=10)
    tk.Button(window, text="Login", command=login).pack(pady=10)

    tk.Label(window, text="Cryptocurrency:").pack(pady=5)
    entry_crypto = tk.Entry(window)
    entry_crypto.pack(pady=5)

    tk.Label(window, text="Amount:").pack(pady=5)
    entry_amount = tk.Entry(window)
    entry_amount.pack(pady=5)

# Create the database when the program starts
create_db()

# Launch the user GUI
if __name__ == "__main__":
    create_user_gui()
    tk.mainloop()
