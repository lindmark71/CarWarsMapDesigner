import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

class DlgAddPolygon(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.title("Add Polygon")
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

        self.label_point_list = tk.Label(self, text="List of points: Comma delimited pairs of points", anchor="w")
        self.label_point_list.grid(row=0, column=0, sticky="w")

        self.var_point_list = tk.StringVar(value="")
        self.entry_point_list = ttk.Entry(self, textvariable=self.var_point_list, width=50)
        self.entry_point_list.grid(row=1, column=0, sticky="w", columnspan=2)

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
        ok_button.grid(row=3, column=0)

        # Cancel button
        cancel_button = ttk.Button(self, text="Cancel", command=self._on_cancel)
        cancel_button.grid(row=3, column=1)

    def on_select_color(self, *args):
       """Gather the selected value from the dropdown and store it in the member variable"""
       self.selected_color = self.color_dropdown.get()

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
