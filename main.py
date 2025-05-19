import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# Database setup
conn = sqlite3.connect('inventory.db')
cursor = conn.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS inventory (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    price REAL NOT NULL
)
''')
conn.commit()

# Insert item
def add_item():
    name = entry_name.get()
    quantity = entry_quantity.get()
    price = entry_price.get()

    if name and quantity and price:
        try:
            cursor.execute("INSERT INTO inventory (name, quantity, price) VALUES (?, ?, ?)",
                           (name, int(quantity), float(price)))
            conn.commit()
            messagebox.showinfo("Success", "Item added")
            display_items()
            clear_fields()
        except Exception as e:
            messagebox.showerror("Error", str(e))
    else:
        messagebox.showwarning("Warning", "All fields are required")

# Display all items
def display_items():
    for row in tree.get_children():
        tree.delete(row)

    cursor.execute("SELECT * FROM inventory")
    for row in cursor.fetchall():
        tree.insert('', 'end', values=row)

# Select item from treeview
def select_item(event):
    selected = tree.focus()
    values = tree.item(selected, 'values')
    if values:
        entry_id.delete(0, tk.END)
        entry_id.insert(0, values[0])
        entry_name.delete(0, tk.END)
        entry_name.insert(0, values[1])
        entry_quantity.delete(0, tk.END)
        entry_quantity.insert(0, values[2])
        entry_price.delete(0, tk.END)
        entry_price.insert(0, values[3])

# Update item
def update_item():
    item_id = entry_id.get()
    name = entry_name.get()
    quantity = entry_quantity.get()
    price = entry_price.get()

    if item_id and name and quantity and price:
        try:
            cursor.execute("UPDATE inventory SET name=?, quantity=?, price=? WHERE id=?",
                           (name, int(quantity), float(price), int(item_id)))
            conn.commit()
            messagebox.showinfo("Success", "Item updated")
            display_items()
            clear_fields()
        except Exception as e:
            messagebox.showerror("Error", str(e))
    else:
        messagebox.showwarning("Warning", "All fields are required")

# Delete item
def delete_item():
    item_id = entry_id.get()
    if item_id:
        cursor.execute("DELETE FROM inventory WHERE id=?", (item_id,))
        conn.commit()
        messagebox.showinfo("Deleted", "Item deleted")
        display_items()
        clear_fields()
    else:
        messagebox.showwarning("Warning", "Select an item to delete")

# Clear input fields
def clear_fields():
    entry_id.delete(0, tk.END)
    entry_name.delete(0, tk.END)
    entry_quantity.delete(0, tk.END)
    entry_price.delete(0, tk.END)

# GUI Setup
root = tk.Tk()
root.title("Inventory Management System")
root.geometry("700x500")

# Labels & Entries
tk.Label(root, text="ID").grid(row=0, column=0, padx=10, pady=10)
entry_id = tk.Entry(root)
entry_id.grid(row=0, column=1, padx=10)

tk.Label(root, text="Name").grid(row=1, column=0, padx=10, pady=10)
entry_name = tk.Entry(root)
entry_name.grid(row=1, column=1, padx=10)

tk.Label(root, text="Quantity").grid(row=2, column=0, padx=10, pady=10)
entry_quantity = tk.Entry(root)
entry_quantity.grid(row=2, column=1, padx=10)

tk.Label(root, text="Price").grid(row=3, column=0, padx=10, pady=10)
entry_price = tk.Entry(root)
entry_price.grid(row=3, column=1, padx=10)

# Buttons
tk.Button(root, text="Add Item", command=add_item).grid(row=1, column=2, padx=10)
tk.Button(root, text="Update", command=update_item).grid(row=2, column=2, padx=10)
tk.Button(root, text="Delete", command=delete_item).grid(row=3, column=2, padx=10)
tk.Button(root, text="Clear", command=clear_fields).grid(row=4, column=2, padx=10)

# Treeview (Table)
columns = ("ID", "Name", "Quantity", "Price")
tree = ttk.Treeview(root, columns=columns, show='headings')
for col in columns:
    tree.heading(col, text=col)
tree.grid(row=5, column=0, columnspan=3, padx=10, pady=20)

tree.bind("<<TreeviewSelect>>", select_item)

# Initial data load
display_items()

# Start GUI loop
root.mainloop()
