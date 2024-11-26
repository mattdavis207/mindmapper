import tkinter as tk
import math
from tkinter import *



#Application object
m = tk.Tk(screenName = "Mindmapper", className = 'Mindmapper')

m.title("Mindmapper")
m.geometry('600x600')

#Configure main grid
for i in range(3):
    m.grid_rowconfigure(i, weight=1)  # Rows expand proportionally
    m.grid_columnconfigure(i, weight=1)




#Make a class for the panning and zooming canvas
class PanZoomCanvasApp:
    def __init__(self, m):
        self.m = m
        self.m.title("Panning and Zooming Canvas")

        
        # Create the Canvas
        self.canvas = tk.Canvas(m, bg="white")
        self.canvas.grid(row =1, column = 1, sticky = "nsew")
        for i in range(3):
            self.canvas.grid_rowconfigure(i, weight=0)  # Rows expand proportionally
            self.canvas.grid_columnconfigure(i, weight=1)

        # Set the percentage of the window size for the canvas
        self.canvas_width_percentage = 0.6  # 70% of the window width
        self.canvas_height_percentage = 0.7  # 70% of the window height


         # Create some Frames for Buttons
        button_frame_1 = tk.Frame(self.canvas, highlightbackground = 'white')
        button_frame_1.grid(row = 0, column = 2, sticky = 'e', pady = (5,0), padx = (0, 5))
        button_frame_1.grid_rowconfigure(0, weight = 1)
        button_frame_2 = tk.Frame(self.canvas, highlightbackground = 'white')
        button_frame_2.grid(row = 0, column = 0, sticky ='w', pady = (5, 0), padx = (5, 0))

        
        # Zoom In Button
        zoom_in_button = tk.Button(button_frame_1, text="+", relief = 'sunken', highlightbackground = 'white', highlightthickness = 0, command=self.zoom_in)
        zoom_in_button.grid(row = 0, column = 1)
        
        # Zoom Out Button
        zoom_out_button = tk.Button(button_frame_1, text="-", relief = 'sunken', command=self.zoom_out, highlightbackground = 'white', highlightthickness = 0)
        zoom_out_button.grid(row = 0, column = 0)

        #Back to Center Button
        btc_button = tk.Button(button_frame_2, text="Back to Center", relief = 'ridge', highlightbackground = 'white', highlightthickness = 0, command = self.back_to_center)
        btc_button.grid(row = 0, column = 0, sticky = 'nsew')

        
        # Variables for Panning and Zooming
        self.scale = 1.1  # Zoom scale factor
        self.offset_x = 0  # Panning offset x
        self.offset_y = 0  # Panning offset y
        self.start_x = 0  # Initial click x
        self.start_y = 0  # Initial click y
        self.move_shape_x = 0 #Moving offset x
        self.move_shape_y = 0 #Moving offset y


        # Store the initial scale and offset to reset to later
        self.initial_scale = self.scale
        self.initial_offset_x = self.offset_x
        self.initial_offset_y = self.offset_y



        
        # Keep track of drawn shapes
        self.shape_ids = {}
        self.selected_shape = None
        self.prev_x = None
        self.prev_y = None


        






        # Binding Mouse Events
        self.canvas.bind("<ButtonPress-1>", self.start_pan)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<MouseWheel>", self.zoom)
        self.m.bind("<Configure>", self.resize_canvas)




    def on_drag(self, event):
        """Handle drag motion."""
        if self.selected_shape:
            # If a shape is selected, move the shape
            self.move_shape(event)
        else:
            # If no shape is selected, pan the canvas
            self.pan_canvas(event)



    def resize_canvas(self, event):
        # Get the current window size
        window_width = self.m.winfo_width()
        window_height = self.m.winfo_height()

        # Calculate the new canvas size as a percentage of the window size
        new_canvas_width = int(window_width * self.canvas_width_percentage)
        new_canvas_height = int(window_height * self.canvas_height_percentage)

        # Update the canvas size
        self.canvas.config(width=new_canvas_width, height=new_canvas_height)


    def zoom_in(self):
        self.scale *= 1.1
        self.update_canvas()

    def zoom_out(self):
        self.scale /= 1.1
        self.update_canvas()

    def zoom(self, event):
        zoom_factor = 1.1 if event.delta > 0 else 0.9

        # Adjust offset to zoom relative to cursor
        self.offset_x += (event.x - self.offset_x) * (1 - zoom_factor)
        self.offset_y += (event.y - self.offset_y) * (1 - zoom_factor)

        self.scale *= zoom_factor
        self.update_canvas()

    def start_pan(self, event):
        if self.selected_shape is None:
            self.start_x = event.x   # Adjust by current offset to prevent "jump"
            self.start_y = event.y
        self.prev_x =event.x
        self.prev_y =event.y
        print(self.prev_x, self.prev_y)
        
        

    def pan_canvas(self, event):
        if self.selected_shape is None:
            dx = event.x - self.start_x
            dy = event.y - self.start_y
            self.offset_x += dx
            self.offset_y += dy


            self.start_x = event.x
            self.start_y = event.y
            self.update_canvas()

    def back_to_center(self):
        # Reset scale and offset to their initial values
        self.scale = self.initial_scale
        self.offset_x = self.initial_offset_x
        self.offset_y = self.initial_offset_y

        # Update the canvas to reflect the reset state
        self.update_canvas()

    def update_canvas(self):
        #Clear the canvas
        self.canvas.delete("all")
        
        #Iterate over the list of shapes and draw them with adjusted coordinates
        for shape_id, shape_data in self.shape_ids.items():
            
            shape_type = shape_data["type"]
            x1, y1, x2, y2 = shape_data["coords"]

            # Adjust coordinates for scale and offset (without modifying original coords)
            adj_x1 = (x1 * self.scale) + self.offset_x + self.move_shape_x
            adj_y1 = (y1 * self.scale) + self.offset_y + self.move_shape_y
            adj_x2 = (x2 * self.scale) + self.offset_x + self.move_shape_x
            adj_y2 = (x2 * self.scale) + self.offset_y + self.move_shape_y


            # Redraw the shapes with updated coordinates
            if shape_type == "Circle":
                new_id = self.canvas.create_oval(adj_x1, adj_y1, adj_x2, adj_y2, fill="blue", outline=shape_data['outline'], width =shape_data['width'], tags=("shape", shape_id))
            elif shape_type == "Square":
                new_id = self.canvas.create_rectangle(adj_x1, adj_y1, adj_x2, adj_y2, fill="green", outline=shape_data['outline'], width =shape_data['width'], tags=("shape", shape_id))
            elif shape_type == "Triangle":
                points = [adj_x1, adj_y2, (adj_x1 + adj_x2) / 2, adj_y1, adj_x2, adj_y2]
                new_id = self.canvas.create_polygon(points, fill="yellow", outline=shape_data['outline'], width =shape_data['width'], tags=("shape", shape_id))


            # Update the shape ID map
            self.shape_ids[shape_id][shape_id] = new_id




            #Bind the select_shape
            self.canvas.bind("<ButtonRelease-1>", self.select_shape)
            


            
            
            

            # Highlight if selected
            if shape_id == self.selected_shape:
                self.canvas.itemconfig(new_id, outline="red", width = 2)

            




    def add_shape(self, shape_type):


        # Define an offset feature for shapes
        offset_x = 20  # Horizontal offset (pixels)
        offset_y = 20  # Vertical offset (pixels)

        # Get the position of the last shape or set the starting position if it's the first shape
        if len(self.shape_ids) == 0:
            # Starting position for the first shape
            x1, y1 = 100, 100
            x2, y2 = 200, 200  # Bottom-right corner'
        else:
            # Offset the position based on the last shape's coordinates
            last_shape_index = max(self.shape_ids.keys())  # Get the last added shape index
            last_shape = self.shape_ids[last_shape_index]
            x1, y1, _, _ = last_shape['coords']  # Get the coordinates of the last shape
            # Apply the offset
            x1 += offset_x
            y1 += offset_y

            x2, y2 = x1 + 100, y1 + 100  # Calculate the bottom-right corner based on the new position
            

        #Main shape logic

        shape_index = len(self.shape_ids) + 1 #Get index of shape_id based on how many shapes come before it in the list
        self.shape_ids[shape_index] = {
            "type": shape_type,
            "coords": (x1, y1, x2, y2),
            "outline": "black",
            "width": 1,
        }

        if shape_type == "Circle":
                canvas_id = self.canvas.create_oval(x1, y1, x2, y2, fill="blue", outline=self.shape_ids[shape_index]['outline'], width =self.shape_ids[shape_index]['width'], tags=(shape_index))
        elif shape_type == "Square":
                canvas_id = self.canvas.create_rectangle(x1, y1, x2, y2, fill="blue", outline=self.shape_ids[shape_index]['outline'], width =self.shape_ids[shape_index]['width'], tags=(shape_index))
        elif shape_type == "Triangle":
                points = [x1, y2, (x1 + x2) / 2, y1, x2, y2]
                canvas_id = self.canvas.create_polygon(points, fill="yellow", outline=self.shape_ids[shape_index]['outline'], width =self.shape_ids[shape_index]['width'], tags=(shape_index))



        # Store the canvas ID in the shape dictionary
        self.shape_ids[shape_index][shape_index] = canvas_id


        print(self.shape_ids)
        self.update_canvas()


    
    def select_shape(self, event):
        prev_selected = self.selected_shape
        #Check if coords in a shape and then make it highlighted if so
        for shape_id, shape_data in self.shape_ids.items():  
            real_id = shape_data[shape_id]
            if self.check_if_inside(event, real_id):    
                # Highlight the selected shape
                self.selected_shape = shape_id
                self.prev_x = event.x
                self.prev_y = event.y
                self.update_canvas()
                return 

        if self.selected_shape == prev_selected:
            self.selected_shape = None
            self.update_canvas()


    def move_shape(self, event):
        if self.selected_shape:
            

            print(event.x, event.y, self.prev_x, self.prev_y)
            #Difference between previous event coords
            self.move_shape_x = event.x - self.prev_x
            self.move_shape_y = event.y - self.prev_y
            
            
            # Update the previous position to the current mouse position
            #self.prev_x = event.x
            #self.prev_y = event.y
            self.update_canvas()




    





    def check_if_inside(self, event, real_index):
        # Get the bounding box of the shape
        
        bbox = self.canvas.bbox(real_index)
        
        # Get the event coordinates
        x_event = event.x
        y_event = event.y
        
        # Check if the event coordinates are inside the bounding box
        x1, y1, x2, y2 = bbox
        if x1 <= x_event <= x2 and y1 <= y_event <= y2:
            return True
        else:
            return False

     
        



    def find_closest_shape(self, click_x, click_y):
        closest_shape_id = None
        closest_distance = float('inf')  # Start with an infinitely large distance
        
        for shape_id, shape_data in self.shape_ids.items():
            shape_type = shape_data["type"]
            coords = shape_data["coords"]
            
            # For a rectangular shape, you can calculate the center of the bounding box
            if shape_type == "Square":
                x1, y1, x2, y2 = coords
                center_x = (x1 + x2) / 2
                center_y = (y1 + y2) / 2
            # For a circle, the center is already in the coords
            elif shape_type == "Circle":
                x1, y1, x2, y2 = coords
                center_x = (x1 + x2) / 2
                center_y = (y1 + y2) / 2
            # For a triangle, find the center of the bounding box or centroid
            elif shape_type == "Triangle":
                x1, y1, x2, y2 = coords
                center_x = (x1 + x2) / 2
                center_y = (y1 + y2) / 2
            else:
                continue  # Skip unsupported shape types
            
            # Calculate the Euclidean distance between the click and the shape's center
            distance = math.sqrt((click_x - center_x) ** 2 + (click_y - center_y) ** 2)
            
            # If this distance is the closest we've found, update the closest shape
            if distance < closest_distance:
                closest_distance = distance
                closest_shape_id = shape_id
        
        return closest_shape_id
        









