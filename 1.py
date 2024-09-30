import yfinance as yf
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from tkcalendar import DateEntry  # Import DateEntry from tkcalendar

# Define colors for each cryptocurrency plot
crypto_colors = {
    "BTC": "#ff9900",  # Bitcoin
    "ETH": "#3c3c3d",  # Ethereum
    "LTC": "#b5b5b5",  # Litecoin
    "XRP": "#4a90e2",  # Ripple
    "ADA": "#3cc8b8",  # Cardano
}

# Function to get cryptocurrency data for multiple cryptos
def get_multiple_crypto_data(crypto_symbols, start_date, end_date):
    data = {}
    for symbol in crypto_symbols:
        try:
            data[symbol] = yf.download(symbol + "-USD", start=start_date, end=end_date)['Adj Close']
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch data for {symbol}: {e}")
    return pd.DataFrame(data)

# Normalize data using Min-Max Scaling to bring all prices to a similar range
def normalize_data(data):
    scaler = MinMaxScaler()
    scaled_data = pd.DataFrame(scaler.fit_transform(data), columns=data.columns, index=data.index)
    return scaled_data

# Function to handle the button click event for fetching and plotting crypto data
def fetch_and_plot(frame_scrollable):
    selected_indices = listbox.curselection()
    crypto_symbols = [cryptos[i] for i in selected_indices]
    
    start_date = entry_start_date.get_date().strftime('%Y-%m-%d')  # Format date as YYYY-MM-DD
    end_date = entry_end_date.get_date().strftime('%Y-%m-%d')      # Format date as YYYY-MM-DD

    if not crypto_symbols or not start_date or not end_date:
        messagebox.showerror("Input Error", "Please fill in all fields.")
        return

    crypto_data = get_multiple_crypto_data(crypto_symbols, start_date, end_date)

    if not crypto_data.empty:
        normalized_crypto_data = normalize_data(crypto_data)
        plot_all_patterns(normalized_crypto_data, frame_scrollable, crypto_symbols)
    else:
        messagebox.showerror("Error", "No data available for the selected cryptocurrencies and date range.")

# Plot all chart patterns and embed them into Tkinter window
def plot_all_patterns(crypto_data, scroll_frame, crypto_symbols):
    # Clear the previous content in the scrollable frame
    for widget in scroll_frame.winfo_children():
        widget.destroy()

    # Create a figure with multiple subplots for each chart pattern
    fig, axs = plt.subplots(8, 2, figsize=(12, 20))  # 8 rows for patterns, 2 columns for bullish and bearish

    patterns = [
        ("Bullish Flag", 0, 0),
        ("Bearish Flag", 0, 1),
        ("Bullish Pennant", 1, 0),
        ("Bearish Pennant", 1, 1),
        ("Ascending Triangle", 2, 0),
        ("Descending Triangle", 2, 1),
        ("Symmetrical Triangle", 3, 0),
        ("Head and Shoulders", 3, 1),
        ("Rising Wedge", 4, 0),
        ("Falling Wedge", 4, 1),
        ("Bullish Rectangle", 5, 0),
        ("Bearish Rectangle", 5, 1),
        ("Double Top", 6, 0),
        ("Double Bottom", 6, 1),
        ("Triple Top", 7, 0),
        ("Triple Bottom", 7, 1),
    ]

    # Loop through each pattern and plot the data for all selected cryptocurrencies
    for title, row, col in patterns:
        for symbol in crypto_symbols:
            sns.lineplot(data=crypto_data[symbol], ax=axs[row, col], label=symbol, color=crypto_colors[symbol])
        axs[row, col].set_title(title)
        axs[row, col].legend(title="Cryptocurrency")

    # Adjust layout
    plt.tight_layout()

    # Embed the plot into Tkinter
    canvas = FigureCanvasTkAgg(fig, master=scroll_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

# Function to create a scrollable frame for displaying plots
def create_scrollable_frame(parent):
    # Create a canvas to add scrolling capability
    canvas = tk.Canvas(parent)
    scroll_y = tk.Scrollbar(parent, orient="vertical", command=canvas.yview)
    
    # Create a frame inside the canvas to hold the content
    scroll_frame = tk.Frame(canvas)
    
    # Configure the scrollable area
    scroll_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
    canvas.configure(yscrollcommand=scroll_y.set)

    # Pack the canvas and scrollbar into the parent frame
    canvas.pack(side="left", fill="both", expand=True)
    scroll_y.pack(side="right", fill="y")

    return scroll_frame

# Main function to set up the Tkinter GUI
def create_gui():
    window = tk.Tk()
    window.title("Cryptocurrency Analysis")
    window.geometry("1700x800")  # Increase the size for better viewing of plots
    window.configure(bg="#f0f0f0")  # Set a light background color

    # Frame to hold the input fields and options on the left
    frame_input = tk.Frame(window, bg="#ffffff", bd=2, relief=tk.RAISED)
    frame_input.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

    # Crypto Symbols dropdown list
    global cryptos, listbox
    cryptos = ["BTC", "ETH", "LTC", "XRP", "ADA"]

    lbl_symbols = ttk.Label(frame_input, text="Select Cryptocurrencies:", font=("Helvetica", 12), background="#ffffff")
    lbl_symbols.grid(row=0, column=0, padx=5, pady=5)

    listbox = tk.Listbox(frame_input, selectmode="multiple", height=10, exportselection=0, font=("Helvetica", 12))
    for crypto in cryptos:
        listbox.insert(tk.END, crypto)
    listbox.grid(row=0, column=1, padx=5, pady=5)

    # Start Date input with DateEntry
    lbl_start_date = ttk.Label(frame_input, text="Start Date:", font=("Helvetica", 12), background="#ffffff")
    lbl_start_date.grid(row=1, column=0, padx=5, pady=5)
    global entry_start_date
    entry_start_date = DateEntry(frame_input, width=20, background='darkblue', foreground='white', borderwidth=2, font=("Helvetica", 12))
    entry_start_date.grid(row=1, column=1, padx=5, pady=5)

    # End Date input with DateEntry
    lbl_end_date = ttk.Label(frame_input, text="End Date:", font=("Helvetica", 12), background="#ffffff")
    lbl_end_date.grid(row=2, column=0, padx=5, pady=5)
    global entry_end_date
    entry_end_date = DateEntry(frame_input, width=20, background='darkblue', foreground='white', borderwidth=2, font=("Helvetica", 12))
    entry_end_date.grid(row=2, column=1, padx=5, pady=5)

    # Fetch and Plot button
    btn_fetch = ttk.Button(frame_input, text="Fetch and Plot Data", 
                           command=lambda: fetch_and_plot(frame_scrollable), style='TButton')
    btn_fetch.grid(row=3, columnspan=2, pady=10)

    # Set button style
    style = ttk.Style()
    style.configure('TButton', font=('Helvetica', 12), padding=5, background='#007bff', foreground='black')  # Changed foreground to black
    style.map('TButton', background=[('active', '#0056b3')])  # Button color on hover

    # Create a frame for plots on the right side
    frame_plot = tk.Frame(window, bg="#f0f0f0", width=800, height=800)
    frame_plot.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    # Create a scrollable frame inside the plot frame
    global frame_scrollable
    frame_scrollable = create_scrollable_frame(frame_plot)

    window.mainloop()

# Run the GUI
create_gui()
