from tkinter import *
from tkinter import filedialog, messagebox, ttk
import pandas as pd

def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv"), ("Excel Files", "*.xlsx")])
    if file_path:
        entry_box.delete(0, END)
        entry_box.insert(0, file_path)

def eda():
    file_path = entry_box.get()
    if not file_path:
        messagebox.showwarning("File Warning", "No file is found")
    else:
        try:
            file = pd.read_csv(file_path) if file_path.endswith('.csv') else pd.read_excel(file_path)
            display_summary(file)
            display_data_preview(file)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

def display_summary(data):
    summary = data.describe()

    txt_field.config(state=NORMAL)
    txt_field.delete(1.0, END)

    txt_field.insert(END, "Summary Statistics\n", "header")
    txt_field.insert(END, "-" * 80 + "\n", "separator")

    # Format column names
    txt_field.insert(END, "{:<15}".format("Metric"), "columns")
    for col in summary.columns:
        txt_field.insert(END, "{:<15}".format(col), "columns")
    txt_field.insert(END, "\n" + "-" * 80 + "\n", "separator")

    # Insert each row of the summary
    for index, row in summary.iterrows():
        txt_field.insert(END, "{:<15}".format(index), "rows")
        for val in row:
            txt_field.insert(END, "{:<15.2f}".format(val), "rows")
        txt_field.insert(END, "\n", "rows")

    txt_field.insert(END, "-" * 80 + "\n\n", "separator")

def display_data_preview(data):
    txt_field.insert(END, "Data Preview (First 10 Rows)\n", "header")
    txt_field.insert(END, "-" * 80 + "\n", "separator")

    # Format column names
    for col in data.columns:
        txt_field.insert(END, "{:<15}".format(col), "columns")
    txt_field.insert(END, "\n" + "-" * 80 + "\n", "separator")

    # Display the first 10 rows
    for i, row in data.head(10).iterrows():
        for val in row:
            txt_field.insert(END, "{:<15}".format(str(val)), "rows")
        txt_field.insert(END, "\n", "rows")

    txt_field.insert(END, "-" * 80 + "\n\n", "separator")

    txt_field.config(state=DISABLED)

# Set up the main window
win = Tk()
win.title("EDA Tool")
win.geometry("900x700")
win.configure(bg="#f0f0f0")

# Adding styles
style = ttk.Style()
style.configure("TButton", font=("Arial", 12), padding=10)
style.configure("TLabel", font=("Arial", 14), background="#f0f0f0")
style.configure("TEntry", font=("Arial", 12), padding=5)

# Label and Entry
label = ttk.Label(win, text="Enter your file below")
label.pack(pady=10)

entry_box = ttk.Entry(win, width=60)
entry_box.pack(ipady=5)

# Browse File Button
browse_button = ttk.Button(win, text="Browse File", command=open_file,  compound=LEFT)
browse_button.pack(pady=10)

# EDA Button
eda_button = ttk.Button(win, text="Perform EDA", command=eda,  compound=LEFT)
eda_button.pack(pady=10)

# Summary Text Field with Scrollbars
txt_frame = Frame(win)
txt_frame.pack(pady=20, padx=20, fill=BOTH, expand=True)

txt_field = Text(txt_frame, height=30, wrap=NONE, font=("Courier New", 12))
txt_field.pack(side=LEFT, fill=BOTH, expand=True)

# Adding Scrollbars
y_scrollbar = Scrollbar(txt_frame, orient=VERTICAL, command=txt_field.yview)
y_scrollbar.pack(side=RIGHT, fill=Y)
txt_field.config(yscrollcommand=y_scrollbar.set)

x_scrollbar = Scrollbar(win, orient=HORIZONTAL, command=txt_field.xview)
x_scrollbar.pack(side=BOTTOM, fill=X)
txt_field.config(xscrollcommand=x_scrollbar.set)

# Custom tags for formatting in the Text widget
txt_field.tag_configure("header", font=("Arial", 16, "bold"), foreground="blue", justify="center")
txt_field.tag_configure("columns", font=("Courier New", 12, "bold"), foreground="black")
txt_field.tag_configure("rows", font=("Courier New", 12), foreground="black")
txt_field.tag_configure("separator", font=("Courier New", 12), foreground="grey")

# Run the application
win.mainloop()