class MenuButtons:
    def __init__(self, m, main_menu):
        self.m = m

        self.main_menu = main_menu
        

    def create_menu(self, menu_name, tabs=None):
        """
        Create a Menubutton with an optional set of cascading tabs.
        :param menu_name: The name of the menu (e.g., "File", "Edit").
        :param tabs: A list of tab names for cascading menus (optional).
        """
        # Create the Menubutton
        menu_obj = Menu(self.main_menu)
        self.main_menu.add_cascade(label = menu_name, menu = menu_obj)
        

        # Add cascading tabs if provided
        if tabs:
            for item in tabs:
                if item[0] != 'separator':
                    menu_obj.add_command(label = item[0], command = item[1])
                else:
                    menu_obj.add_separator()

        return menu_obj



    def placeholder(self):
        print("This feature is not implemented yet!")



    def create_submenu(self, parent_menu, submenu_name, submenu_tabs=None):
        """
        Create a submenu under an existing menu.
        :param parent_menu: The parent menu where the submenu will be added.
        :param submenu_name: The name of the submenu.
        :param submenu_tabs: A list of tab names and commands for the submenu.
        """
        # Create the Submenu
        submenu = Menu(parent_menu, tearoff=0)
        parent_menu.add_cascade(label=submenu_name, menu=submenu)

        # Add submenu tabs if provided
        if submenu_tabs:
            for item in submenu_tabs:
                if item[0] != 'separator':
                    submenu.add_command(label=item[0], command=item[1])
                else:
                    submenu.add_separator()

        return submenu  # Return the submenu object for further customization




    #Menu functions

    def end(self):
        self.m.quit()
        self.m.destroy()









