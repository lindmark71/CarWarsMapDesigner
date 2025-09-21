import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import re
import json
import base64
import math
from io import BytesIO
from PIL import Image, ImageTk, ImageDraw # Pillow library for image handling
import numpy as np
from itertools import pairwise
from dlg_map_size import DlgMapSize
from dlg_add_rectangle import DlgAddRectangle
from dlg_add_circle import DlgAddCircle
from dlg_add_polygon import DlgAddPolygon
from dlg_add_text import DlgAddText
from dlg_add_floor_paint import DlgAddFloorPaint

class cwo_online_map_window():

    def __init__(self):
        """ Initial class, establish TKinter usage, labels, dropdowns and buttons"""
        #self.set_columns()
        self.root = tk.Tk()
        self.root.state('zoomed')
        self.root.title("Car Wars Online Map Designer: Version 08_18_2025") # Sets window title
        self.root.geometry("1600x800") # Sets window size
        self.current_file_path: str = ""
        self.current_image = None
        self.launch_client = None
        self.game_id = None
        self.client_id = None
        self.design_dict_list: list = []
        self.hz_1_thread = None
        self.base_image = None
        self.display_photo_img = None
        self.var_map_y_qty: float = 0.0
        self.var_map_x_qty: float = 0.0
        self.zoom_level: float = 1.0
        self.current_image_x = 0
        self.current_image_y = 0
        self.set_image_values()
        #Add drop down menus
        self.load_menus()
        self.main_grid = tk.Label(self.root, image="")
        self.main_grid.place(relx=0.01, rely=0.01, anchor="nw")
        # Create a Canvas
        self.canvas = tk.Canvas(self.root, bg="white")
        self.canvas.pack(side="left", fill="both", expand=True)

        # Create scrollbars
        self.v_scrollbar = tk.Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        self.v_scrollbar.pack(side="right", fill="y")

        self.h_scrollbar = tk.Scrollbar(self.root, orient="horizontal", command=self.canvas.xview)
        self.h_scrollbar.pack(side="bottom", fill="x")

        # Link scrollbars to canvas
        self.canvas.config(xscrollcommand=self.h_scrollbar.set, yscrollcommand=self.v_scrollbar.set)

        self.load_main_grid()
        
    def set_image_values(self):
        base_grid_pixel:  str = 'iVBORw0KGgoAAAANSUhEUgAAACkAAAApCAYAAACoYAD2AAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAAFiUAABYlAUlSJPAAAACGSURBVFhH7ZAxCsAwDMT8/2/5YSlZOpTCafDggxN4CXIQrqo6BlOH0N3fp1+mvUQqqJdIBfUSqaBeIhXUeyPvwtbxuiSBfjrtJVJBvUQqqJdIBfW8Iu/C1vG6JIF+Ou0lUkG9RCqol0gF9bwi78LW8bokgX467SVSQb1EKqiXSAX1vCK3zwPkjq7CROX+0AAAAABJRU5ErkJggg=='
        black_pixel:      str = 'Qk06AAAAAAAAADYAAAAoAAAAAQAAAAEAAAABABgAAAAAAAQAAAAlFgAAJRYAAAAAAAAAAAAAAAAAAA=='
        blue_pixel:       str = 'Qk06AAAAAAAAADYAAAAoAAAAAQAAAAEAAAABABgAAAAAAAQAAAAlFgAAJRYAAAAAAAAAAAAAzEg/AA=='
        dark_grey_pixel:  str = 'Qk06AAAAAAAAADYAAAAoAAAAAQAAAAEAAAABABgAAAAAAAQAAAAlFgAAJRYAAAAAAAAAAAAAf39/AA=='
        light_blue_pixel: str = 'Qk06AAAAAAAAADYAAAAoAAAAAQAAAAEAAAABABgAAAAAAAQAAAAlFgAAJRYAAAAAAAAAAAAA6KIAAA=='
        light_grey_pixel: str = 'Qk06AAAAAAAAADYAAAAoAAAAAQAAAAEAAAABABgAAAAAAAQAAAAlFgAAJRYAAAAAAAAAAAAAw8PDAA=='
        maroon_pixel:     str = 'Qk06AAAAAAAAADYAAAAoAAAAAQAAAAEAAAABABgAAAAAAAQAAAAlFgAAJRYAAAAAAAAAAAAAw8PDAA=='
        orange_pixel:     str = 'Qk06AAAAAAAAADYAAAAoAAAAAQAAAAEAAAABABgAAAAAAAQAAAAlFgAAJRYAAAAAAAAAAAAAJ3//AA=='
        purple_pixel:     str = 'Qk06AAAAAAAAADYAAAAoAAAAAQAAAAEAAAABABgAAAAAAAQAAAAlFgAAJRYAAAAAAAAAAAAApEmjAA=='
        red_pixel:        str = 'Qk06AAAAAAAAADYAAAAoAAAAAQAAAAEAAAABABgAAAAAAAQAAAAlFgAAJRYAAAAAAAAAAAAAJBztAA=='
        yellow_pixel:     str = 'Qk06AAAAAAAAADYAAAAoAAAAAQAAAAEAAAABABgAAAAAAAQAAAAlFgAAJRYAAAAAAAAAAAAAAPL/AA=='

        decoded_image_bytes = base64.b64decode(base_grid_pixel)
        self.base_image = Image.open(BytesIO(decoded_image_bytes))

        decoded_image_bytes = base64.b64decode(black_pixel)
        self.black_pixel_image = Image.open(BytesIO(decoded_image_bytes))

        decoded_image_bytes = base64.b64decode(blue_pixel)
        self.blue_pixel_image = Image.open(BytesIO(decoded_image_bytes))

        decoded_image_bytes = base64.b64decode(dark_grey_pixel)
        self.dark_grey_pixel_image = Image.open(BytesIO(decoded_image_bytes))

        decoded_image_bytes = base64.b64decode(light_blue_pixel)
        self.light_blue_pixel_image = Image.open(BytesIO(decoded_image_bytes))

        decoded_image_bytes = base64.b64decode(light_grey_pixel)
        self.light_grey_pixel_image = Image.open(BytesIO(decoded_image_bytes))

        decoded_image_bytes = base64.b64decode(maroon_pixel)
        self.maroon_pixel_image = Image.open(BytesIO(decoded_image_bytes))

        decoded_image_bytes = base64.b64decode(orange_pixel)
        self.orange_pixel_image = Image.open(BytesIO(decoded_image_bytes))

        decoded_image_bytes = base64.b64decode(purple_pixel)
        self.purple_pixel_image = Image.open(BytesIO(decoded_image_bytes))

        decoded_image_bytes = base64.b64decode(red_pixel)
        self.red_pixel_image = Image.open(BytesIO(decoded_image_bytes))

        decoded_image_bytes = base64.b64decode(yellow_pixel)
        self.yellow_pixel_image = Image.open(BytesIO(decoded_image_bytes))

    def launch_it(self):
        """Launch the TKinter front end"""
        self.root.mainloop()

    def load_menus(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        file_menu = tk.Menu(menubar, tearoff=0)  # tearoff=0 prevents detaching the menu
        edit_menu = tk.Menu(menubar, tearoff=0)
        construct_menu = tk.Menu(menubar, tearoff=0)
        help_menu = tk.Menu(menubar, tearoff=0)

        menubar.add_cascade(label="File", menu=file_menu)
        menubar.add_cascade(label="Edit", menu=edit_menu)
        menubar.add_cascade(label="Map Construction", menu=construct_menu)
        menubar.add_cascade(label="Help", menu=help_menu)

        file_menu.add_command(label="New", command=self.menu_file_new)
        file_menu.add_command(label="Open", command=self.menu_file_open)
        file_menu.add_command(label="Save", command=self.menu_file_save)
        file_menu.add_separator()  # Add a visual separator
        file_menu.add_command(label="Exit", command=self.menu_file_exit)

        edit_menu.add_command(label="Undo", command=self.menu_edit_undo)
        edit_menu.add_command(label="Zoom In", command=self.zoom_in)
        edit_menu.add_command(label="Zoom Out", command=self.zoom_out)

        construct_menu.add_command(label="Size Map", command=self.menu_construct_size_map)
        construct_menu.add_command(label="Add Rectangle", command=self.menu_construct_add_rectangle)
        construct_menu.add_command(label="Add Circle", command=self.menu_construct_add_circle)
        construct_menu.add_command(label="Add Polygon", command=self.menu_construct_add_polygon)
        construct_menu.add_command(label="Add Text", command=self.menu_construct_add_text)
        construct_menu.add_command(label="Add Floor Paint", command=self.menu_construct_add_floor_paint)

        help_menu.add_command(label="How Does This Work?", command=self.menu_help_how_does_this_work)
        help_menu.add_command(label="What's New", command=self.menu_help_whats_new)
        help_menu.add_command(label="What's Next", command=self.menu_help_whats_next)
        help_menu.add_command(label="About", command=self.menu_help_about)        

    def menu_file_new(self, *args):
        """Remove any loaded images and start from scratch"""
        self.design_dict_list.clear()
        self.var_map_y_qty = 1.0
        self.var_map_x_qty = 1.0
        self.resize_image()
        self.design_dict_list.clear()

    def menu_file_open(self, *args):
        self.current_file_path = filedialog.askopenfilename()  # Open file selection dialog
        self.load_map(self.current_file_path)

    def menu_file_save(self, *args):
        if self.current_file_path == "":
            self.current_file_path = filedialog.asksaveasfilename()  # Open file selection dialog
        self.save_record()
        messagebox.showinfo("File Save", f"{self.current_file_path} saved.")

    def save_record(self):
        """Save the map record to a text file"""
        with open(self.current_file_path, "w", encoding="UTF-8") as output_file:
            output_file.write(str(self.design_dict_list))     

    def load_map(self, path: str):
        """Load a map into memory to upload to the server for storage"""
        file_input_list: list = []
        file_incoming_entry: str = ""
        with open(path, "r", encoding="UTF-8") as input_file:
            file_incoming_entry = input_file.readline()

        string_of_dicts_cleaned = re.sub(r"'(?=[^:]*:)", '"', file_incoming_entry)
        string_of_dicts_cleaned = re.sub(r"(?<=:)'", '"', string_of_dicts_cleaned)
        file_input_list = json.loads(string_of_dicts_cleaned)

        self.output_map(file_input_list)

    def menu_file_exit(self, *args):
        response = messagebox.askquestion('Exit Application', 'Do you really want to exit?')
        if response == 'yes': 
            self.root.quit()

    def menu_edit_undo(self, *args):
        input_list: list = self.design_dict_list.copy() #calling the resize map will clear the self.design_dict_list
        input_list.pop() #remove the last entry
        self.output_map(input_list)

    def menu_construct_size_map(self, *args):
        """Produce a dialog box to take in map size and set the map to that size"""
        dialog = DlgMapSize(self.root)
        result = dialog.show()
        if result: #OK was pressed, make it happen
            output = dialog.var_map_x_qty.get()
            self.var_map_x_qty = output
            output = dialog.var_map_y_qty.get()
            self.var_map_y_qty = output
            self.resize_image()

    def menu_construct_add_rectangle(self, *args):
        """Produce a dialog box to take in size and starting position for a rectangle/square and add 
           the shape to the map"""
        dialog = DlgAddRectangle(self.root)
        result = dialog.show()
        if result: #OK was pressed, make it happen
            input_x_qty: float = dialog.var_object_x_qty.get()
            input_y_qty: float = dialog.var_object_y_qty.get()
            input_z_floor_qty: float = dialog.var_object_z_floor_qty.get()
            input_z_ceiling_qty: float = dialog.var_object_z_ceiling_qty.get()
            input_starting_x_qty: float = dialog.var_object_starting_x_qty.get()
            input_starting_y_qty: float = dialog.var_object_starting_y_qty.get()
            input_color: str = dialog.selected_color.get()
            if input_color == "Color":
                input_color = "Black"
            self.create_rect(input_x_qty = input_x_qty,
                             input_y_qty = input_y_qty,
                             input_z_floor_qty = input_z_floor_qty,
                             input_z_ceiling_qty = input_z_ceiling_qty,
                             input_starting_x_qty = input_starting_x_qty,
                             input_starting_y_qty = input_starting_y_qty,
                             input_color          = input_color)

    def menu_construct_add_circle(self, *args):
        """Produce a dialog box to take in size and starting position for a circle (or partial arc) and add 
           the shape to the map"""
        dialog = DlgAddCircle(self.root)
        result = dialog.show()
        if result: #OK was pressed, make it happen
            input_outer_radius_qty: float = dialog.var_object_outer_radius_qty.get()
            input_inner_radius_qty: float = dialog.var_object_inner_radius_qty.get()
            input_begin_degree_qty: float = dialog.var_object_begin_degree_qty.get()
            input_end_degree_qty:   float = dialog.var_object_end_degree_qty.get()
            input_z_floor_qty: float = dialog.var_object_z_floor_qty.get()
            input_z_ceiling_qty: float = dialog.var_object_z_ceiling_qty.get()
            input_starting_x_qty:   float = dialog.var_object_starting_x_qty.get()
            input_starting_y_qty:   float = dialog.var_object_starting_y_qty.get()
            input_color: str = dialog.selected_color.get()
            self.create_circle(input_outer_radius_qty = input_outer_radius_qty,
                               input_inner_radius_qty = input_inner_radius_qty,
                               input_begin_degree_qty = input_begin_degree_qty,
                               input_end_degree_qty = input_end_degree_qty,
                               input_z_floor_qty    = input_z_floor_qty,
                               input_z_ceiling_qty  = input_z_ceiling_qty,
                               input_starting_x_qty = input_starting_x_qty,
                               input_starting_y_qty = input_starting_y_qty,
                               input_color          = input_color)
 
    def menu_construct_add_polygon(self, *args):
        """Produce a dialog box to take in size and starting position for a generic polygon and add 
           the shape to the map"""
        dialog = DlgAddPolygon(self.root)
        result = dialog.show()
        if result: #OK was pressed, make it happen
            point_list: str = dialog.var_point_list.get()
            input_color: str = dialog.selected_color.get()
            comma_delimited_list: list = point_list.split(',')
            list_length: int = len(comma_delimited_list)
            list_of_tuples: list = []
            for loop_index in range(0, list_length, 2):
                first = comma_delimited_list[loop_index]
                second = comma_delimited_list[loop_index+1]
                list_of_tuples.append((float(first), float(second)))
            self.create_polygon(list_of_tuples = list_of_tuples,
                                input_color = input_color)

    def menu_construct_add_text(self, *args):
        """Produce a dialog box to take in a text string and starting location for text to be displayed on the map"""
        dialog = DlgAddText(self.root)
        result = dialog.show()
        if result: #OK was pressed, make it happen
            text_entry:               str = dialog.var_text.get()
            input_starting_x_qty:   float = dialog.var_object_starting_x_qty.get()
            input_starting_y_qty:   float = dialog.var_object_starting_y_qty.get()
            input_color: str = dialog.selected_color.get()
            self.create_text(text_entry = text_entry.upper(), #upper case for now
                             input_color = input_color,
                             input_starting_x_qty = input_starting_x_qty,
                             input_starting_y_qty = input_starting_y_qty)

    def menu_construct_add_floor_paint(self, *args):
        """Produce a dialog box to take in a measurement and fill in the white small squares with a custom color"""
        dialog = DlgAddFloorPaint(self.root)
        result = dialog.show()
        if result: #OK was pressed, make it happen
            input_starting_x_qty: float = dialog.var_object_starting_x_qty.get()
            input_starting_y_qty: float = dialog.var_object_starting_y_qty.get()
            input_color: str = dialog.selected_color.get()
            self.create_floor_paint(input_color = input_color,
                             input_starting_x_qty = input_starting_x_qty,
                             input_starting_y_qty = input_starting_y_qty)

    def menu_help_how_does_this_work(self, *args):
        display_info: str = "How Does This Work?\n"
        display_info += "Welcome to the Python Car Wars Map Designer.\n"
        display_info += "\n"
        display_info += "As part of the Car Wars Online system, this will help design maps for use in online gaming.\n"
        display_info += "\n"
        display_info += "Create a map, place obstacles, save and upload to the Car Wars Online Server for use.\n"
        display_info += "\n"
        display_info += "And always, remember to drive offensively.\n"
        messagebox.showinfo("How Does This Work?", display_info)

    def menu_help_about(self, *args):
        messagebox.showinfo("About", "Car Wars Online Map Designer 08_18_2025")

    def menu_help_whats_new(self, *args):
        display_info: str = "What's New with the Car Wars Online Map Designer:\n"
        display_info += "\n"
        display_info += "1) Creating and saving maps for upload.\n"
        display_info += "2) Creating objects dynamically thru a series of dialogs.\n"
        display_info += "3) Adding a color selection to object creation.\n"
        display_info += "4) Using the polygon programming to build letter crafting and installing words to maps.\n"
        display_info += "5) Add a dialog to allow the painting of the floor, leaving the small grid lines intact.\n"
        display_info += "5) Add menu items to allow for zooming in and out of the image.\n"
        display_info += "6) Edit->Undo has been implemented, redrawing the map minus the most recent object written."
        messagebox.showinfo("What's New", display_info)

    def menu_help_whats_next(self, *args):
        display_info: str = "What's Next with the Car Wars Online Map Designer:\n"
        display_info += "\n"
        display_info += "1) Stitching together object to allow for more complex creations.\n"
        display_info += "\n"
        messagebox.showinfo("What's Next", display_info)

    def output_map(self, input_list: list):
        """take the self.design_dict_list member variable and output it to the screen"""
        if len(input_list) == 0: #This is an empty list
            self.var_map_y_qty = 1
            self.var_map_x_qty = 1
            self.resize_image()
            return
        for list_entry in input_list:
            object_found: bool = False
            object_type: str = ""
            local_x_qty: str = ""
            local_y_qty: str = ""
            local_z_floor_qty: str = ""
            local_z_ceiling_qty: str = ""
            local_starting_x_qty: str = ""
            local_starting_y_qty: str = ""
            local_current_speed: str = ""
            local_top_speed: str = ""
            local_heading: str = ""
            local_orientation: str = ""
            local_color: str = ""
            local_outer_radius_qty: str = ""
            local_inner_radius_qty: str = ""
            local_begin_degree_qty: str = ""
            local_end_degree_qty: str = ""
            local_list_of_tuples: list = []
            local_text_entry: str = ""

            object_list: list = ["Rect", "Circle", "Polygon", "Text", "FloorPaint"]
            for object_key, object_entry in list_entry.items():
                if object_key == "map_size":
                    char_index = object_entry.index("X")
                    map_width_str: str = object_entry[:char_index]
                    map_height_str: str = object_entry[char_index+1:]
                    self.var_map_y_qty = int(map_height_str)
                    self.var_map_x_qty = int(map_width_str)
                    self.resize_image()
                elif object_key in object_list: 
                    object_found = True
                    object_type = object_key
                elif object_key == "local_x_qty":
                    local_x_qty = object_entry
                elif object_key == "local_y_qty":
                    local_y_qty = object_entry
                elif object_key == "local_z_floor_qty":
                    local_z_floor_qty = object_entry
                elif object_key == "local_z_ceiling_qty":
                    local_z_ceiling_qty = object_entry
                elif object_key == "local_starting_x_qty":
                    local_starting_x_qty = object_entry
                elif object_key == "local_starting_y_qty":
                    local_starting_y_qty = object_entry
                elif object_key == "current_speed":
                    local_color = object_entry
                elif object_key == "top_speed":
                    local_top_speed = object_entry
                elif object_key == "heading":
                    local_heading = object_entry
                elif object_key == "orientation":
                    local_orientation = object_entry
                elif object_key == "color":
                    local_color = object_entry
                elif object_key == "input_outer_radius_qty":
                    local_outer_radius_qty = object_entry
                elif object_key == "input_inner_radius_qty":
                    local_inner_radius_qty = object_entry
                elif object_key == "input_begin_degree_qty":
                    local_begin_degree_qty = object_entry
                elif object_key == "input_end_degree_qty":
                    local_end_degree_qty = object_entry
                elif object_key == "input_starting_x_qty":
                    local_starting_x_qty = object_entry
                elif object_key == "input_starting_y_qty":
                    local_starting_y_qty = object_entry
                elif object_key == "list_of_tuples":
                    local_list_of_tuples = object_entry
                elif object_key == "text_entry":
                    local_text_entry = object_entry

            if object_found:
                if object_type == "Rect":
                    self.create_rect(input_x_qty = local_x_qty,
                                     input_y_qty = local_y_qty,
                                     input_z_floor_qty = local_z_floor_qty,
                                     input_z_ceiling_qty = local_z_ceiling_qty,
                                     input_starting_x_qty = local_starting_x_qty,
                                     input_starting_y_qty = local_starting_y_qty,
                                     input_color          = local_color)
                if object_type == "Circle":
                    self.create_circle(input_outer_radius_qty = local_outer_radius_qty,
                                       input_inner_radius_qty = local_inner_radius_qty,
                                       input_begin_degree_qty = local_begin_degree_qty,
                                       input_end_degree_qty   = local_end_degree_qty,
                                       input_z_floor_qty      = local_z_floor_qty,
                                       input_z_ceiling_qty    = local_z_ceiling_qty,
                                       input_starting_x_qty   = local_starting_x_qty,
                                       input_starting_y_qty   = local_starting_y_qty,
                                       input_color            = local_color)
                if object_type == "Polygon":
                    self.create_polygon(list_of_tuples = local_list_of_tuples,
                                         input_color = local_color)
                if object_type == "Text":
                    self.create_text(text_entry = local_text_entry,
                                     input_color = local_color,
                                     input_starting_x_qty = local_starting_x_qty,
                                     input_starting_y_qty= local_starting_y_qty)
                if object_type == "FloorPaint":
                    self.create_floor_paint(input_color = local_color,
                                            input_starting_x_qty = local_starting_x_qty,
                                            input_starting_y_qty = local_starting_y_qty)
                            
                object_found = False

    def create_rect(self, input_x_qty: float,
                          input_y_qty: float,
                          input_z_floor_qty: float,
                          input_z_ceiling_qty: float,
                          input_starting_x_qty: float,
                          input_starting_y_qty: float,
                          input_color: str):
        """Add the object to the object list and draw it on the map"""
        fill_color = input_color.lower()
        if fill_color == "Color":
            fill_color = "Black"

        top: int = int(input_starting_y_qty * 40)
        bottom: int = int(input_y_qty * 40 + input_starting_y_qty * 40 + 1)

        left: int = int(input_starting_x_qty * 40)
        right: int = int(input_x_qty * 40 + input_starting_x_qty * 40 + 1)

        polygon_coords = [[left, top], [right, top], [right, bottom], [left, bottom]]
        draw = ImageDraw.Draw(self.current_image)
        draw.polygon(polygon_coords, fill=fill_color, outline=fill_color)

        self.display_photo_img = ImageTk.PhotoImage(self.current_image)
        #self.main_grid.configure(image=self.display_photo_img)
        self.canvas_image_id = self.canvas.create_image(0, 0, anchor="nw", image=self.display_photo_img)
        self.canvas.config(scrollregion=self.canvas.bbox(tk.ALL))
        entry_dict: dict = {}
        entry_dict["Rect"] = "Rect"
        entry_dict["local_x_qty"]          = input_x_qty
        entry_dict["local_y_qty"]          = input_y_qty
        entry_dict["local_z_floor_qty"]    = input_z_floor_qty
        entry_dict["local_z_ceiling_qty"]  = input_z_ceiling_qty
        entry_dict["local_starting_x_qty"] = input_starting_x_qty
        entry_dict["local_starting_y_qty"] = input_starting_y_qty
        entry_dict["current_speed"]        = 0
        entry_dict["top_speed"]            = 0
        entry_dict["heading"]              = 0
        entry_dict["orientation"]          = 0
        entry_dict["color"]                = fill_color
        self.design_dict_list.append(entry_dict)

    def create_circle(self, input_outer_radius_qty: float,
                            input_inner_radius_qty: float,
                            input_begin_degree_qty: float,
                            input_end_degree_qty: float,
                            input_z_floor_qty: float,
                            input_z_ceiling_qty: float,
                            input_starting_x_qty: float,
                            input_starting_y_qty: float,
                            input_color: str):
        """Add the object to the object list and draw it on the map"""
        #using starting_x and starting_y as a starting point, 
        #  begin at begin_degree, loop thru till end_degree
        #    from inner_radius, draw a dot and loop thru to outer_radius
        list_of_points: list = []

        x_coordinate: float = 0.0
        y_coordinate: float = 0.0
        fill_color = input_color.lower()
        if fill_color == "Color":
            fill_color = "Black"

        # we will presume the outer radius is always >= the inner radius, and rely on the dialog to check

        # check the degree inputs for valid data that wouldn't make sense without an adjustment
        if (input_begin_degree_qty == 0.0 and input_end_degree_qty == 0.0) or \
           (input_begin_degree_qty > input_end_degree_qty):
            input_end_degree_qty = input_end_degree_qty + 360.0

        for degree_index in range(int(input_begin_degree_qty), int(input_end_degree_qty) + 1):
            angle_radians = math.radians(degree_index)
            x_coordinate = input_starting_x_qty + input_outer_radius_qty * math.cos(angle_radians)
            y_coordinate = input_starting_y_qty + input_outer_radius_qty * math.sin(angle_radians)
            self.current_image.paste(im=self.black_pixel_image, box=(int(x_coordinate*40), int(y_coordinate*40))) #X, Y, not Y, X
            list_of_points.append((x_coordinate*40, y_coordinate*40))
        #by looping in one direction thru the outer points, and the other direction thru the inner points,
        #we make a polygon that connects both arcs.  The draw.polygon function will fill in everything in between

        for degree_index in range(int(input_end_degree_qty), int(input_begin_degree_qty) -1, -1):
            angle_radians = math.radians(degree_index)
            x_coordinate = input_starting_x_qty + input_inner_radius_qty * math.cos(angle_radians)
            y_coordinate = input_starting_y_qty + input_inner_radius_qty * math.sin(angle_radians)
            self.current_image.paste(im=self.black_pixel_image, box=(int(x_coordinate*40), int(y_coordinate*40))) #X, Y, not Y, X
            list_of_points.append((x_coordinate*40, y_coordinate*40))

        draw = ImageDraw.Draw(self.current_image)
        draw.polygon(list_of_points, fill=fill_color, outline=fill_color) #make use of other colors as necessary

        self.display_photo_img = ImageTk.PhotoImage(self.current_image)
        #self.main_grid.configure(image=self.display_photo_img)
        self.canvas_image_id = self.canvas.create_image(0, 0, anchor="nw", image=self.display_photo_img)
        self.canvas.config(scrollregion=self.canvas.bbox(tk.ALL))
        entry_dict: dict = {}
        entry_dict["Circle"] = "Circle"
        entry_dict["input_outer_radius_qty"] = input_outer_radius_qty
        entry_dict["input_inner_radius_qty"] = input_inner_radius_qty
        entry_dict["input_begin_degree_qty"] = input_begin_degree_qty
        entry_dict["input_end_degree_qty"]   = input_end_degree_qty
        entry_dict["local_z_floor_qty"]      = input_z_floor_qty
        entry_dict["local_z_ceiling_qty"]    = input_z_ceiling_qty
        entry_dict["input_starting_x_qty"]   = input_starting_x_qty
        entry_dict["input_starting_y_qty"]   = input_starting_y_qty
        entry_dict["current_speed"] = 0
        entry_dict["top_speed"]     = 0
        entry_dict["heading"]       = 0
        entry_dict["orientation"]   = 0
        entry_dict["color"]         = fill_color
        self.design_dict_list.append(entry_dict)

    def create_polygon(self, list_of_tuples: list, input_color: str):
        """Given a list of pairs of coordinates, draw a polygon on the screen, fill it in, and save
           the object to the object list"""
        #obtain the 1/4" image and duplicate it from local starting x/y to the local_x_qty and then the local_y_qty

        #Given a list of pairs of coordinates, draw a line between point 1, and point 2, 
        #repeat for point 2 and point 3, and so on until the last point
        #The last point should be the same as the first point
        #Possibly add-on, draw to the last point if the last point and the first point aren't the same
        #Add-on, fill in the middle.  The canvas fill option might not be a suitable option

        expanded_tuples: list = []
        for entry in list_of_tuples:
            x, y = entry
            x = x * 40
            y = y * 40
            expanded_tuples.append((x, y))
        fill_color = input_color.lower()
        if fill_color == "Color":
            fill_color = "Black"
            
        draw = ImageDraw.Draw(self.current_image)
        draw.polygon(expanded_tuples, fill=fill_color, outline=fill_color)

        self.display_photo_img = ImageTk.PhotoImage(self.current_image)
        #self.main_grid.configure(image=self.display_photo_img)
        self.canvas_image_id = self.canvas.create_image(0, 0, anchor="nw", image=self.display_photo_img)
        self.canvas.config(scrollregion=self.canvas.bbox(tk.ALL))
        entry_dict: dict = {}
        entry_dict["Polygon"] = "Polygon"
        entry_dict["list_of_tuples"] = list_of_tuples
        entry_dict["current_speed"] = 0
        entry_dict["top_speed"] = 0
        entry_dict["heading"] = 0
        entry_dict["orientation"] = 0
        entry_dict["color"]         = fill_color
        self.design_dict_list.append(entry_dict)

    def create_text(self, text_entry: str, 
                          input_color: str,
                          input_starting_x_qty: float,
                          input_starting_y_qty: float):
        """Give a text entry and starting point, draw letters on the map and store them as objects"""
        entry_dict: dict = {}
        entry_dict["Text"] = "Text"
        entry_dict["text_entry"] = text_entry
        entry_dict["local_starting_x_qty"] = input_starting_x_qty
        entry_dict["local_starting_y_qty"] = input_starting_y_qty
        entry_dict["current_speed"] = 0
        entry_dict["top_speed"]     = 0
        entry_dict["heading"]       = 0
        entry_dict["orientation"]   = 0
        entry_dict["color"]         = input_color
        self.design_dict_list.append(entry_dict)
        if input_color == "Color":
            input_color = "Black"

        for char in text_entry:
            match char:
                case 'A':
                    self.draw_a(input_starting_x_qty = input_starting_x_qty,
                                input_starting_y_qty = input_starting_y_qty,
                                input_color = input_color)
                case 'B':
                    self.draw_b(input_starting_x_qty = input_starting_x_qty,
                                input_starting_y_qty = input_starting_y_qty,
                                input_color = input_color)
                case 'C':
                    self.draw_c(input_starting_x_qty = input_starting_x_qty,
                                input_starting_y_qty = input_starting_y_qty,
                                input_color = input_color)
                case 'D':
                    self.draw_d(input_starting_x_qty = input_starting_x_qty,
                                input_starting_y_qty = input_starting_y_qty,
                                input_color = input_color)
                case 'E':
                    self.draw_e(input_starting_x_qty = input_starting_x_qty,
                                input_starting_y_qty = input_starting_y_qty,
                                input_color = input_color)
                case 'F':
                    self.draw_f(input_starting_x_qty = input_starting_x_qty,
                                input_starting_y_qty = input_starting_y_qty,
                                input_color = input_color)
                case 'G':
                    self.draw_g(input_starting_x_qty = input_starting_x_qty,
                                input_starting_y_qty = input_starting_y_qty,
                                input_color = input_color)
                case 'H':
                    self.draw_h(input_starting_x_qty = input_starting_x_qty,
                                input_starting_y_qty = input_starting_y_qty,
                                input_color = input_color)
                case 'I':
                    self.draw_i(input_starting_x_qty = input_starting_x_qty,
                                input_starting_y_qty = input_starting_y_qty,
                                input_color = input_color)
                case 'J':
                    self.draw_j(input_starting_x_qty = input_starting_x_qty,
                                input_starting_y_qty = input_starting_y_qty,
                                input_color = input_color)
                case 'K':
                    self.draw_k(input_starting_x_qty = input_starting_x_qty,
                                input_starting_y_qty = input_starting_y_qty,
                                input_color = input_color)
                case 'L':
                    self.draw_l(input_starting_x_qty = input_starting_x_qty,
                                input_starting_y_qty = input_starting_y_qty,
                                input_color = input_color)
                case 'M':
                    self.draw_m(input_starting_x_qty = input_starting_x_qty,
                                input_starting_y_qty = input_starting_y_qty,
                                input_color = input_color)
                case 'N':
                    self.draw_n(input_starting_x_qty = input_starting_x_qty,
                                input_starting_y_qty = input_starting_y_qty,
                                input_color = input_color)
                case 'O':
                    self.draw_o(input_starting_x_qty = input_starting_x_qty,
                                input_starting_y_qty = input_starting_y_qty,
                                input_color = input_color)
                case 'P':
                    self.draw_p(input_starting_x_qty = input_starting_x_qty,
                                input_starting_y_qty = input_starting_y_qty,
                                input_color = input_color)
                case 'Q':
                    self.draw_q(input_starting_x_qty = input_starting_x_qty,
                                input_starting_y_qty = input_starting_y_qty,
                                input_color = input_color)
                case 'R':
                    self.draw_r(input_starting_x_qty = input_starting_x_qty,
                                input_starting_y_qty = input_starting_y_qty,
                                input_color = input_color)
                case 'S':
                    self.draw_s(input_starting_x_qty = input_starting_x_qty,
                                input_starting_y_qty = input_starting_y_qty,
                                input_color = input_color)
                case 'T':
                    self.draw_t(input_starting_x_qty = input_starting_x_qty,
                                input_starting_y_qty = input_starting_y_qty,
                                input_color = input_color)
                case 'U':
                    self.draw_u(input_starting_x_qty = input_starting_x_qty,
                                input_starting_y_qty = input_starting_y_qty,
                                input_color = input_color)
                case 'V':
                    self.draw_v(input_starting_x_qty = input_starting_x_qty,
                                input_starting_y_qty = input_starting_y_qty,
                                input_color = input_color)
                case 'W':
                    self.draw_w(input_starting_x_qty = input_starting_x_qty,
                                input_starting_y_qty = input_starting_y_qty,
                                input_color = input_color)
                case 'X':
                    self.draw_x(input_starting_x_qty = input_starting_x_qty,
                                input_starting_y_qty = input_starting_y_qty,
                                input_color = input_color)
                case 'Y':
                    self.draw_y(input_starting_x_qty = input_starting_x_qty,
                                input_starting_y_qty = input_starting_y_qty,
                                input_color = input_color)
                case 'Z':
                    self.draw_z(input_starting_x_qty = input_starting_x_qty,
                                input_starting_y_qty = input_starting_y_qty,
                                input_color = input_color)
            input_starting_x_qty += 1.0 #exact value TBD

    def draw_a(self, input_starting_x_qty: float, input_starting_y_qty: float, input_color: str):
        """Draw a letter at the coordinates provided"""
        #26 points drawing the capital A
        list_of_tuples: list = []
        #40 pixels to the inch
        #0.025 for the pixel

        list_of_tuples.append((input_starting_x_qty + 0.05,  input_starting_y_qty + 0.775))
        list_of_tuples.append((input_starting_x_qty + 0.05,  input_starting_y_qty + 0.925))
        list_of_tuples.append((input_starting_x_qty + 0.075, input_starting_y_qty + 0.95))
        list_of_tuples.append((input_starting_x_qty + 0.225, input_starting_y_qty + 0.95))
        list_of_tuples.append((input_starting_x_qty + 0.25,  input_starting_y_qty + 0.925))
        list_of_tuples.append((input_starting_x_qty + 0.25,  input_starting_y_qty + 0.775))
        list_of_tuples.append((input_starting_x_qty + 0.225, input_starting_y_qty + 0.75))
        list_of_tuples.append((input_starting_x_qty + 0.5,   input_starting_y_qty + 0.25))
        list_of_tuples.append((input_starting_x_qty + 0.775, input_starting_y_qty + 0.75))
        list_of_tuples.append((input_starting_x_qty + 0.7,   input_starting_y_qty + 0.625))
        list_of_tuples.append((input_starting_x_qty + 0.3,   input_starting_y_qty + 0.625))
        list_of_tuples.append((input_starting_x_qty + 0.375, input_starting_y_qty + 0.5))
        list_of_tuples.append((input_starting_x_qty + 0.65,  input_starting_y_qty + 0.5))
        list_of_tuples.append((input_starting_x_qty + 0.775, input_starting_y_qty + 0.75))
        list_of_tuples.append((input_starting_x_qty + 0.75,  input_starting_y_qty + 0.775))
        list_of_tuples.append((input_starting_x_qty + 0.75,  input_starting_y_qty + 0.925))
        list_of_tuples.append((input_starting_x_qty + 0.775, input_starting_y_qty + 0.95))
        list_of_tuples.append((input_starting_x_qty + 0.925, input_starting_y_qty + 0.95))
        list_of_tuples.append((input_starting_x_qty + 0.95,  input_starting_y_qty + 0.925))
        list_of_tuples.append((input_starting_x_qty + 0.95,  input_starting_y_qty + 0.775))
        list_of_tuples.append((input_starting_x_qty + 0.925, input_starting_y_qty + 0.75))
        list_of_tuples.append((input_starting_x_qty + 0.625, input_starting_y_qty + 0.075))
        list_of_tuples.append((input_starting_x_qty + 0.6,   input_starting_y_qty + 0.05))
        list_of_tuples.append((input_starting_x_qty + 0.4,   input_starting_y_qty + 0.05))
        list_of_tuples.append((input_starting_x_qty + 0.375, input_starting_y_qty + 0.075))
        list_of_tuples.append((input_starting_x_qty + 0.075, input_starting_y_qty + 0.75))
        
        self.create_polygon(list_of_tuples=list_of_tuples, input_color=input_color)

    def draw_b(self, input_starting_x_qty: float, input_starting_y_qty: float, input_color: str):
        """Draw a letter at the coordinates provided"""
        #23 points drawing the capital B
        list_of_tuples: list = []
        #40 pixels to the inch
        #0.025 for the pixel

        list_of_tuples.append((input_starting_x_qty + 0.05,  input_starting_y_qty + 0.075))
        list_of_tuples.append((input_starting_x_qty + 0.05,  input_starting_y_qty + 0.925))
        list_of_tuples.append((input_starting_x_qty + 0.075, input_starting_y_qty + 0.95))
        list_of_tuples.append((input_starting_x_qty + 0.85,  input_starting_y_qty + 0.95))
        list_of_tuples.append((input_starting_x_qty + 0.95,  input_starting_y_qty + 0.85))
        list_of_tuples.append((input_starting_x_qty + 0.95,  input_starting_y_qty + 0.625))
        list_of_tuples.append((input_starting_x_qty + 0.825, input_starting_y_qty + 0.5))
        list_of_tuples.append((input_starting_x_qty + 0.95,  input_starting_y_qty + 0.375))
        list_of_tuples.append((input_starting_x_qty + 0.95,  input_starting_y_qty + 0.15))
        list_of_tuples.append((input_starting_x_qty + 0.85,  input_starting_y_qty + 0.05))
        list_of_tuples.append((input_starting_x_qty + 0.075, input_starting_y_qty + 0.05))
        list_of_tuples.append((input_starting_x_qty + 0.075, input_starting_y_qty + 0.075))
        list_of_tuples.append((input_starting_x_qty + 0.075, input_starting_y_qty + 0.1))
        list_of_tuples.append((input_starting_x_qty + 0.1,   input_starting_y_qty + 0.1))
        list_of_tuples.append((input_starting_x_qty + 0.1,   input_starting_y_qty + 0.125))
        list_of_tuples.append((input_starting_x_qty + 0.125, input_starting_y_qty + 0.125))
        list_of_tuples.append((input_starting_x_qty + 0.15,  input_starting_y_qty + 0.125))
        list_of_tuples.append((input_starting_x_qty + 0.15,  input_starting_y_qty + 0.15))
        list_of_tuples.append((input_starting_x_qty + 0.175, input_starting_y_qty + 0.15))
        list_of_tuples.append((input_starting_x_qty + 0.175, input_starting_y_qty + 0.175))
        list_of_tuples.append((input_starting_x_qty + 0.2,   input_starting_y_qty + 0.175))
        list_of_tuples.append((input_starting_x_qty + 0.2,   input_starting_y_qty + 0.2))
        list_of_tuples.append((input_starting_x_qty + 0.225, input_starting_y_qty + 0.2))
        list_of_tuples.append((input_starting_x_qty + 0.225, input_starting_y_qty + 0.225))
        list_of_tuples.append((input_starting_x_qty + 0.25,  input_starting_y_qty + 0.225))
        list_of_tuples.append((input_starting_x_qty + 0.25,  input_starting_y_qty + 0.25))
        list_of_tuples.append((input_starting_x_qty + 0.675, input_starting_y_qty + 0.25))
        list_of_tuples.append((input_starting_x_qty + 0.75,  input_starting_y_qty + 0.325))
        list_of_tuples.append((input_starting_x_qty + 0.675, input_starting_y_qty + 0.4))
        list_of_tuples.append((input_starting_x_qty + 0.25,  input_starting_y_qty + 0.4))
        list_of_tuples.append((input_starting_x_qty + 0.25,  input_starting_y_qty + 0.275))
        list_of_tuples.append((input_starting_x_qty + 0.25,  input_starting_y_qty + 0.75))
        list_of_tuples.append((input_starting_x_qty + 0.675, input_starting_y_qty + 0.75))
        list_of_tuples.append((input_starting_x_qty + 0.75,  input_starting_y_qty + 0.675))
        list_of_tuples.append((input_starting_x_qty + 0.675, input_starting_y_qty + 0.6))
        list_of_tuples.append((input_starting_x_qty + 0.25,  input_starting_y_qty + 0.6))
        list_of_tuples.append((input_starting_x_qty + 0.25,  input_starting_y_qty + 0.225))
        list_of_tuples.append((input_starting_x_qty + 0.225, input_starting_y_qty + 0.225))
        list_of_tuples.append((input_starting_x_qty + 0.225, input_starting_y_qty + 0.2))
        list_of_tuples.append((input_starting_x_qty + 0.2,   input_starting_y_qty + 0.2))
        list_of_tuples.append((input_starting_x_qty + 0.2,   input_starting_y_qty + 0.175))
        list_of_tuples.append((input_starting_x_qty + 0.175, input_starting_y_qty + 0.175))
        list_of_tuples.append((input_starting_x_qty + 0.175, input_starting_y_qty + 0.15))
        list_of_tuples.append((input_starting_x_qty + 0.15,  input_starting_y_qty + 0.15))
        list_of_tuples.append((input_starting_x_qty + 0.15,  input_starting_y_qty + 0.125))
        list_of_tuples.append((input_starting_x_qty + 0.125, input_starting_y_qty + 0.125))
        list_of_tuples.append((input_starting_x_qty + 0.125, input_starting_y_qty + 0.1))
        list_of_tuples.append((input_starting_x_qty + 0.1,   input_starting_y_qty + 0.1))
        list_of_tuples.append((input_starting_x_qty + 0.1,   input_starting_y_qty + 0.075))
        list_of_tuples.append((input_starting_x_qty + 0.075, input_starting_y_qty + 0.075))
        list_of_tuples.append((input_starting_x_qty + 0.05,  input_starting_y_qty + 0.075))
        
        self.create_polygon(list_of_tuples=list_of_tuples, input_color=input_color)

    def draw_c(self, input_starting_x_qty: float, input_starting_y_qty: float, input_color: str):
        """Draw a letter at the coordinates provided"""
        #16 points drawing the capital C
        list_of_tuples: list = []
        #40 pixels to the inch
        #0.025 for the pixel

        list_of_tuples.append((input_starting_x_qty + 0.05,  input_starting_y_qty + 0.075))
        list_of_tuples.append((input_starting_x_qty + 0.05,  input_starting_y_qty + 0.925))
        list_of_tuples.append((input_starting_x_qty + 0.075, input_starting_y_qty + 0.95))
        list_of_tuples.append((input_starting_x_qty + 0.925, input_starting_y_qty + 0.95))
        list_of_tuples.append((input_starting_x_qty + 0.95,  input_starting_y_qty + 0.925))
        list_of_tuples.append((input_starting_x_qty + 0.95,  input_starting_y_qty + 0.8))
        list_of_tuples.append((input_starting_x_qty + 0.925, input_starting_y_qty + 0.775))
        list_of_tuples.append((input_starting_x_qty + 0.25,  input_starting_y_qty + 0.775))
        list_of_tuples.append((input_starting_x_qty + 0.225, input_starting_y_qty + 0.75))
        list_of_tuples.append((input_starting_x_qty + 0.225, input_starting_y_qty + 0.25))
        list_of_tuples.append((input_starting_x_qty + 0.25,  input_starting_y_qty + 0.225))
        list_of_tuples.append((input_starting_x_qty + 0.925, input_starting_y_qty + 0.225))
        list_of_tuples.append((input_starting_x_qty + 0.95,  input_starting_y_qty + 0.2))
        list_of_tuples.append((input_starting_x_qty + 0.95,  input_starting_y_qty + 0.075))
        list_of_tuples.append((input_starting_x_qty + 0.925, input_starting_y_qty + 0.05))
        list_of_tuples.append((input_starting_x_qty + 0.075, input_starting_y_qty + 0.05))

        self.create_polygon(list_of_tuples=list_of_tuples, input_color=input_color)

    def draw_d(self, input_starting_x_qty: float, input_starting_y_qty: float, input_color: str):
        """Draw a letter at the coordinates provided"""
        list_of_tuples: list = []
        #40 pixels to the inch
        #0.025 for the pixel

        list_of_tuples.append((input_starting_x_qty + 0.05,  input_starting_y_qty + 0.075))
        list_of_tuples.append((input_starting_x_qty + 0.05,  input_starting_y_qty + 0.925))
        list_of_tuples.append((input_starting_x_qty + 0.075, input_starting_y_qty + 0.95))
        list_of_tuples.append((input_starting_x_qty + 0.85,  input_starting_y_qty + 0.95))
        list_of_tuples.append((input_starting_x_qty + 0.95,  input_starting_y_qty + 0.85))
        list_of_tuples.append((input_starting_x_qty + 0.95,  input_starting_y_qty + 0.15))
        list_of_tuples.append((input_starting_x_qty + 0.85,  input_starting_y_qty + 0.05))
        list_of_tuples.append((input_starting_x_qty + 0.075, input_starting_y_qty + 0.05))
        list_of_tuples.append((input_starting_x_qty + 0.075, input_starting_y_qty + 0.075))
        list_of_tuples.append((input_starting_x_qty + 0.1,   input_starting_y_qty + 0.075))
        list_of_tuples.append((input_starting_x_qty + 0.1,   input_starting_y_qty + 0.1))
        list_of_tuples.append((input_starting_x_qty + 0.125, input_starting_y_qty + 0.1))
        list_of_tuples.append((input_starting_x_qty + 0.125, input_starting_y_qty + 0.125))
        list_of_tuples.append((input_starting_x_qty + 0.15,  input_starting_y_qty + 0.125))
        list_of_tuples.append((input_starting_x_qty + 0.15,  input_starting_y_qty + 0.15))
        list_of_tuples.append((input_starting_x_qty + 0.175, input_starting_y_qty + 0.15))
        list_of_tuples.append((input_starting_x_qty + 0.175, input_starting_y_qty + 0.175))
        list_of_tuples.append((input_starting_x_qty + 0.2,   input_starting_y_qty + 0.175))
        list_of_tuples.append((input_starting_x_qty + 0.2,   input_starting_y_qty + 0.2))
        list_of_tuples.append((input_starting_x_qty + 0.225, input_starting_y_qty + 0.2))
        list_of_tuples.append((input_starting_x_qty + 0.225, input_starting_y_qty + 0.225))
        list_of_tuples.append((input_starting_x_qty + 0.25,  input_starting_y_qty + 0.225))
        list_of_tuples.append((input_starting_x_qty + 0.25,  input_starting_y_qty + 0.25))
        list_of_tuples.append((input_starting_x_qty + 0.25,  input_starting_y_qty + 0.725))
        list_of_tuples.append((input_starting_x_qty + 0.625, input_starting_y_qty + 0.75))
        list_of_tuples.append((input_starting_x_qty + 0.75,  input_starting_y_qty + 0.625))
        list_of_tuples.append((input_starting_x_qty + 0.75,  input_starting_y_qty + 0.375))
        list_of_tuples.append((input_starting_x_qty + 0.625, input_starting_y_qty + 0.25))
        list_of_tuples.append((input_starting_x_qty + 0.25,  input_starting_y_qty + 0.25))
        list_of_tuples.append((input_starting_x_qty + 0.25,  input_starting_y_qty + 0.225))
        list_of_tuples.append((input_starting_x_qty + 0.225, input_starting_y_qty + 0.225))
        list_of_tuples.append((input_starting_x_qty + 0.225, input_starting_y_qty + 0.2))
        list_of_tuples.append((input_starting_x_qty + 0.2,   input_starting_y_qty + 0.2))
        list_of_tuples.append((input_starting_x_qty + 0.2,   input_starting_y_qty + 0.175))
        list_of_tuples.append((input_starting_x_qty + 0.175, input_starting_y_qty + 0.175))
        list_of_tuples.append((input_starting_x_qty + 0.175, input_starting_y_qty + 0.15))
        list_of_tuples.append((input_starting_x_qty + 0.15,  input_starting_y_qty + 0.15))
        list_of_tuples.append((input_starting_x_qty + 0.15,  input_starting_y_qty + 0.125))
        list_of_tuples.append((input_starting_x_qty + 0.125, input_starting_y_qty + 0.125))
        list_of_tuples.append((input_starting_x_qty + 0.125, input_starting_y_qty + 0.1))
        list_of_tuples.append((input_starting_x_qty + 0.1,   input_starting_y_qty + 0.1))
        list_of_tuples.append((input_starting_x_qty + 0.1,   input_starting_y_qty + 0.075))
        list_of_tuples.append((input_starting_x_qty + 0.075, input_starting_y_qty + 0.075))
        list_of_tuples.append((input_starting_x_qty + 0.075, input_starting_y_qty + 0.05))

        self.create_polygon(list_of_tuples=list_of_tuples, input_color=input_color)

    def draw_e(self, input_starting_x_qty: float, input_starting_y_qty: float, input_color: str):
        """Draw a letter at the coordinates provided"""
        #24 points drawing the capital E
        list_of_tuples: list = []
        #40 pixels to the inch
        #0.025 for the pixel

        list_of_tuples.append((input_starting_x_qty + 0.05,  input_starting_y_qty + 0.075))
        list_of_tuples.append((input_starting_x_qty + 0.05,  input_starting_y_qty + 0.925))
        list_of_tuples.append((input_starting_x_qty + 0.075, input_starting_y_qty + 0.95))
        list_of_tuples.append((input_starting_x_qty + 0.925, input_starting_y_qty + 0.95))
        list_of_tuples.append((input_starting_x_qty + 0.95,  input_starting_y_qty + 0.925))
        list_of_tuples.append((input_starting_x_qty + 0.95,  input_starting_y_qty + 0.775))
        list_of_tuples.append((input_starting_x_qty + 0.925, input_starting_y_qty + 0.75))
        list_of_tuples.append((input_starting_x_qty + 0.275, input_starting_y_qty + 0.75))
        list_of_tuples.append((input_starting_x_qty + 0.25,  input_starting_y_qty + 0.725))
        list_of_tuples.append((input_starting_x_qty + 0.25,  input_starting_y_qty + 0.625))
        list_of_tuples.append((input_starting_x_qty + 0.275, input_starting_y_qty + 0.6))
        list_of_tuples.append((input_starting_x_qty + 0.725, input_starting_y_qty + 0.6))
        list_of_tuples.append((input_starting_x_qty + 0.75,  input_starting_y_qty + 0.575))
        list_of_tuples.append((input_starting_x_qty + 0.75,  input_starting_y_qty + 0.425))
        list_of_tuples.append((input_starting_x_qty + 0.725, input_starting_y_qty + 0.4))
        list_of_tuples.append((input_starting_x_qty + 0.275, input_starting_y_qty + 0.4))
        list_of_tuples.append((input_starting_x_qty + 0.25,  input_starting_y_qty + 0.375))
        list_of_tuples.append((input_starting_x_qty + 0.25,  input_starting_y_qty + 0.275))
        list_of_tuples.append((input_starting_x_qty + 0.275, input_starting_y_qty + 0.25))
        list_of_tuples.append((input_starting_x_qty + 0.925, input_starting_y_qty + 0.25))
        list_of_tuples.append((input_starting_x_qty + 0.95,  input_starting_y_qty + 0.225))
        list_of_tuples.append((input_starting_x_qty + 0.95,  input_starting_y_qty + 0.075))
        list_of_tuples.append((input_starting_x_qty + 0.925, input_starting_y_qty + 0.05))
        list_of_tuples.append((input_starting_x_qty + 0.075, input_starting_y_qty + 0.05))

        self.create_polygon(list_of_tuples=list_of_tuples, input_color=input_color)

    def draw_f(self, input_starting_x_qty: float, input_starting_y_qty: float, input_color: str):
        """Draw a letter at the coordinates provided"""
        #20 points drawing the capital F
        list_of_tuples: list = []
        #40 pixels to the inch
        #0.025 for the pixel

        list_of_tuples.append((input_starting_x_qty + 0.05,  input_starting_y_qty + 0.075))
        list_of_tuples.append((input_starting_x_qty + 0.05,  input_starting_y_qty + 0.925))
        list_of_tuples.append((input_starting_x_qty + 0.075, input_starting_y_qty + 0.95))
        list_of_tuples.append((input_starting_x_qty + 0.225, input_starting_y_qty + 0.95))
        list_of_tuples.append((input_starting_x_qty + 0.25,  input_starting_y_qty + 0.925))
        list_of_tuples.append((input_starting_x_qty + 0.25,  input_starting_y_qty + 0.625))
        list_of_tuples.append((input_starting_x_qty + 0.275, input_starting_y_qty + 0.6))
        list_of_tuples.append((input_starting_x_qty + 0.725, input_starting_y_qty + 0.6))
        list_of_tuples.append((input_starting_x_qty + 0.75,  input_starting_y_qty + 0.575))
        list_of_tuples.append((input_starting_x_qty + 0.75,  input_starting_y_qty + 0.425))
        list_of_tuples.append((input_starting_x_qty + 0.725, input_starting_y_qty + 0.4))
        list_of_tuples.append((input_starting_x_qty + 0.275, input_starting_y_qty + 0.4))
        list_of_tuples.append((input_starting_x_qty + 0.25,  input_starting_y_qty + 0.375))
        list_of_tuples.append((input_starting_x_qty + 0.25,  input_starting_y_qty + 0.275))
        list_of_tuples.append((input_starting_x_qty + 0.275, input_starting_y_qty + 0.25))
        list_of_tuples.append((input_starting_x_qty + 0.925, input_starting_y_qty + 0.25))
        list_of_tuples.append((input_starting_x_qty + 0.95,  input_starting_y_qty + 0.225))
        list_of_tuples.append((input_starting_x_qty + 0.95,  input_starting_y_qty + 0.075))
        list_of_tuples.append((input_starting_x_qty + 0.925, input_starting_y_qty + 0.05))
        list_of_tuples.append((input_starting_x_qty + 0.075, input_starting_y_qty + 0.05))
        
        self.create_polygon(list_of_tuples=list_of_tuples, input_color=input_color)

    def draw_g(self, input_starting_x_qty: float, input_starting_y_qty: float, input_color: str):
        """Draw a letter at the coordinates provided"""
        #24 points drawing the capital G
        list_of_tuples: list = []
        #40 pixels to the inch
        #0.025 for the pixel

        list_of_tuples.append((input_starting_x_qty + 0.05,  input_starting_y_qty + 0.075))
        list_of_tuples.append((input_starting_x_qty + 0.05,  input_starting_y_qty + 0.925))
        list_of_tuples.append((input_starting_x_qty + 0.075, input_starting_y_qty + 0.95))
        list_of_tuples.append((input_starting_x_qty + 0.925, input_starting_y_qty + 0.95))
        list_of_tuples.append((input_starting_x_qty + 0.95,  input_starting_y_qty + 0.925))
        list_of_tuples.append((input_starting_x_qty + 0.95,  input_starting_y_qty + 0.525))
        list_of_tuples.append((input_starting_x_qty + 0.925, input_starting_y_qty + 0.5))
        list_of_tuples.append((input_starting_x_qty + 0.525, input_starting_y_qty + 0.5))
        list_of_tuples.append((input_starting_x_qty + 0.5,   input_starting_y_qty + 0.525))
        list_of_tuples.append((input_starting_x_qty + 0.5,   input_starting_y_qty + 0.6))
        list_of_tuples.append((input_starting_x_qty + 0.525, input_starting_y_qty + 0.625))
        list_of_tuples.append((input_starting_x_qty + 0.725, input_starting_y_qty + 0.625))
        list_of_tuples.append((input_starting_x_qty + 0.75,  input_starting_y_qty + 0.65))
        list_of_tuples.append((input_starting_x_qty + 0.75,  input_starting_y_qty + 0.725))
        list_of_tuples.append((input_starting_x_qty + 0.725, input_starting_y_qty + 0.75))
        list_of_tuples.append((input_starting_x_qty + 0.275, input_starting_y_qty + 0.75))
        list_of_tuples.append((input_starting_x_qty + 0.25,  input_starting_y_qty + 0.725))
        list_of_tuples.append((input_starting_x_qty + 0.25,  input_starting_y_qty + 0.275))
        list_of_tuples.append((input_starting_x_qty + 0.275, input_starting_y_qty + 0.25))
        list_of_tuples.append((input_starting_x_qty + 0.925, input_starting_y_qty + 0.25))
        list_of_tuples.append((input_starting_x_qty + 0.95,  input_starting_y_qty + 0.225))
        list_of_tuples.append((input_starting_x_qty + 0.95,  input_starting_y_qty + 0.075))
        list_of_tuples.append((input_starting_x_qty + 0.925, input_starting_y_qty + 0.05))
        list_of_tuples.append((input_starting_x_qty + 0.075, input_starting_y_qty + 0.05))        

        self.create_polygon(list_of_tuples=list_of_tuples, input_color=input_color)

    def draw_h(self, input_starting_x_qty: float, input_starting_y_qty: float, input_color: str):
        """Draw a letter at the coordinates provided"""
        #24 points drawing the capital H
        list_of_tuples: list = []
        #40 pixels to the inch
        #0.025 for the pixel

        list_of_tuples.append((input_starting_x_qty + 0.05,  input_starting_y_qty + 0.075))
        list_of_tuples.append((input_starting_x_qty + 0.05,  input_starting_y_qty + 0.925))
        list_of_tuples.append((input_starting_x_qty + 0.075, input_starting_y_qty + 0.95))
        list_of_tuples.append((input_starting_x_qty + 0.2,   input_starting_y_qty + 0.95))
        list_of_tuples.append((input_starting_x_qty + 0.225, input_starting_y_qty + 0.925))
        list_of_tuples.append((input_starting_x_qty + 0.225, input_starting_y_qty + 0.625))
        list_of_tuples.append((input_starting_x_qty + 0.25,  input_starting_y_qty + 0.6))
        list_of_tuples.append((input_starting_x_qty + 0.75,  input_starting_y_qty + 0.6))
        list_of_tuples.append((input_starting_x_qty + 0.775, input_starting_y_qty + 0.625))
        list_of_tuples.append((input_starting_x_qty + 0.775, input_starting_y_qty + 0.925))
        list_of_tuples.append((input_starting_x_qty + 0.8,   input_starting_y_qty + 0.95))
        list_of_tuples.append((input_starting_x_qty + 0.925, input_starting_y_qty + 0.95))
        list_of_tuples.append((input_starting_x_qty + 0.95,  input_starting_y_qty + 0.925))
        list_of_tuples.append((input_starting_x_qty + 0.95,  input_starting_y_qty + 0.075))
        list_of_tuples.append((input_starting_x_qty + 0.925, input_starting_y_qty + 0.05))
        list_of_tuples.append((input_starting_x_qty + 0.8,   input_starting_y_qty + 0.05))
        list_of_tuples.append((input_starting_x_qty + 0.775, input_starting_y_qty + 0.075))
        list_of_tuples.append((input_starting_x_qty + 0.775, input_starting_y_qty + 0.375))
        list_of_tuples.append((input_starting_x_qty + 0.75,  input_starting_y_qty + 0.4))
        list_of_tuples.append((input_starting_x_qty + 0.25,  input_starting_y_qty + 0.4))
        list_of_tuples.append((input_starting_x_qty + 0.225, input_starting_y_qty + 0.375))
        list_of_tuples.append((input_starting_x_qty + 0.225, input_starting_y_qty + 0.075))
        list_of_tuples.append((input_starting_x_qty + 0.2,   input_starting_y_qty + 0.05))
        list_of_tuples.append((input_starting_x_qty + 0.075, input_starting_y_qty + 0.05))

        self.create_polygon(list_of_tuples=list_of_tuples, input_color=input_color)

    def draw_i(self, input_starting_x_qty: float, input_starting_y_qty: float, input_color: str):
        """Draw a letter at the coordinates provided"""
        #24 points drawing the capital I
        list_of_tuples: list = []
        #40 pixels to the inch
        #0.025 for the pixel

        list_of_tuples.append((input_starting_x_qty + 0.05,  input_starting_y_qty + 0.075))
        list_of_tuples.append((input_starting_x_qty + 0.05,  input_starting_y_qty + 0.2))
        list_of_tuples.append((input_starting_x_qty + 0.075, input_starting_y_qty + 0.225))
        list_of_tuples.append((input_starting_x_qty + 0.375, input_starting_y_qty + 0.225))
        list_of_tuples.append((input_starting_x_qty + 0.4,   input_starting_y_qty + 0.25))
        list_of_tuples.append((input_starting_x_qty + 0.4,   input_starting_y_qty + 0.75))
        list_of_tuples.append((input_starting_x_qty + 0.375, input_starting_y_qty + 0.775))
        list_of_tuples.append((input_starting_x_qty + 0.075, input_starting_y_qty + 0.775))
        list_of_tuples.append((input_starting_x_qty + 0.05,  input_starting_y_qty + 0.8))
        list_of_tuples.append((input_starting_x_qty + 0.05,  input_starting_y_qty + 0.925))
        list_of_tuples.append((input_starting_x_qty + 0.075, input_starting_y_qty + 0.95))
        list_of_tuples.append((input_starting_x_qty + 0.925, input_starting_y_qty + 0.95))
        list_of_tuples.append((input_starting_x_qty + 0.95,  input_starting_y_qty + 0.925))
        list_of_tuples.append((input_starting_x_qty + 0.95,  input_starting_y_qty + 0.8))
        list_of_tuples.append((input_starting_x_qty + 0.925, input_starting_y_qty + 0.77))
        list_of_tuples.append((input_starting_x_qty + 0.625, input_starting_y_qty + 0.77))
        list_of_tuples.append((input_starting_x_qty + 0.6,   input_starting_y_qty + 0.75))
        list_of_tuples.append((input_starting_x_qty + 0.6,   input_starting_y_qty + 0.25))
        list_of_tuples.append((input_starting_x_qty + 0.625, input_starting_y_qty + 0.225))
        list_of_tuples.append((input_starting_x_qty + 0.925, input_starting_y_qty + 0.225))
        list_of_tuples.append((input_starting_x_qty + 0.95,  input_starting_y_qty + 0.2))
        list_of_tuples.append((input_starting_x_qty + 0.95,  input_starting_y_qty +0.075 ))
        list_of_tuples.append((input_starting_x_qty + 0.925, input_starting_y_qty + 0.05))
        list_of_tuples.append((input_starting_x_qty + 0.075, input_starting_y_qty + 0.05))

        self.create_polygon(list_of_tuples=list_of_tuples, input_color=input_color)

    def draw_j(self, input_starting_x_qty: float, input_starting_y_qty: float, input_color: str):
        """Draw a letter at the coordinates provided"""
        #23 points drawing the capital J
        list_of_tuples: list = []
        #40 pixels to the inch
        #0.025 for the pixel

        list_of_tuples.append((input_starting_x_qty + 0.05,  input_starting_y_qty + 0.075))
        list_of_tuples.append((input_starting_x_qty + 0.05,  input_starting_y_qty + 0.225))
        list_of_tuples.append((input_starting_x_qty + 0.075, input_starting_y_qty + 0.25))
        list_of_tuples.append((input_starting_x_qty + 0.475, input_starting_y_qty + 0.25))
        list_of_tuples.append((input_starting_x_qty + 0.5,   input_starting_y_qty + 0.275))
        list_of_tuples.append((input_starting_x_qty + 0.5,   input_starting_y_qty + 0.725))
        list_of_tuples.append((input_starting_x_qty + 0.475, input_starting_y_qty + 0.75))
        list_of_tuples.append((input_starting_x_qty + 0.275, input_starting_y_qty + 0.75))
        list_of_tuples.append((input_starting_x_qty + 0.25,  input_starting_y_qty + 0.725))
        list_of_tuples.append((input_starting_x_qty + 0.25,  input_starting_y_qty + 0.525))
        list_of_tuples.append((input_starting_x_qty + 0.075, input_starting_y_qty + 0.5))
        list_of_tuples.append((input_starting_x_qty + 0.05,  input_starting_y_qty + 0.525))
        list_of_tuples.append((input_starting_x_qty + 0.05,  input_starting_y_qty + 0.925))
        list_of_tuples.append((input_starting_x_qty + 0.075, input_starting_y_qty + 0.95))
        list_of_tuples.append((input_starting_x_qty + 0.725, input_starting_y_qty + 0.95))
        list_of_tuples.append((input_starting_x_qty + 0.75,  input_starting_y_qty + 0.925))
        list_of_tuples.append((input_starting_x_qty + 0.75,  input_starting_y_qty + 0.275))
        list_of_tuples.append((input_starting_x_qty + 0.775, input_starting_y_qty + 0.25))
        list_of_tuples.append((input_starting_x_qty + 0.925, input_starting_y_qty + 0.25))
        list_of_tuples.append((input_starting_x_qty + 0.95,  input_starting_y_qty + 0.225))
        list_of_tuples.append((input_starting_x_qty + 0.95,  input_starting_y_qty + 0.075))
        list_of_tuples.append((input_starting_x_qty + 0.925, input_starting_y_qty + 0.05))
        list_of_tuples.append((input_starting_x_qty + 0.075, input_starting_y_qty + 0.05))

        self.create_polygon(list_of_tuples=list_of_tuples, input_color=input_color)

    def draw_k(self, input_starting_x_qty: float, input_starting_y_qty: float, input_color: str):
        """Draw a letter at the coordinates provided"""
        #20 points drawing the capital K
        list_of_tuples: list = []
        #40 pixels to the inch
        #0.025 for the pixel

        list_of_tuples.append((input_starting_x_qty + 0.05,  input_starting_y_qty + 0.075))
        list_of_tuples.append((input_starting_x_qty + 0.05,  input_starting_y_qty + 0.925))
        list_of_tuples.append((input_starting_x_qty + 0.075, input_starting_y_qty + 0.95))
        list_of_tuples.append((input_starting_x_qty + 0.225, input_starting_y_qty + 0.95))
        list_of_tuples.append((input_starting_x_qty + 0.25,  input_starting_y_qty + 0.925))
        list_of_tuples.append((input_starting_x_qty + 0.25,  input_starting_y_qty + 0.65))
        list_of_tuples.append((input_starting_x_qty + 0.275, input_starting_y_qty + 0.625))
        list_of_tuples.append((input_starting_x_qty + 0.45,  input_starting_y_qty + 0.625))
        list_of_tuples.append((input_starting_x_qty + 0.775, input_starting_y_qty + 0.95))
        list_of_tuples.append((input_starting_x_qty + 0.925, input_starting_y_qty + 0.95))
        list_of_tuples.append((input_starting_x_qty + 0.95,  input_starting_y_qty + 0.925))
        list_of_tuples.append((input_starting_x_qty + 0.95,  input_starting_y_qty + 0.775))
        list_of_tuples.append((input_starting_x_qty + 0.675, input_starting_y_qty + 0.5))
        list_of_tuples.append((input_starting_x_qty + 0.95,  input_starting_y_qty + 0.225))
        list_of_tuples.append((input_starting_x_qty + 0.95,  input_starting_y_qty + 0.075))
        list_of_tuples.append((input_starting_x_qty + 0.925, input_starting_y_qty + 0.05))
        list_of_tuples.append((input_starting_x_qty + 0.775, input_starting_y_qty + 0.05))
        list_of_tuples.append((input_starting_x_qty + 0.45,  input_starting_y_qty + 0.375))
        list_of_tuples.append((input_starting_x_qty + 0.275, input_starting_y_qty + 0.375))
        list_of_tuples.append((input_starting_x_qty + 0.25,  input_starting_y_qty + 0.35))
        list_of_tuples.append((input_starting_x_qty + 0.25,  input_starting_y_qty + 0.075))
        list_of_tuples.append((input_starting_x_qty + 0.075, input_starting_y_qty + 0.05))

        self.create_polygon(list_of_tuples=list_of_tuples, input_color=input_color)

    def draw_l(self, input_starting_x_qty: float, input_starting_y_qty: float, input_color: str):
        """Draw a letter at the coordinates provided"""
        #12 points drawing the capital L
        list_of_tuples: list = []
        #40 pixels to the inch
        #0.025 for the pixel

        list_of_tuples.append((input_starting_x_qty + 0.05,  input_starting_y_qty + 0.075))
        list_of_tuples.append((input_starting_x_qty + 0.05,  input_starting_y_qty + 0.925))
        list_of_tuples.append((input_starting_x_qty + 0.075, input_starting_y_qty + 0.95))
        list_of_tuples.append((input_starting_x_qty + 0.925, input_starting_y_qty + 0.95))
        list_of_tuples.append((input_starting_x_qty + 0.95,  input_starting_y_qty + 0.925))
        list_of_tuples.append((input_starting_x_qty + 0.95,  input_starting_y_qty + 0.775))
        list_of_tuples.append((input_starting_x_qty + 0.925, input_starting_y_qty + 0.75))
        list_of_tuples.append((input_starting_x_qty + 0.275, input_starting_y_qty + 0.75))
        list_of_tuples.append((input_starting_x_qty + 0.25,  input_starting_y_qty + 0.725))
        list_of_tuples.append((input_starting_x_qty + 0.25,  input_starting_y_qty + 0.075))
        list_of_tuples.append((input_starting_x_qty + 0.225, input_starting_y_qty + 0.05))
        list_of_tuples.append((input_starting_x_qty + 0.075, input_starting_y_qty + 0.05))

        self.create_polygon(list_of_tuples=list_of_tuples, input_color=input_color)

    def draw_m(self, input_starting_x_qty: float, input_starting_y_qty: float, input_color: str):
        """Draw a letter at the coordinates provided"""
        #20 points drawing the capital M
        list_of_tuples: list = []
        #40 pixels to the inch
        #0.025 for the pixel

        list_of_tuples.append((input_starting_x_qty + 0.05,  input_starting_y_qty + 0.075))
        list_of_tuples.append((input_starting_x_qty + 0.05,  input_starting_y_qty + 0.925))
        list_of_tuples.append((input_starting_x_qty + 0.075, input_starting_y_qty + 0.95))
        list_of_tuples.append((input_starting_x_qty + 0.225, input_starting_y_qty + 0.95))
        list_of_tuples.append((input_starting_x_qty + 0.25,  input_starting_y_qty + 0.925))
        list_of_tuples.append((input_starting_x_qty + 0.25,  input_starting_y_qty + 0.375))
        list_of_tuples.append((input_starting_x_qty + 0.275, input_starting_y_qty + 0.35))
        list_of_tuples.append((input_starting_x_qty + 0.5,   input_starting_y_qty + 0.575))
        list_of_tuples.append((input_starting_x_qty + 0.725, input_starting_y_qty + 0.35))
        list_of_tuples.append((input_starting_x_qty + 0.75,  input_starting_y_qty + 0.375))
        list_of_tuples.append((input_starting_x_qty + 0.75,  input_starting_y_qty + 0.925))
        list_of_tuples.append((input_starting_x_qty + 0.775, input_starting_y_qty + 0.95))
        list_of_tuples.append((input_starting_x_qty + 0.925, input_starting_y_qty + 0.95))
        list_of_tuples.append((input_starting_x_qty + 0.95,  input_starting_y_qty + 0.925))
        list_of_tuples.append((input_starting_x_qty + 0.95,  input_starting_y_qty + 0.075))
        list_of_tuples.append((input_starting_x_qty + 0.925, input_starting_y_qty + 0.05))
        list_of_tuples.append((input_starting_x_qty + 0.775, input_starting_y_qty + 0.05))
        list_of_tuples.append((input_starting_x_qty + 0.475, input_starting_y_qty + 0.325))
        list_of_tuples.append((input_starting_x_qty + 0.225, input_starting_y_qty + 0.05))
        list_of_tuples.append((input_starting_x_qty + 0.075, input_starting_y_qty + 0.05))

        self.create_polygon(list_of_tuples=list_of_tuples, input_color=input_color)

    def draw_n(self, input_starting_x_qty: float, input_starting_y_qty: float, input_color: str):
        """Draw a letter at the coordinates provided"""
        #18 points drawing the capital N
        list_of_tuples: list = []
        #40 pixels to the inch
        #0.025 for the pixel

        list_of_tuples.append((input_starting_x_qty + 0.05,  input_starting_y_qty + 0.075))
        list_of_tuples.append((input_starting_x_qty + 0.05,  input_starting_y_qty + 0.925))
        list_of_tuples.append((input_starting_x_qty + 0.075, input_starting_y_qty + 0.95))
        list_of_tuples.append((input_starting_x_qty + 0.225, input_starting_y_qty + 0.95))
        list_of_tuples.append((input_starting_x_qty + 0.25,  input_starting_y_qty + 0.925))
        list_of_tuples.append((input_starting_x_qty + 0.25,  input_starting_y_qty + 0.475))
        list_of_tuples.append((input_starting_x_qty + 0.275, input_starting_y_qty + 0.45))
        list_of_tuples.append((input_starting_x_qty + 0.775, input_starting_y_qty + 0.95))
        list_of_tuples.append((input_starting_x_qty + 0.925, input_starting_y_qty + 0.95))
        list_of_tuples.append((input_starting_x_qty + 0.95,  input_starting_y_qty + 0.925))
        list_of_tuples.append((input_starting_x_qty + 0.95,  input_starting_y_qty + 0.075))
        list_of_tuples.append((input_starting_x_qty + 0.925, input_starting_y_qty + 0.05))
        list_of_tuples.append((input_starting_x_qty + 0.775, input_starting_y_qty + 0.05))
        list_of_tuples.append((input_starting_x_qty + 0.75,  input_starting_y_qty + 0.075))
        list_of_tuples.append((input_starting_x_qty + 0.75,  input_starting_y_qty + 0.525))
        list_of_tuples.append((input_starting_x_qty + 0.725, input_starting_y_qty + 0.55))
        list_of_tuples.append((input_starting_x_qty + 0.225, input_starting_y_qty + 0.05))
        list_of_tuples.append((input_starting_x_qty + 0.075, input_starting_y_qty + 0.05))

        self.create_polygon(list_of_tuples=list_of_tuples, input_color=input_color)

    def draw_o(self, input_starting_x_qty: float, input_starting_y_qty: float, input_color: str):
        """Draw a letter at the coordinates provided"""
        #16 points drawing the capital O
        list_of_tuples: list = []
        #40 pixels to the inch
        #0.025 for the pixel

        list_of_tuples.append((input_starting_x_qty + 0.05,  input_starting_y_qty + 0.075))
        list_of_tuples.append((input_starting_x_qty + 0.05,  input_starting_y_qty + 0.925))
        list_of_tuples.append((input_starting_x_qty + 0.075, input_starting_y_qty + 0.95))
        list_of_tuples.append((input_starting_x_qty + 0.925, input_starting_y_qty + 0.95))
        list_of_tuples.append((input_starting_x_qty + 0.95,  input_starting_y_qty + 0.925))
        list_of_tuples.append((input_starting_x_qty + 0.95,  input_starting_y_qty + 0.075))
        list_of_tuples.append((input_starting_x_qty + 0.925, input_starting_y_qty + 0.05))
        list_of_tuples.append((input_starting_x_qty + 0.25,  input_starting_y_qty + 0.05))
        list_of_tuples.append((input_starting_x_qty + 0.25,  input_starting_y_qty + 0.725))
        list_of_tuples.append((input_starting_x_qty + 0.275, input_starting_y_qty + 0.75))
        list_of_tuples.append((input_starting_x_qty + 0.725, input_starting_y_qty + 0.75))
        list_of_tuples.append((input_starting_x_qty + 0.75,  input_starting_y_qty + 0.725))
        list_of_tuples.append((input_starting_x_qty + 0.75,  input_starting_y_qty + 0.275))
        list_of_tuples.append((input_starting_x_qty + 0.725, input_starting_y_qty + 0.25))
        list_of_tuples.append((input_starting_x_qty + 0.25,  input_starting_y_qty + 0.25))
        list_of_tuples.append((input_starting_x_qty + 0.25,  input_starting_y_qty + 0.05))
        list_of_tuples.append((input_starting_x_qty + 0.075, input_starting_y_qty + 0.05))

        self.create_polygon(list_of_tuples=list_of_tuples, input_color=input_color)

    def draw_p(self, input_starting_x_qty: float, input_starting_y_qty: float, input_color: str):
        """Draw a letter at the coordinates provided"""
        #16 points drawing the capital Q
        list_of_tuples: list = []
        #40 pixels to the inch
        #0.025 for the pixel

        list_of_tuples.append((input_starting_x_qty + 0.05,  input_starting_y_qty + 0.075))
        list_of_tuples.append((input_starting_x_qty + 0.05,  input_starting_y_qty + 0.925))
        list_of_tuples.append((input_starting_x_qty + 0.075, input_starting_y_qty + 0.95))
        list_of_tuples.append((input_starting_x_qty + 0.225, input_starting_y_qty + 0.95))
        list_of_tuples.append((input_starting_x_qty + 0.25,  input_starting_y_qty + 0.275))
        list_of_tuples.append((input_starting_x_qty + 0.275, input_starting_y_qty + 0.25))
        list_of_tuples.append((input_starting_x_qty + 0.725, input_starting_y_qty + 0.25))
        list_of_tuples.append((input_starting_x_qty + 0.75,  input_starting_y_qty + 0.375))
        list_of_tuples.append((input_starting_x_qty + 0.625, input_starting_y_qty + 0.5))
        list_of_tuples.append((input_starting_x_qty + 0.25,  input_starting_y_qty + 0.5))
        list_of_tuples.append((input_starting_x_qty + 0.25,  input_starting_y_qty + 0.625))
        list_of_tuples.append((input_starting_x_qty + 0.75,  input_starting_y_qty + 0.625))
        list_of_tuples.append((input_starting_x_qty + 0.95,  input_starting_y_qty + 0.425))
        list_of_tuples.append((input_starting_x_qty + 0.95,  input_starting_y_qty + 0.075))
        list_of_tuples.append((input_starting_x_qty + 0.925, input_starting_y_qty + 0.05))
        list_of_tuples.append((input_starting_x_qty + 0.075, input_starting_y_qty + 0.05))

        self.create_polygon(list_of_tuples=list_of_tuples, input_color=input_color)

    def draw_q(self, input_starting_x_qty: float, input_starting_y_qty: float, input_color: str):
        """Draw a letter at the coordinates provided"""
        #20 points drawing the capital Q
        list_of_tuples: list = []
        #40 pixels to the inch
        #0.025 for the pixel
        
        list_of_tuples.append((input_starting_x_qty + 0.05,  input_starting_y_qty + 0.075))
        list_of_tuples.append((input_starting_x_qty + 0.05,  input_starting_y_qty + 0.925))
        list_of_tuples.append((input_starting_x_qty + 0.075, input_starting_y_qty + 0.95))
        list_of_tuples.append((input_starting_x_qty + 0.625, input_starting_y_qty + 0.95))
        list_of_tuples.append((input_starting_x_qty + 0.725, input_starting_y_qty + 0.85))
        list_of_tuples.append((input_starting_x_qty + 0.825, input_starting_y_qty + 0.95))
        list_of_tuples.append((input_starting_x_qty + 0.95,  input_starting_y_qty + 0.825))
        list_of_tuples.append((input_starting_x_qty + 0.85,  input_starting_y_qty + 0.725))
        list_of_tuples.append((input_starting_x_qty + 0.95,  input_starting_y_qty + 0.625))
        list_of_tuples.append((input_starting_x_qty + 0.95,  input_starting_y_qty + 0.075))
        list_of_tuples.append((input_starting_x_qty + 0.925, input_starting_y_qty + 0.05))
        list_of_tuples.append((input_starting_x_qty + 0.25,  input_starting_y_qty + 0.05))
        list_of_tuples.append((input_starting_x_qty + 0.25,  input_starting_y_qty + 0.725))
        list_of_tuples.append((input_starting_x_qty + 0.275, input_starting_y_qty + 0.75))
        list_of_tuples.append((input_starting_x_qty + 0.625, input_starting_y_qty + 0.75))
        list_of_tuples.append((input_starting_x_qty + 0.55,  input_starting_y_qty + 0.675))
        list_of_tuples.append((input_starting_x_qty + 0.675, input_starting_y_qty + 0.55))
        list_of_tuples.append((input_starting_x_qty + 0.75,  input_starting_y_qty + 0.625))
        list_of_tuples.append((input_starting_x_qty + 0.75,  input_starting_y_qty + 0.275))
        list_of_tuples.append((input_starting_x_qty + 0.725, input_starting_y_qty + 0.25))
        list_of_tuples.append((input_starting_x_qty + 0.25,  input_starting_y_qty + 0.25))
        list_of_tuples.append((input_starting_x_qty + 0.25,  input_starting_y_qty + 0.05))
        list_of_tuples.append((input_starting_x_qty + 0.075, input_starting_y_qty + 0.05))

        self.create_polygon(list_of_tuples=list_of_tuples, input_color=input_color)

    def draw_r(self, input_starting_x_qty: float, input_starting_y_qty: float, input_color: str):
        """Draw a letter at the coordinates provided"""
        #23 points drawing the capital R
        list_of_tuples: list = []

        list_of_tuples.append((input_starting_x_qty + 0.05,  input_starting_y_qty + 0.075))
        list_of_tuples.append((input_starting_x_qty + 0.05,  input_starting_y_qty + 0.925))
        list_of_tuples.append((input_starting_x_qty + 0.075, input_starting_y_qty + 0.95))
        list_of_tuples.append((input_starting_x_qty + 0.225, input_starting_y_qty + 0.925))
        list_of_tuples.append((input_starting_x_qty + 0.25,  input_starting_y_qty + 0.925))
        list_of_tuples.append((input_starting_x_qty + 0.25,  input_starting_y_qty + 0.275))
        list_of_tuples.append((input_starting_x_qty + 0.275, input_starting_y_qty + 0.25))
        list_of_tuples.append((input_starting_x_qty + 0.725, input_starting_y_qty + 0.25))
        list_of_tuples.append((input_starting_x_qty + 0.75,  input_starting_y_qty + 0.275))
        list_of_tuples.append((input_starting_x_qty + 0.75,  input_starting_y_qty + 0.375))
        list_of_tuples.append((input_starting_x_qty + 0.625, input_starting_y_qty + 0.5))
        list_of_tuples.append((input_starting_x_qty + 0.25,  input_starting_y_qty + 0.475))
        list_of_tuples.append((input_starting_x_qty + 0.25,  input_starting_y_qty + 0.625))
        list_of_tuples.append((input_starting_x_qty + 0.45,  input_starting_y_qty + 0.625))
        list_of_tuples.append((input_starting_x_qty + 0.775, input_starting_y_qty + 0.95))
        list_of_tuples.append((input_starting_x_qty + 0.925, input_starting_y_qty + 0.95))
        list_of_tuples.append((input_starting_x_qty + 0.95,  input_starting_y_qty + 0.925))
        list_of_tuples.append((input_starting_x_qty + 0.95,  input_starting_y_qty + 0.775))
        list_of_tuples.append((input_starting_x_qty + 0.775, input_starting_y_qty + 0.6))
        list_of_tuples.append((input_starting_x_qty + 0.95,  input_starting_y_qty + 0.425))
        list_of_tuples.append((input_starting_x_qty + 0.95,  input_starting_y_qty + 0.075))
        list_of_tuples.append((input_starting_x_qty + 0.925, input_starting_y_qty + 0.05))
        list_of_tuples.append((input_starting_x_qty + 0.075, input_starting_y_qty + 0.05))
                
        self.create_polygon(list_of_tuples=list_of_tuples, input_color=input_color)

    def draw_s(self, input_starting_x_qty: float, input_starting_y_qty: float, input_color: str):
        """Draw a letter at the coordinates provided"""
        #24 points drawing the capital S
        list_of_tuples: list = []
        #40 pixels to the inch
        #0.025 for the pixel

        list_of_tuples.append((input_starting_x_qty + 0.05,  input_starting_y_qty + 0.075))
        list_of_tuples.append((input_starting_x_qty + 0.05,  input_starting_y_qty + 0.425))
        list_of_tuples.append((input_starting_x_qty + 0.25,  input_starting_y_qty + 0.625))
        list_of_tuples.append((input_starting_x_qty + 0.725, input_starting_y_qty + 0.625))
        list_of_tuples.append((input_starting_x_qty + 0.75,  input_starting_y_qty + 0.65))
        list_of_tuples.append((input_starting_x_qty + 0.75,  input_starting_y_qty + 0.725))
        list_of_tuples.append((input_starting_x_qty + 0.725, input_starting_y_qty + 0.75))
        list_of_tuples.append((input_starting_x_qty + 0.075, input_starting_y_qty + 0.75))
        list_of_tuples.append((input_starting_x_qty + 0.05,  input_starting_y_qty + 0.775))
        list_of_tuples.append((input_starting_x_qty + 0.05,  input_starting_y_qty + 0.925))
        list_of_tuples.append((input_starting_x_qty + 0.075, input_starting_y_qty + 0.95))
        list_of_tuples.append((input_starting_x_qty + 0.925, input_starting_y_qty + 0.95))
        list_of_tuples.append((input_starting_x_qty + 0.95,  input_starting_y_qty + 0.925))
        list_of_tuples.append((input_starting_x_qty + 0.95,  input_starting_y_qty + 0.575))
        list_of_tuples.append((input_starting_x_qty + 0.75,  input_starting_y_qty + 0.4))
        list_of_tuples.append((input_starting_x_qty + 0.275, input_starting_y_qty + 0.375))
        list_of_tuples.append((input_starting_x_qty + 0.25,  input_starting_y_qty + 0.35))
        list_of_tuples.append((input_starting_x_qty + 0.25,  input_starting_y_qty + 0.275))
        list_of_tuples.append((input_starting_x_qty + 0.275, input_starting_y_qty + 0.25))
        list_of_tuples.append((input_starting_x_qty + 0.925, input_starting_y_qty + 0.25))
        list_of_tuples.append((input_starting_x_qty + 0.95,  input_starting_y_qty + 0.225))
        list_of_tuples.append((input_starting_x_qty + 0.95,  input_starting_y_qty + 0.075))
        list_of_tuples.append((input_starting_x_qty + 0.925, input_starting_y_qty + 0.05))
        list_of_tuples.append((input_starting_x_qty + 0.075, input_starting_y_qty + 0.05))

        self.create_polygon(list_of_tuples=list_of_tuples, input_color=input_color)

    def draw_t(self, input_starting_x_qty: float, input_starting_y_qty: float, input_color: str):
        """Draw a letter at the coordinates provided"""
        #16 points drawing the capital T
        list_of_tuples: list = []
        #40 pixels to the inch
        #0.025 for the pixel

        list_of_tuples.append((input_starting_x_qty + 0.05,  input_starting_y_qty + 0.075))
        list_of_tuples.append((input_starting_x_qty + 0.05,  input_starting_y_qty + 0.2))
        list_of_tuples.append((input_starting_x_qty + 0.075, input_starting_y_qty + 0.225))
        list_of_tuples.append((input_starting_x_qty + 0.375, input_starting_y_qty + 0.225))
        list_of_tuples.append((input_starting_x_qty + 0.4,   input_starting_y_qty + 0.25))
        list_of_tuples.append((input_starting_x_qty + 0.4,   input_starting_y_qty + 0.925))
        list_of_tuples.append((input_starting_x_qty + 0.425, input_starting_y_qty + 0.95))
        list_of_tuples.append((input_starting_x_qty + 0.575, input_starting_y_qty + 0.95))
        list_of_tuples.append((input_starting_x_qty + 0.6,   input_starting_y_qty + 0.925))
        list_of_tuples.append((input_starting_x_qty + 0.6,   input_starting_y_qty + 0.25))
        list_of_tuples.append((input_starting_x_qty + 0.625, input_starting_y_qty + 0.225))
        list_of_tuples.append((input_starting_x_qty + 0.925, input_starting_y_qty + 0.225))
        list_of_tuples.append((input_starting_x_qty + 0.95,  input_starting_y_qty + 0.2))
        list_of_tuples.append((input_starting_x_qty + 0.95,  input_starting_y_qty + 0.075))
        list_of_tuples.append((input_starting_x_qty + 0.925, input_starting_y_qty + 0.05))
        list_of_tuples.append((input_starting_x_qty + 0.075, input_starting_y_qty + 0.05))

        self.create_polygon(list_of_tuples=list_of_tuples, input_color=input_color)

    def draw_u(self, input_starting_x_qty: float, input_starting_y_qty: float, input_color: str):
        """Draw a letter at the coordinates provided"""
        #16 points drawing the capital U
        list_of_tuples: list = []
        #40 pixels to the inch
        #0.025 for the pixel

        list_of_tuples.append((input_starting_x_qty + 0.05,  input_starting_y_qty + 0.075))
        list_of_tuples.append((input_starting_x_qty + 0.05,  input_starting_y_qty + 0.925))
        list_of_tuples.append((input_starting_x_qty + 0.075, input_starting_y_qty + 0.95))
        list_of_tuples.append((input_starting_x_qty + 0.925, input_starting_y_qty + 0.95))
        list_of_tuples.append((input_starting_x_qty + 0.95,  input_starting_y_qty + 0.925))
        list_of_tuples.append((input_starting_x_qty + 0.95,  input_starting_y_qty + 0.075))
        list_of_tuples.append((input_starting_x_qty + 0.925, input_starting_y_qty + 0.05))
        list_of_tuples.append((input_starting_x_qty + 0.8,   input_starting_y_qty + 0.05))
        list_of_tuples.append((input_starting_x_qty + 0.775, input_starting_y_qty + 0.075))
        list_of_tuples.append((input_starting_x_qty + 0.775, input_starting_y_qty + 0.75))
        list_of_tuples.append((input_starting_x_qty + 0.75,  input_starting_y_qty + 0.75))
        list_of_tuples.append((input_starting_x_qty + 0.25,  input_starting_y_qty + 0.775))
        list_of_tuples.append((input_starting_x_qty + 0.225, input_starting_y_qty + 0.75))
        list_of_tuples.append((input_starting_x_qty + 0.225, input_starting_y_qty + 0.075))
        list_of_tuples.append((input_starting_x_qty + 0.2,   input_starting_y_qty + 0.05))
        list_of_tuples.append((input_starting_x_qty + 0.075, input_starting_y_qty + 0.05))

        self.create_polygon(list_of_tuples=list_of_tuples, input_color=input_color)

    def draw_v(self, input_starting_x_qty: float, input_starting_y_qty: float, input_color: str):
        """Draw a letter at the coordinates provided"""
        #17 points drawing the capital V
        list_of_tuples: list = []
        #40 pixels to the inch
        #0.025 for the pixel

        list_of_tuples.append((input_starting_x_qty + 0.05,  input_starting_y_qty + 0.075))
        list_of_tuples.append((input_starting_x_qty + 0.05,  input_starting_y_qty + 0.225))
        list_of_tuples.append((input_starting_x_qty + 0.075, input_starting_y_qty + 0.25))
        list_of_tuples.append((input_starting_x_qty + 0.375, input_starting_y_qty + 0.925))
        list_of_tuples.append((input_starting_x_qty + 0.4,   input_starting_y_qty + 0.95))
        list_of_tuples.append((input_starting_x_qty + 0.6,   input_starting_y_qty + 0.95))
        list_of_tuples.append((input_starting_x_qty + 0.625, input_starting_y_qty + 0.925))
        list_of_tuples.append((input_starting_x_qty + 0.925, input_starting_y_qty + 0.25))
        list_of_tuples.append((input_starting_x_qty + 0.95,  input_starting_y_qty + 0.225))
        list_of_tuples.append((input_starting_x_qty + 0.95,  input_starting_y_qty + 0.075))
        list_of_tuples.append((input_starting_x_qty + 0.925, input_starting_y_qty + 0.05))
        list_of_tuples.append((input_starting_x_qty + 0.775, input_starting_y_qty + 0.05))
        list_of_tuples.append((input_starting_x_qty + 0.75,  input_starting_y_qty + 0.075))
        list_of_tuples.append((input_starting_x_qty + 0.5,   input_starting_y_qty + 0.675))
        list_of_tuples.append((input_starting_x_qty + 0.25,  input_starting_y_qty + 0.075))
        list_of_tuples.append((input_starting_x_qty + 0.225, input_starting_y_qty + 0.05))
        list_of_tuples.append((input_starting_x_qty + 0.075, input_starting_y_qty + 0.05))

        self.create_polygon(list_of_tuples=list_of_tuples, input_color=input_color)

    def draw_w(self, input_starting_x_qty: float, input_starting_y_qty: float, input_color: str):
        """Draw a letter at the coordinates provided"""
        #27 points drawing the capital W
        list_of_tuples: list = []
        #40 pixels to the inch
        #0.025 for the pixel

        list_of_tuples.append((input_starting_x_qty + 0.05,  input_starting_y_qty + 0.075))
        list_of_tuples.append((input_starting_x_qty + 0.05,  input_starting_y_qty + 0.225))
        list_of_tuples.append((input_starting_x_qty + 0.075, input_starting_y_qty + 0.25))
        list_of_tuples.append((input_starting_x_qty + 0.25,  input_starting_y_qty + 0.925))
        list_of_tuples.append((input_starting_x_qty + 0.275, input_starting_y_qty + 0.95))
        list_of_tuples.append((input_starting_x_qty + 0.375, input_starting_y_qty + 0.95))
        list_of_tuples.append((input_starting_x_qty + 0.4,   input_starting_y_qty + 0.925))
        list_of_tuples.append((input_starting_x_qty + 0.5,   input_starting_y_qty + 0.5))
        list_of_tuples.append((input_starting_x_qty + 0.6,   input_starting_y_qty + 0.925))
        list_of_tuples.append((input_starting_x_qty + 0.625, input_starting_y_qty + 0.95))
        list_of_tuples.append((input_starting_x_qty + 0.725, input_starting_y_qty + 0.95))
        list_of_tuples.append((input_starting_x_qty + 0.75,  input_starting_y_qty + 0.925))
        list_of_tuples.append((input_starting_x_qty + 0.925, input_starting_y_qty + 0.25))
        list_of_tuples.append((input_starting_x_qty + 0.95,  input_starting_y_qty + 0.225))
        list_of_tuples.append((input_starting_x_qty + 0.95,  input_starting_y_qty + 0.075))
        list_of_tuples.append((input_starting_x_qty + 0.925, input_starting_y_qty + 0.05))
        list_of_tuples.append((input_starting_x_qty + 0.775, input_starting_y_qty + 0.05))
        list_of_tuples.append((input_starting_x_qty + 0.75,  input_starting_y_qty + 0.075))
        list_of_tuples.append((input_starting_x_qty + 0.65,  input_starting_y_qty + 0.5))
        list_of_tuples.append((input_starting_x_qty + 0.575, input_starting_y_qty + 0.075))
        list_of_tuples.append((input_starting_x_qty + 0.55,  input_starting_y_qty + 0.05))
        list_of_tuples.append((input_starting_x_qty + 0.45,  input_starting_y_qty + 0.05))
        list_of_tuples.append((input_starting_x_qty + 0.425, input_starting_y_qty + 0.075))
        list_of_tuples.append((input_starting_x_qty + 0.35,  input_starting_y_qty + 0.5))
        list_of_tuples.append((input_starting_x_qty + 0.25,  input_starting_y_qty + 0.075))
        list_of_tuples.append((input_starting_x_qty + 0.225, input_starting_y_qty + 0.05))
        list_of_tuples.append((input_starting_x_qty + 0.075, input_starting_y_qty + 0.05))        

        self.create_polygon(list_of_tuples=list_of_tuples, input_color=input_color)

    def draw_x(self, input_starting_x_qty: float, input_starting_y_qty: float, input_color: str):
        """Draw a letter at the coordinates provided"""
        #20 points drawing the capital X
        list_of_tuples: list = []
        #40 pixels to the inch
        #0.025 for the pixel

        list_of_tuples.append((input_starting_x_qty + 0.05,  input_starting_y_qty + 0.075))
        list_of_tuples.append((input_starting_x_qty + 0.05,  input_starting_y_qty + 0.225))
        list_of_tuples.append((input_starting_x_qty + 0.325, input_starting_y_qty + 0.5))
        list_of_tuples.append((input_starting_x_qty + 0.05,  input_starting_y_qty + 0.775))
        list_of_tuples.append((input_starting_x_qty + 0.05,  input_starting_y_qty + 0.925))
        list_of_tuples.append((input_starting_x_qty + 0.075, input_starting_y_qty + 0.95))
        list_of_tuples.append((input_starting_x_qty + 0.225, input_starting_y_qty + 0.95))
        list_of_tuples.append((input_starting_x_qty + 0.5,   input_starting_y_qty + 0.675))
        list_of_tuples.append((input_starting_x_qty + 0.775, input_starting_y_qty + 0.95))
        list_of_tuples.append((input_starting_x_qty + 0.925, input_starting_y_qty + 0.95))
        list_of_tuples.append((input_starting_x_qty + 0.95,  input_starting_y_qty + 0.925))
        list_of_tuples.append((input_starting_x_qty + 0.95,  input_starting_y_qty + 0.8))
        list_of_tuples.append((input_starting_x_qty + 0.65,  input_starting_y_qty + 0.5))
        list_of_tuples.append((input_starting_x_qty + 0.95,  input_starting_y_qty + 0.2))
        list_of_tuples.append((input_starting_x_qty + 0.95,  input_starting_y_qty + 0.075))
        list_of_tuples.append((input_starting_x_qty + 0.925, input_starting_y_qty + 0.05))
        list_of_tuples.append((input_starting_x_qty + 0.775, input_starting_y_qty + 0.05))
        list_of_tuples.append((input_starting_x_qty + 0.5,   input_starting_y_qty + 0.325))
        list_of_tuples.append((input_starting_x_qty + 0.225, input_starting_y_qty + 0.05))
        list_of_tuples.append((input_starting_x_qty + 0.075, input_starting_y_qty + 0.05))

        self.create_polygon(list_of_tuples=list_of_tuples, input_color=input_color)

    def draw_y(self, input_starting_x_qty: float, input_starting_y_qty: float, input_color: str):
        """Draw a letter at the coordinates provided"""
        #15 points drawing the capital X
        list_of_tuples: list = []
        #40 pixels to the inch
        #0.025 for the pixel

        list_of_tuples.append((input_starting_x_qty + 0.05,  input_starting_y_qty + 0.075))
        list_of_tuples.append((input_starting_x_qty + 0.05,  input_starting_y_qty + 0.225))
        list_of_tuples.append((input_starting_x_qty + 0.375, input_starting_y_qty + 0.55))
        list_of_tuples.append((input_starting_x_qty + 0.375, input_starting_y_qty + 0.925))
        list_of_tuples.append((input_starting_x_qty + 0.4,   input_starting_y_qty + 0.95))
        list_of_tuples.append((input_starting_x_qty + 0.6,   input_starting_y_qty + 0.95))
        list_of_tuples.append((input_starting_x_qty + 0.625, input_starting_y_qty + 0.925))
        list_of_tuples.append((input_starting_x_qty + 0.625, input_starting_y_qty + 0.55))
        list_of_tuples.append((input_starting_x_qty + 0.95,  input_starting_y_qty + 0.225))
        list_of_tuples.append((input_starting_x_qty + 0.95,  input_starting_y_qty + 0.075))
        list_of_tuples.append((input_starting_x_qty + 0.925, input_starting_y_qty + 0.05))
        list_of_tuples.append((input_starting_x_qty + 0.775, input_starting_y_qty + 0.05))
        list_of_tuples.append((input_starting_x_qty + 0.5,   input_starting_y_qty + 0.325))
        list_of_tuples.append((input_starting_x_qty + 0.225, input_starting_y_qty + 0.05))
        list_of_tuples.append((input_starting_x_qty + 0.075, input_starting_y_qty + 0.05))

        self.create_polygon(list_of_tuples=list_of_tuples, input_color=input_color)

    def draw_z(self, input_starting_x_qty: float, input_starting_y_qty: float, input_color: str):
        """Draw a letter at the coordinates provided"""
        #17 points drawing the capital Z
        list_of_tuples: list = []
        #40 pixels to the inch
        #0.025 for the pixel

        list_of_tuples.append((input_starting_x_qty + 0.05, input_starting_y_qty + 0.075))
        list_of_tuples.append((input_starting_x_qty + 0.05, input_starting_y_qty + 0.225))
        list_of_tuples.append((input_starting_x_qty + 0.075, input_starting_y_qty + 0.25))
        list_of_tuples.append((input_starting_x_qty + 0.525, input_starting_y_qty + 0.25))
        list_of_tuples.append((input_starting_x_qty + 0.55, input_starting_y_qty + 0.275))
        list_of_tuples.append((input_starting_x_qty + 0.05, input_starting_y_qty + 0.775))
        list_of_tuples.append((input_starting_x_qty + 0.05, input_starting_y_qty + 0.925))
        list_of_tuples.append((input_starting_x_qty + 0.075, input_starting_y_qty + 0.95))
        list_of_tuples.append((input_starting_x_qty + 0.925, input_starting_y_qty + 0.95))
        list_of_tuples.append((input_starting_x_qty + 0.95, input_starting_y_qty + 0.925))
        list_of_tuples.append((input_starting_x_qty + 0.95, input_starting_y_qty + 0.775))
        list_of_tuples.append((input_starting_x_qty + 0.925, input_starting_y_qty + 0.75))
        list_of_tuples.append((input_starting_x_qty + 0.425, input_starting_y_qty + 0.75))
        list_of_tuples.append((input_starting_x_qty + 0.95, input_starting_y_qty + 0.225))
        list_of_tuples.append((input_starting_x_qty + 0.95, input_starting_y_qty + 0.075))
        list_of_tuples.append((input_starting_x_qty + 0.925, input_starting_y_qty + 0.05))
        list_of_tuples.append((input_starting_x_qty + 0.075, input_starting_y_qty + 0.05))

        self.create_polygon(list_of_tuples=list_of_tuples, input_color=input_color)

    def create_floor_paint(self, input_color: str,
                             input_starting_x_qty: float,
                             input_starting_y_qty: float):
        """Given the input color, starting x and y qtys, apply the color to the white parts of the given square"""
        fill_color = input_color.lower()
        if fill_color == "Color":
            fill_color = "Black"
        #obtain the 1/4" image and duplicate it from local starting x/y to the local_x_qty and then the local_y_qty

        top: int = int(input_starting_y_qty * 40 + 1)
        left: int = int(input_starting_x_qty * 40 + 1)
        bottom: int = int(input_starting_y_qty * 40 + 9)
        right: int = int(input_starting_x_qty * 40 + 9)

        list_of_polygon_coords: list = []
        for row_loop in range(4):
            for col_loop in range(4):
                polygon_coords = [[left, top], [right, top], [right, bottom], [left, bottom]]
                list_of_polygon_coords.append(polygon_coords)
                left += 10
                right += 10
            top += 10
            bottom += 10
            left = int(input_starting_x_qty * 40 + 1)
            right = int(input_starting_x_qty * 40 + 9)
     
        draw = ImageDraw.Draw(self.current_image)
        for polygon_coords in list_of_polygon_coords:
            draw.polygon(polygon_coords, fill=fill_color, outline=fill_color)

        self.display_photo_img = ImageTk.PhotoImage(self.current_image)
        #self.main_grid.configure(image=self.display_photo_img)
        self.canvas_image_id = self.canvas.create_image(0, 0, anchor="nw", image=self.display_photo_img)
        self.canvas.config(scrollregion=self.canvas.bbox(tk.ALL))
        entry_dict: dict = {}
        entry_dict["FloorPaint"] = "FloorPaint"
        entry_dict["local_starting_x_qty"] = input_starting_x_qty
        entry_dict["local_starting_y_qty"] = input_starting_y_qty
        entry_dict["current_speed"]        = 0
        entry_dict["top_speed"]            = 0
        entry_dict["heading"]              = 0
        entry_dict["orientation"]          = 0
        entry_dict["color"]                = fill_color
        self.design_dict_list.append(entry_dict)

    def resize_image(self):
        """resize the map image"""
        #self.var_map_y_qty
        #self.var_map_x_qty
        # Get dimensions
        base_x, base_y = self.base_image.size
        local_y_qty = int(self.var_map_y_qty)
        local_x_qty = int(self.var_map_x_qty)
        #if local_y_qty > 17:
        #    local_y_qty = 17
        #if local_x_qty > 31:
        #    local_x_qty = 31

        # Concatenate horizontally
        # Create a new image with combined width and max height
        final_y: int = (base_y - 1) * local_y_qty + 1
        final_x: int = (base_x - 1) * local_x_qty + 1
        concatenated_v = Image.new('RGB', (base_x, final_y))
        for loop_index in range(local_y_qty):
            temp_y: int = (base_y -1) * (loop_index)
            concatenated_v.paste(im=self.base_image, box=(0, temp_y) )

        new_x, new_y = concatenated_v.size
        # Concatenate vertically
        # Create a new image with max width and combined height
        final_image = Image.new('RGB', (final_x, final_y))
        for loop_index in range(local_x_qty):
            temp_x: int = (base_x - 1) * (loop_index)
            final_image.paste(im=concatenated_v, box=(temp_x, 0))

        self.current_image = final_image
        self.display_photo_img = ImageTk.PhotoImage(self.current_image)
        # Add the image to the canvas
        self.canvas_image_id = self.canvas.create_image(0, 0, anchor="nw", image=self.display_photo_img)
        self.canvas.config(scrollregion=self.canvas.bbox(tk.ALL))
        #self.main_grid.configure(image=self.display_photo_img)
        self.design_dict_list.clear() #resizing the map means empty all the objects
        entry_dict: dict = {}
        entry_dict['map_size'] = f"{local_x_qty}X{local_y_qty}"
        self.design_dict_list.append(entry_dict)

    def zoom_in(self, event=None):
        self.zoom_level += 0.2
        new_width = int(self.current_image.width * self.zoom_level)
        new_height = int(self.current_image.height * self.zoom_level)
        resized_image = self.current_image.resize((new_width, new_height), Image.LANCZOS)
        self.display_photo_img = ImageTk.PhotoImage(resized_image) # Update reference
        self.main_grid.config(image=self.display_photo_img)

    def zoom_out(self, event=None):
        self.zoom_level -= 0.2
        if self.zoom_level == 0.0:
            self.zoom_level = 0.2
        new_width = int(self.current_image.width * self.zoom_level)
        new_height = int(self.current_image.height * self.zoom_level)
        resized_image = self.current_image.resize((new_width, new_height), Image.LANCZOS)
        self.display_photo_img = ImageTk.PhotoImage(resized_image)
        self.main_grid.config(image=self.display_photo_img)

    def load_main_grid(self):
        self.display_photo_img = ImageTk.PhotoImage(self.base_image)
        self.current_image = self.base_image
        # Configure scrollregion to match image size
        self.canvas.config(scrollregion=self.canvas.bbox(self.display_photo_img))
        #self.main_grid.configure(image=self.display_photo_img)
        self.canvas_image_id = self.canvas.create_image(0, 0, anchor="nw", image=self.display_photo_img)
        self.canvas.config(scrollregion=self.canvas.bbox(tk.ALL))

if __name__ == '__main__':
    print("Launching CWO Map Designer")
    local_map_app: cwo_online_map_window = cwo_online_map_window()
    local_map_app.launch_it()
    print('Leaving CWO Map Designer')
