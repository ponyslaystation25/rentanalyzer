import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pandas as pd
import run_analyzer

def dataframe_to_table(parent, df, headers, width=550, height=300):
    columns = list(df.columns) 
    if headers is None:
        headers = columns  # Use custom headers if provided

    tree = ttk.Treeview(parent, columns=columns, show='headings', height=min(len(df), 20))
    for col, headers in zip(columns, headers):
        tree.heading(col, text=headers)
        tree.column(col, width=int(width/len(columns)), anchor='center')
    
    # Configure row tags for alternating colors
    tree.tag_configure('oddrow', background="#bfc4d3")
    tree.tag_configure('evenrow', background="#DEDEDE")

    for i, (_, row) in enumerate(df.iterrows()):
        tag = 'evenrow' if i % 2 == 0 else 'oddrow'
        tree.insert('', tk.END, values=list(row), tags=(tag,))
    tree.pack(fill=tk.BOTH, expand=True, pady=10)
    return tree

def run_gui():

    # Analyze the data
    df, rent_per_m2_stats = run_analyzer.analyze()

    # Create the main application window
    root = tk.Tk()
    root.title("Property Analyzer")
    root.geometry("1300x850")  # Set a fixed size for the window
    root.resizable(False, False)  # Disable resizing
    #root.iconbitmap('src/analyzer/icon.ico')  # Set the icon for the window
    
    # Set the style for the Treeview and buttons
    style = ttk.Style()
    style.configure("Treeview.Heading", font=("Arial", 11, "bold"), background="#4a90e2")
    style.configure("Treeview", borderwidth=1, relief="flat", font=("Arial", 10), rowheight=28, background="#f0f0f0", foreground="#333333", fieldbackground="#f0f0f0")
    style.map("Treeview", background=[('selected', '#1d5798')], foreground=[('selected', 'white')]) 
    


    # Left frame for user input
    left_frame = tk.Frame(root, padx=10, pady=10)
    left_frame.pack(side=tk.LEFT, fill=tk.Y)
    tk.Label(left_frame, text="Calculation tool with User Input", font=("Arial", 16, "bold"), fg="#2a4d69" ).pack(pady=20)

    # Add the labels and textboxes for user input
    tk.Label(left_frame, text="Select the area name:", font=("Arial", 11)).pack(pady=(20, 2))
    area_names = sorted(rent_per_m2_stats['title'].unique())
    area_var = tk.StringVar()
    area_combobox = ttk.Combobox(left_frame, textvariable=area_var, values=area_names, width=28)
    area_combobox.pack(pady=(0, 10))
    area_combobox.current(0)  # Set the first area as default
    tk.Label(left_frame, text="Enter the price listed:", font=("Arial", 11)).pack(pady=(20, 2))
    price_input = tk.Entry(left_frame, width=30)
    price_input.pack(pady=(0, 10))
    tk.Label(left_frame, text="Enter the floor size(m2):", font=("Arial", 11)).pack(pady=(20, 2))
    size_input = tk.Entry(left_frame, width=30)
    size_input.pack(pady=(0, 10))

    # Add a separator before results
    #ttk.Separator(left_frame, orient='horizontal').pack(fill='x', pady=10)
    # Add a Text widget for displaying results
    result_textbox = tk.Text(left_frame, width=80, height=20, font=("Consolas", 11),bg="#f9f9f9", relief="groove", bd=2 )
    result_textbox.pack(pady=(15, 15))

    def save_note():
        note = result_textbox.get("1.0", tk.END).strip()
        if not note:
            messagebox.showinfo("No Content", "There is nothing to save.")
            return
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],
            title="Save Note"
        )
        if file_path:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(note)
            messagebox.showinfo("Saved", f"Note saved to {file_path}")


    # Function to run when button is clicked
    def run_income_approach():
        title = area_var.get()
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
                f"Results for {title} with a size of {floor_size:.2f} at a price of {price:.2f}:\n"
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
    income_button = ttk.Button(left_frame, text="Calculate Metrics", command=run_income_approach)
    income_button.pack(pady=(0, 20))

    # Add a button to save the results
    save_button = ttk.Button(left_frame, text="Save Note", command=save_note)
    save_button.pack(pady=(0, 10))

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
    tk.Label(right_frame, text="Analysis Results of properties", font=("Arial", 16, "bold"), fg="#2a4d69" ).pack(pady=15)

    # Add your tables with labels
    tk.Label(right_frame, text="Top 15 Properties by Mean Rent per m2", font=("Arial", 11, "bold")).pack(pady=(10,2))
    custom_headers = ["Area Name", "Rent (R/m²)", "Number of Rentals"]
    dataframe_to_table(right_frame, run_analyzer.top_15_mean_rent_per_m2(rent_per_m2_stats), headers = custom_headers)
    tk.Label(right_frame, text="Top 15 Properties by Maximum Rent per m2", font=("Arial", 11, "bold")).pack(pady=(10,2))
    dataframe_to_table(right_frame, run_analyzer.top_15_rent_per_m2(rent_per_m2_stats), headers = custom_headers)
    tk.Label(right_frame, text="Lowest 15 Properties by Mean Rent per m2", font=("Arial", 11, "bold")).pack(pady=(10,2))
    dataframe_to_table(right_frame, run_analyzer.low_15_mean_rent_per_m2(rent_per_m2_stats), headers = custom_headers)
    tk.Label(right_frame, text="Lowest 15 Properties by Minimum Rent per m2", font=("Arial", 11, "bold")).pack(pady=(10,2))
    dataframe_to_table(right_frame, run_analyzer.low_15_min_rent_per_m2(rent_per_m2_stats), headers = custom_headers)
    tk.Label(right_frame, text="Top 15 Properties by Standard Deviation in rent per m2", font=("Arial", 11, "bold")).pack(pady=(10,2))
    custom_headers = ["Area Name", "Std Dev in Rent (R/m²)", "Number of Rentals"]
    dataframe_to_table(right_frame, run_analyzer.top_15_stddev_rent_per_m2(rent_per_m2_stats), headers = custom_headers)
    tk.Label(right_frame, text="Lowest 15 Properties by Standard Deviation in rent per m2", font=("Arial", 11, "bold")).pack(pady=(10,2))
    dataframe_to_table(right_frame, run_analyzer.low_15_stddev_rent_per_m2(rent_per_m2_stats), headers = custom_headers)

    # Quit button at the bottom
    button_frame = tk.Frame(left_frame)
    button_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=10)
    quit_button = ttk.Button(button_frame, text="Quit Application", command=root.quit)
    quit_button.pack(anchor="center", padx = 10, expand=False)

    root.mainloop()

if __name__ == "__main__":
    run_gui()