#Main Menu 
main_menu = Menu(m)
m.config(menu = main_menu)


#Make out class objects
cc = PanZoomCanvasApp(m)
mbs = MenuButtons(m, main_menu)



#Menus inside main menu
mbs.create_menu("File", 
    [
    ("Save Canvas as Image", mbs.placeholder),
    ("Export", mbs.placeholder),
    ("Clear Canvas", mbs.placeholder),
    ("Undo", mbs.placeholder),
    ("Canvas Settings", mbs.placeholder),
    ("Exit", mbs.end) #Passes function reference instead of calling the funciton

    ])
mbs.create_menu('Edit',
    tabs = [
        ("Undo", mbs.placeholder),
        ("Redo", mbs.placeholder),
        ("separator", None),
        ("Cut", mbs.placeholder),
        ("Copy", mbs.placeholder),
        ("Paste", mbs.placeholder),
        ("separator", None),
        ("Delete", mbs.placeholder),
        ("Clear Canvas", mbs.placeholder),
        ("separator", None),
        ("Resize/Scale", mbs.placeholder),
        ("Rotate", mbs.placeholder),
        ("Change Properties", mbs.placeholder),
        ("Zooming", mbs.placeholder),
    ])


add_menu = mbs.create_menu("Add")
shape_submenu = mbs.create_submenu(add_menu, "Add Shape",
    [
        ("Circle", lambda: cc.add_shape("Circle")),
        ("Square", lambda: cc.add_shape("Square")),
        ("Triangle", lambda: cc.add_shape("Triangle"))
    ]
)













#Runs the main loop for the application
m.mainloop()



