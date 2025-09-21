import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

class DlgAddFloorPaint(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.title("Add Floor Paint")
        # Center the dialog on the parent window (optional)
        self.transient(parent)
        self.grab_set()  # Make it modal
        self.protocol("WM_DELETE_WINDOW", self.on_closing) # Handle window close buttons

        # Set the dialog to be centered on the parent (optional)
        self.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() // 2) - (self.winfo_width() // 2)
        y = parent.winfo_y() + (parent.winfo_height() // 2) - (self.winfo_height() // 2)
        self.geometry(f"+{x}+{y}")

        # Add widgets to the dialog (e.g., labels, entry fields, buttons)

        self.label_object_starting_x = tk.Label(self, text="Object Starting X:", anchor="w")
        self.label_object_starting_x.grid(row=0, column=0)

        self.var_object_starting_x_qty = tk.DoubleVar(value=0.0)
        self.entry_object_starting_x = ttk.Entry(self, textvariable=self.var_object_starting_x_qty, width=5)
        self.entry_object_starting_x.grid(row=0, column=1)

        self.label_object_starting_y = tk.Label(self, text="Object Starting Y:", anchor="w")
        self.label_object_starting_y.grid(row=1, column=0)

        self.var_object_starting_y_qty = tk.DoubleVar(value=0.0)
        self.entry_object_starting_y = ttk.Entry(self, textvariable=self.var_object_starting_y_qty, width=5)
        self.entry_object_starting_y.grid(row=1, column=1)

        self.selected_color = tk.StringVar()
        self.selected_color.set("Black") # Set default option

        # Options for the dropdown
        options = ["Color"
                    , "Black"
                    , "Blue"
                    , "Light Blue"
                    , "Dark Grey"
                    , "Light Gray"
                    , "Maroon"
                    , "Orange"
                    , "Purple"
                    , "Red"
                    , "Yellow"]

        # Create the dropdown widget
        self.color_dropdown = ttk.OptionMenu(self, self.selected_color, "Color", *options)
        self.color_dropdown.grid(row=2, column=0)
        self.selected_color.trace_add("write", self.on_select_color)

        # OK button
        ok_button = ttk.Button(self, text="Ok", command=self._on_ok)
        ok_button.grid(row=5, column=0)

        # Cancel button
        cancel_button = ttk.Button(self, text="Cancel", command=self._on_cancel)
        cancel_button.grid(row=5, column=1)

    def on_select_color(self, *args):
       """Gather the selected value from the dropdown and store it in the member variable"""
       self.selected_color = self.color_dropdown.cget()

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
