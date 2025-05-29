import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import run_analyzer

def dataframe_to_table(parent, df, width=600, height=300):
    tree = ttk.Treeview(parent, columns=list(df.columns), show='headings', height=min(len(df), 20))
    for col in df.columns:
        tree.heading(col, text=col)
        tree.column(col, width=int(width/len(df.columns)), anchor='center')
    for _, row in df.iterrows():
        tree.insert('', tk.END, values=list(row))
    tree.pack(fill=tk.BOTH, expand=True, pady=10)
    return tree

def run_gui():

    # Analyze the data
    df, rent_per_m2_stats = run_analyzer.analyze()

    # Create the main application window
    root = tk.Tk()
    root.title("Property Analyzer")
    root.geometry("1200x800")  # Set a fixed size for the window
    root.resizable(False, False)  # Disable resizing

    # Left frame for user input
    left_frame = tk.Frame(root, padx=10, pady=10)
    left_frame.pack(side=tk.LEFT, fill=tk.Y)
    tk.Label(left_frame, text="Calculation tool with User Input", font=("Arial", 12, "bold")).pack(pady=10)

    # Add the labels and textboxes for user input
    tk.Label(left_frame, text="Enter the area name:", font=("Arial", 11)).pack(pady=(20, 2))
    area_input = tk.Entry(left_frame, width=30)
    area_input.pack(pady=(0, 10))
    tk.Label(left_frame, text="Enter the price listed:", font=("Arial", 11)).pack(pady=(20, 2))
    price_input = tk.Entry(left_frame, width=30)
    price_input.pack(pady=(0, 10))
    tk.Label(left_frame, text="Enter the floor size(m2):", font=("Arial", 11)).pack(pady=(20, 2))
    size_input = tk.Entry(left_frame, width=30)
    size_input.pack(pady=(0, 10))

    # Add a Text widget to display results
    # Add a Text widget for displaying results
    result_textbox = tk.Text(left_frame, width=70, height=20, font=("Arial", 11))
    result_textbox.pack(pady=(10, 10))

    # Function to run when button is clicked
    def run_income_approach():
        title = area_input.get()
        try:
            price = float(price_input.get())
            floor_size = float(size_input.get())
        except ValueError:
            tk.messagebox.showerror("Input Error", "Please enter valid numbers for price and floor size.")
            return

        # Import the function to calculate income approach
        from run_analyzer import calculate_income_approach

        try:
            results = calculate_income_approach(title, price, floor_size, rent_per_m2_stats)
            # Display results (for example, in a popup)
            result_text = (
                f" \n"
                f"Results for {title} at a price of {price:.2f}:\n"
                f"Monthly Gross Rent Income: {results[0]:,.2f}\n"
                f"Monthly Gross Rent Income Stddev: {results[1]:,.2f}\n"
                f"Annual Gross Rent Income: {results[2]:,.2f}\n"
                f"Annual Gross Rent Income Stddev: {results[3]:,.2f}\n"
                f"Capitalization Rate: {results[4]:.2f}%\n"
                f"Capitalization Rate Stddev: {results[5]:.2f}%\n"
            )
            #tk.messagebox.showinfo("Income Approach Results", result_text)
            # Clear and insert the result into the Text widget
            # result_textbox.delete("1.0", tk.END)
            result_textbox.insert(tk.END, result_text)
        except Exception as e:
            tk.messagebox.showerror("Calculation Error", str(e))

    # Add the button to run the calculation
    income_button = tk.Button(left_frame, text="Calculate Metrics", command=run_income_approach)
    income_button.pack(pady=(0, 20))

    # --- Scrollable right frame setup ---
    right_canvas = tk.Canvas(root, width =600)
    right_canvas.pack(side=tk.RIGHT, fill=tk.BOTH, expand=False)

    scrollbar = tk.Scrollbar(root, orient="vertical", command=right_canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    right_canvas.configure(yscrollcommand=scrollbar.set)
    right_canvas.bind('<Configure>', lambda e: right_canvas.configure(scrollregion=right_canvas.bbox("all")))

    right_frame = tk.Frame(right_canvas, padx=10, pady=10)
    right_canvas.create_window((0, 0), window=right_frame, anchor="nw")

    # Top label for analysis results
    tk.Label(right_frame, text="Analysis Results of properties", font=("Arial", 12, "bold")).pack(pady=10)

    # Add your tables with labels
    tk.Label(right_frame, text="Top 15 Properties by Mean Rent per m2", font=("Arial", 11, "bold")).pack(pady=(10,2))
    dataframe_to_table(right_frame, run_analyzer.top_15_mean_rent_per_m2(rent_per_m2_stats))
    tk.Label(right_frame, text="Top 15 Properties by Maximum Rent per m2", font=("Arial", 11, "bold")).pack(pady=(10,2))
    dataframe_to_table(right_frame, run_analyzer.top_15_rent_per_m2(rent_per_m2_stats))
    tk.Label(right_frame, text="Lowest 15 Properties by Mean Rent per m2", font=("Arial", 11, "bold")).pack(pady=(10,2))
    dataframe_to_table(right_frame, run_analyzer.low_15_mean_rent_per_m2(rent_per_m2_stats))
    tk.Label(right_frame, text="Lowest 15 Properties by Minimum Rent per m2", font=("Arial", 11, "bold")).pack(pady=(10,2))
    dataframe_to_table(right_frame, run_analyzer.low_15_min_rent_per_m2(rent_per_m2_stats))
    tk.Label(right_frame, text="Top 15 Properties by Standard Deviation in rent per m2", font=("Arial", 11, "bold")).pack(pady=(10,2))
    dataframe_to_table(right_frame, run_analyzer.top_15_stddev_rent_per_m2(rent_per_m2_stats))
    tk.Label(right_frame, text="Lowest 15 Properties by Standard Deviation in rent per m2", font=("Arial", 11, "bold")).pack(pady=(10,2))
    dataframe_to_table(right_frame, run_analyzer.low_15_stddev_rent_per_m2(rent_per_m2_stats))

    # Quit button at the bottom
    button_frame = tk.Frame(left_frame)
    button_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=10)
    quit_button = tk.Button(button_frame, text="Quit Application", command=root.quit)
    quit_button.pack(anchor="center", padx = 10, expand=False)

    root.mainloop()

if __name__ == "__main__":
    run_gui()