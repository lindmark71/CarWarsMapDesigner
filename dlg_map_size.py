import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox


class DlgMapSize(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.title("Set Map Size")
        # Center the dialog on the parent window (optional)
        self.transient(parent)
        self.grab_set()  # Make it modal
        self.protocol("WM_DELETE_WINDOW", self.on_closing) # Handle window close button

        # Set the dialog to be centered on the parent (optional)
        self.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() // 2) - (self.winfo_width() // 2)
        y = parent.winfo_y() + (parent.winfo_height() // 2) - (self.winfo_height() // 2)
        self.geometry(f"+{x}+{y}")

        # Add widgets to the dialog (e.g., labels, entry fields, buttons)
        self.label_map_x = tk.Label(self, text="Map X:", anchor="w")
        self.label_map_x.grid(row=0, column=0, padx=10, pady=10)

        self.var_map_x_qty = tk.IntVar(value=1)
        self.entry_map_x = ttk.Entry(self, textvariable=self.var_map_x_qty, width=5)
        self.entry_map_x.grid(row=0, column=1, padx=10, pady=10)

        self.label_map_y = tk.Label(self, text="Map Y:", anchor="w")
        self.label_map_y.grid(row=1, column=0, padx=10, pady=10)

        self.var_map_y_qty = tk.IntVar(value=1)
        self.entry_map_y = ttk.Entry(self, textvariable=self.var_map_y_qty, width=5)
        self.entry_map_y.grid(row=1, column=1, padx=10, pady=10)

        # OK button
        ok_button = ttk.Button(self, text="Ok", command=self._on_ok)
        ok_button.grid(row=2, column=0, padx=10, pady=20)

        # Cancel button
        cancel_button = ttk.Button(self, text="Cancel", command=self._on_cancel)
        cancel_button.grid(row=2, column=1, padx=10, pady=20)

    def on_closing(self):
        # You can add custom logic here before closing
        self.destroy()

    def _on_ok(self):
        self.result = True
        self.destroy()

    def _on_cancel(self):
        self.result = False
        self.destroy()

    def show(self):
        self.parent.wait_window(self) # Wait until the dialog is destroyed
        return self.result

if __name__ == '__main__':
    messagebox.showinfo("Debug Status", f"Don't try to debug this file directly.")
