import tkinter as tk
import math
from tkinter import *
from tkinter import colorchooser
from tkinter import simpledialog
from tkinter import ttk
from PIL import Image, ImageTk 
import tkinter.font as tkfont



#Application object/configuration
m = tk.Tk(screenName = "Mindmapper", className = 'Mindmapper')
m.title("Mindmapper")
m.geometry('800x600')
is_fullscreen = False








#Application Functions/Bindings
#--------------------------------------------------------------------------------------------
def toggle_fullscreen(event=None):
    global is_fullscreen
    is_fullscreen = not is_fullscreen
    if is_fullscreen:
        m.attributes("-fullscreen", True)  # Enable fullscreen
    else:
        m.attributes("-fullscreen", False)  # Disable fullscreen
        m.geometry("800x600")  # Set the window size to 600x600
    



# Exit full-screen mode with the Escape key
m.bind("<Escape>", toggle_fullscreen)






#Configure main grid
for i in range(3):
    m.grid_rowconfigure(i, weight=1)  # Rows expand proportionally
    m.grid_columnconfigure(i, weight=1)

 
m.grid_columnconfigure(0, weight=20, uniform = 'resize')  # PanedWindow column
m.grid_columnconfigure(1, weight=75, uniform = 'resize')  # Canvas column (more weight = wider)
m.grid_columnconfigure(2, weight=5, uniform = 'resize')




#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------




class ShapeCanvas:
    def __init__(self, m):
        #Pass in main window
        self.m = m

    
        # Create the Canvas
        self.canvas = tk.Canvas(self.m, bg="white")
        self.canvas.grid(row = 1, column = 1, sticky = 'nsew')
        for i in range(3):
            self.canvas.grid_rowconfigure(i, weight=0)  # Rows expand proportionally
            self.canvas.grid_columnconfigure(i, weight=1) #Columns expand proportionally


        #Tool Panel Setup
        #--------------------------------------------------------------------------------------------

        tool_panel = PanedWindow(bd = 4, relief = 'ridge', bg = "#969998", orient = tk.VERTICAL)
        tool_panel.grid(row = 0, column = 0,  rowspan=3, sticky='nsew', padx = (10, 10), pady = (10, 10))

        #Panel Title
        panel_title = Label(tool_panel, text = "Tool Customization")
        tool_panel.add(panel_title, minsize = 20)
        tool_panel.paneconfig(panel_title, stretch = "never")


        #Text Pane
        text_pane = tk.Frame(tool_panel, bg="lightblue", bd = 5)
        tool_panel.add(text_pane, minsize=200)
        tool_panel.paneconfig(text_pane, stretch = "always")

        #Text Pane Configuration
        text_pane.grid_rowconfigure(0, weight = 0)
        text_pane.grid_rowconfigure(1, weight = 0)
        text_pane.grid_rowconfigure(2, weight = 1)
        for i in range(3, 8):
            text_pane.grid_rowconfigure(i, weight = 1)
        text_pane.grid_columnconfigure(0, weight = 1)
        text_pane.grid_columnconfigure(1, weight = 1)
    
        

        #Text Label 
        add_text = Label(text_pane, text = "Add Text to Shape", width = 15, bg = 'lightblue')
        add_text.grid(row = 0, column = 0, sticky = 'w')


        #Text Entry/Apply Button
        self.text_entry = tk.Text(text_pane, height = 10, width = 100)
        self.text_entry.grid(row = 1, column = 0, padx=10, sticky = 'n')


        #Text Font Combobox
        font_family_label = Label(text_pane, text = 'Choose Font', width = 10, bg = 'lightblue')
        font_family_label.grid(row = 2, column = 0)
        self.font_combobox = ttk.Combobox(
            text_pane,
            values=['Academy Engraved LET', 'Adelle Sans Devanagari', 'AkayaKanadaka', 'AkayaTelivigala', 'Al Bayan', 'Al Nile', 'Al Tarikh', 'American Typewriter', 'Andale Mono',
            'Annai MN', 'Apple Braille', 'Apple Chancery', 'Apple Color Emoji', 'Apple LiGothic', 'Apple LiSung', 'Apple SD Gothic Neo', 'Apple Symbols', 'AppleGothic', 'AppleMyungjo',
            'Arial', 'Arial Black', 'Arial Hebrew', 'Arial Hebrew Scholar', 'Arial Narrow', 'Arial Rounded MT Bold', 'Arial Unicode MS', 'Arima Koshi', 'Arima Madurai', 'Avenir', 'Avenir Next',
            'Avenir Next Condensed', 'Ayuthaya', 'Baghdad', 'Bai Jamjuree', 'Baloo 2', 'Baloo Bhai 2', 'Baloo Bhaijaan', 'Baloo Bhaina 2', 'Baloo Chettan 2', 'Baloo Da 2', 'Baloo Paaji 2', 'Baloo Tamma 2',
            'Baloo Tammudu 2', 'Baloo Thambi 2', 'Bangla MN', 'Bangla Sangam MN', 'Baoli SC', 'Baoli TC', 'Baskerville', 'Beirut', 'BiauKaiHK', 'BiauKaiTC', 'Big Caslon', 'BM Dohyeon', 'BM Hanna 11yrs Old',
            'BM Hanna Air', 'BM Hanna Pro', 'BM Jua', 'BM Kirang Haerang', 'BM Yeonsung', 'Bodoni 72', 'Bodoni 72 Oldstyle', 'Bodoni 72 Smallcaps', 'Bodoni Ornaments', 'Bradley Hand', 'Brush Script MT', 
            'Cambay Devanagari', 'Chakra Petch', 'Chalkboard', 'Chalkboard SE', 'Chalkduster', 'Charm', 'Charmonman', 'Charter', 'Cochin', 'Comic Sans MS', 'Copperplate', 'Corsiva Hebrew', 'Courier New', 
            'Damascus', 'DecoType Naskh', 'Devanagari MT', 'Devanagari Sangam MN', 'Didot', 'DIN Alternate', 'DIN Condensed', 'Diwan Kufi', 'Diwan Thuluth', 'Euphemia UCAS', 'Fahkwang', 'Farah', 'Farisi', 
            'Futura', 'Galvji', 'GB18030 Bitmap', 'Geeza Pro', 'Geneva', 'Georgia', 'Gill Sans', 'Gotu', 'Grantha Sangam MN', 'Gujarati MT', 'Gujarati Sangam MN', 'GungSeo', 'Gurmukhi MN', 'Gurmukhi MT', 
            'Gurmukhi Sangam MN', 'Hannotate SC', 'Hannotate TC', 'HanziPen SC', 'HanziPen TC', 'HeadLineA', 'Hei', 'Heiti SC', 'Heiti TC', 'Helvetica', 'Helvetica Neue', 'Herculanum', 'Hiragino Maru Gothic ProN', 
            'Hiragino Mincho ProN', 'Hiragino Sans', 'Hiragino Sans CNS', 'Hiragino Sans GB', 'Hoefler Text', 'Hubballi', 'Impact', 'InaiMathi', 'ITF Devanagari', 'ITF Devanagari Marathi', 'Jaini', 'Jaini Purva', 
            'K2D', 'Kai', 'Kailasa', 'Kaiti SC', 'Kaiti TC', 'Kannada MN', 'Kannada Sangam MN', 'Katari', 'Kavivanar', 'Kefa', 'Khmer MN', 'Khmer Sangam MN', 'Klee', 'Kodchasan', 'Kohinoor Bangla', 'Kohinoor Devanagari', 
            'Kohinoor Gujarati', 'Kohinoor Telugu', 'KoHo', 'Kokonor', 'Krub', 'Krungthep', 'KufiStandardGK', 'Lahore Gurmukhi', 'Lantinghei SC', 'Lantinghei TC', 'Lao MN', 'Lao Sangam MN', 'Lava Devanagari', 'Lava Kannada', 
            'Lava Telugu', 'Libian SC', 'Libian TC', 'LiHei Pro', 'LingWai SC', 'LingWai TC', 'LiSong Pro', 'Lucida Grande', 'Luminari', 'Maku', 'Malayalam MN', 'Malayalam Sangam MN', 'Mali', 'Marker Felt', 'Menlo', 'Microsoft Sans Serif',
            'Mishafi', 'Mishafi Gold', 'Modak', 'Monaco', 'Mshtakan', 'Mukta', 'Mukta Mahee', 'Mukta Malar', 'Mukta Vaani', 'Muna', 'Myanmar MN', 'Myanmar Sangam MN', 'Nadeem', 'Nanum Brush Script', 'Nanum Gothic', 'Nanum Myeongjo',
            'Nanum Pen Script', 'New Peninim MT', 'Niramit', 'Noteworthy', 'Noto Nastaliq Urdu', 'Noto Sans Batak', 'Noto Sans Kannada', 'Noto Sans Myanmar', 'Noto Sans NKo', 'Noto Sans Oriya', 'Noto Sans Tagalog', 'Noto Serif Kannada',
            'Noto Serif Myanmar', 'October Compressed Devanagari', 'October Compressed Tamil', 'October Condensed Devanagari', 'October Condensed Tamil', 'October Devanagari', 'October Tamil', 'Optima', 'Oriya MN', 'Oriya Sangam MN', 'Osaka',
            'Padyakke Expanded One', 'Palatino', 'Papyrus', 'Party LET', 'PCMyungjo', 'Phosphate', 'PilGi', 'PingFang HK', 'PingFang SC', 'PingFang TC', 'Plantagenet Cherokee', 'PSL Ornanong Pro', 'PT Mono', 'PT Sans', 'PT Sans Caption', 'PT Sans Narrow', 
            'PT Serif', 'PT Serif Caption', 'Raanana', 'Rockwell', 'Sama Devanagari', 'Sama Gujarati', 'Sama Gurmukhi', 'Sama Kannada', 'Sama Malayalam', 'Sama Tamil', 'Sana', 'Sarabun', 'Sathu', 'Savoye LET', 'SF Compact', 'SF Compact Display', 'SF Compact Rounded', 
            'SF Compact Text', 'SF Pro', 'SF Pro Display', 'SF Pro Rounded', 'SF Pro Text', 'Shobhika', 'Shree Devanagari 714', 'SignPainter', 'Silom', 'SimSong', 'Sinhala MN', 'Sinhala Sangam MN', 'Skia', 'Snell Roundhand', 'Songti SC', 'Songti TC', 'Srisakdi', 'STFangsong', 
            'STHeiti', 'STIX Two Math', 'STIX Two Text', 'STKaiti', 'STSong', 'Sukhumvit Set', 'Symbol', 'Tahoma', 'Tamil MN', 'Tamil Sangam MN', 'Telugu MN', 'Telugu Sangam MN', 'Thonburi', 'Times New Roman', 'Tiro Bangla', 'Tiro Devanagari Hindi', 'Tiro Devanagari Marathi', 
            'Tiro Devanagari Sanskrit', 'Tiro Gurmukhi', 'Tiro Kannada', 'Tiro Tamil', 'Tiro Telugu', 'Toppan Bunkyu Gothic', 'Toppan Bunkyu Midashi Gothic', 'Toppan Bunkyu Midashi Mincho', 'Toppan Bunkyu Mincho', 'Trattatello', 'Trebuchet MS', 
            'Tsukushi A Round Gothic', 'Tsukushi B Round Gothic', 'Verdana', 'Waseem', 'Wawati SC', 'Wawati TC', 'Webdings', 'Wingdings', 'Wingdings 2', 'Wingdings 3', 'Xingkai SC', 'Xingkai TC', 'Yuanti SC', 'Yuanti TC', 'YuGothic', 
            'YuKyokasho', 'YuKyokasho Yoko', 'YuMincho', 'YuMincho +36p Kana', 'Yuppy SC', 'Yuppy TC', 'Zapf Dingbats', 'Zapfino'],
            state="readonly",
            width = 7
        )
        self.font_combobox.set("Arial")  #Default


        #Text Font Size Combobox
        font_sizes_label = Label(text_pane, text = 'Choose Font Size', width = 15, bg = 'lightblue')
        font_sizes_label.grid(row = 4, column = 0)


        big_font_sizes = list(range(14, 101, 4))
        font_sizes = [2, 4, 6, 8, 10, 12] + big_font_sizes 

        self.font_size_cb = ttk.Combobox(
            text_pane,
            values = font_sizes, 
            width = 5,
            height = 10,
        )
        self.font_size_cb.set("12")  #Default
        self.font_size_cb.grid(row = 5, column = 0)



        #Text Color

        # Variable to store chosen color
        self.chosen_color = tk.StringVar(value="#000000")  # Default to black

        choose_color_frame = Frame(text_pane, bg = 'lightblue')
        choose_color_frame.grid(row = 6, column = 0)
        
        color_button = tk.Button(choose_color_frame, text="Choose Font Color", command=self.choose_color, bg = 'lightblue')
        color_button.pack(side = RIGHT)

        # Canvas to display the chosen color
        self.color_display_canvas = tk.Canvas(choose_color_frame, width=30, height=30, bg=self.chosen_color.get(), highlightthickness=1, relief="solid")
        self.color_display_canvas.pack(side = LEFT, padx = (0, 10))






        #Text Bold
        #Text Italics
        #Text Alignment








        apply_text_button = tk.Button(text_pane, text="Apply Text", command=self.apply_text_to_shape, highlightbackground = 'lightblue', bd = 5)
        apply_text_button.grid(row = 7, column = 0, columnspan = 2, sticky = 'n' )




















        #Bottom Pane
        bottom_pane = tk.Frame(tool_panel, bg="lightgreen")
        tool_panel.add(bottom_pane, minsize = 200)
        tool_panel.paneconfig(bottom_pane, stretch = "never")

        
        # Load and resize the image using Pillow
        original_image = Image.open("plus_icon.png")
        resized_image = original_image.resize((40, 40), Image.Resampling.LANCZOS)  # Resize to 20x20 pixels
        self.plus_image = ImageTk.PhotoImage(resized_image)




        

        #Add Shape Button
        self.add_shape_button = tk.Button(
            bottom_pane, image = self.plus_image,
            command = self.show_shape_options, 
            width = 50, height = 50,
            cursor = 'hand2', border = 0,
            highlightbackground='lightgreen', 
            highlightcolor='lightgreen',
            activebackground='lightgreen',
            bg='lightgreen',
         )
        self.add_shape_button.pack(padx = (30, 0), pady = (30, 0), anchor = 'nw')

        

        
        #Shape Combobox to select shape type
        self.shape_combobox = ttk.Combobox(bottom_pane, values=["Circle", "Square", "Triangle"], state="readonly", width = 7)
        self.shape_combobox.set("Circle")  # Default to Rectangle

        # Apply button to confirm shape selection
        self.apply_button = tk.Button(bottom_pane, text="OK", command=self.apply_shape, highlightbackground = 'lightgreen', cursor = 'hand2')







        # Inner Canvas Buttons
        #--------------------------------------------------------------------------------------------

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
        self.scale = 1.0  # Zoom scale factor
        self.offset_x = 0  # Panning offset x
        self.offset_y = 0  # Panning offset y
        self.dx = 0
        self.dy = 0

        # Set the percentage of the window size for the canvas
        self.canvas_width_percentage = 0.6  # 70% of the window width
        self.canvas_height_percentage = 0.7  # 70% of the window height

        #Shape Data/Intialization
        self.shape_ids = {}
        self.selected_shape = None
        
        
        

        # Store the initial scale and offset to reset for backToCenter Button
        self.initial_scale = self.scale
        self.initial_offset_x = self.offset_x
        self.initial_offset_y = self.offset_y
        self.initial_x = 0
        self.initial_y = 0

        

        # Binding Mouse Events
        self.canvas.bind("<ButtonPress-1>", self.onLeftClick)
        self.canvas.bind("<B1-Motion>", self.onDrag)
        self.canvas.bind("<ButtonRelease-1>", self.onRelease)
        self.canvas.bind("<Button-2>", self.onRightClick)
        self.canvas.bind("<MouseWheel>", self.zoom)
        self.m.bind("<Configure>", self.resize_canvas)


#Setup Configuration functions
#--------------------------------------------------------------------------------------------

    def resize_canvas(self, event):
        # Get the current window size
        window_width = self.m.winfo_width()
        window_height = self.m.winfo_height()

        # Calculate the new canvas size as a percentage of the window size
        new_canvas_width = int(window_width * self.canvas_width_percentage)
        new_canvas_height = int(window_height * self.canvas_height_percentage)

        # Update the canvas size
        self.canvas.config(width=new_canvas_width, height=new_canvas_height)


    def show_shape_options(self):
        # Show ComboBox for shape selection
        self.shape_combobox.pack(padx=10, pady=10, anchor = 'sw')
        self.apply_button.pack(padx=(27, 0), pady=10, anchor = 'sw')

        # Disable the "Add Shape" button once the ComboBox is visible
        self.add_shape_button.config(state="disabled")


    def apply_shape(self):
        shape_type = self.shape_combobox.get()
        self.add_shape(shape_type)
        self.shape_combobox.pack_forget()  # Hide the ComboBox after selection
        self.apply_button.pack_forget()   # Hide the Apply button
        self.add_shape_button.config(state="normal")  # Re-enable the Add Shape button






#Click/Motion Event functions 
#--------------------------------------------------------------------------------------------


    def onLeftClick(self, event):
        print(self.shape_ids)
        if self.selected_shape is None:
            self.start_pan(event)

        #Save the click coords
        self.set_initial_click(event)

    def onDrag(self, event):
        """Handle drag motion."""
        if self.selected_shape:
            # If a shape is selected, move the shape
            self.move_shape(event)
            
        elif not self.check_inside_all(event) and not self.selected_shape:
            # If no shape is selected, pan the canvas
            self.pan_canvas(event)

    def onRelease(self, event):
        self.select_shape(event)
        


    def onRightClick(self, event):
        #If the click is in a shape
        if self.check_inside_all(event):  

            #Make this the selected shape
            self.select_shape(event)

            self.shape_menu = tk.Menu(self.canvas, tearoff=0)
            self.shape_menu.add_command(label="Resize", command=self.open_resize_dialog)
            self.shape_menu.add_command(label="Delete", command=self.delete_selected_shape)
            self.shape_menu.add_separator()
            self.shape_menu.add_command(label="Change Color", command=self.change_shape_color)

            self.shape_menu.post(event.x_root, event.y_root)
        else:
            self.selected_shape = None


#Tool Menu Functions 
#--------------------------------------------------------------------------------------------

    def open_resize_dialog(self):
        
        if not self.selected_shape:
            return

        real_id = self.shape_ids[self.selected_shape][self.selected_shape]

        x1, y1, x2, y2 = self.canvas.bbox(real_id)
        current_width = x2 - x1
        current_height = y2 - y1

        # Prompt the user for new dimensions
        new_width = simpledialog.askinteger("Resize Shape", f"Enter new width (current: {current_width}):")
        new_height = simpledialog.askinteger("Resize Shape", f"Enter new height (current: {current_height}):")


        # Calculate the new coordinates
        cx = (x1 + x2) / 2  # Center x
        cy = (y1 + y2) / 2  # Center y
        half_width = new_width / 2
        half_height = new_height / 2

        new_x1 = cx - half_width
        new_y1 = cy - half_height
        new_x2 = cx + half_width
        new_y2 = cy + half_height

        #Update shape data
        self.shape_ids[self.selected_shape]['coords'] = (new_x1, new_y1, new_x2, new_y2)

        # Redraw all shapes
        self.draw_shapes()



    def delete_selected_shape(self):
        if self.selected_shape:
            del self.shape_ids[self.selected_shape]
            self.canvas.delete(self.selected_shape)
            self.text_entry.delete('1.0', tk.END)
            self.selected_shape = None
            self.draw_shapes()
            
    def change_shape_color(self):
        if self.selected_shape:
            get_color = colorchooser.askcolor()
            print(self.shape_ids[self.selected_shape][self.selected_shape])
            print(get_color, get_color[1])
            print(self.selected_shape)
            self.shape_ids[self.selected_shape]['color'] = get_color[1]
            self.draw_shapes()






#Panning/Zooming and Button Handling functions
#--------------------------------------------------------------------------------------------

    def set_initial_click(self, event):
        self.initial_x = event.x
        self.initial_y = event.y

        #Check if panned 
        if self.scale != 1:
            for shape_id, shape_data in self.shape_ids.items():
                self.shape_ids[shape_id]["coords"] = self.shape_ids[shape_id]["adj_coords"]
                original_font_size = shape_data['font_size']
                scaled_font_size = max(1, round(original_font_size * self.scale))
                self.shape_ids[shape_id]['font_size'] = scaled_font_size
            self.scale = 1.0
        print(self.initial_x, self.initial_y)

    def zoom_in(self):
        self.scale *= 1.1
        self.draw_shapes()

    def zoom_out(self):
        self.scale *= 0.9
        self.draw_shapes()

    def zoom(self, event):
        zoom_factor = 1.1 if event.delta > 0 else 0.9

        # Adjust offset to zoom relative to cursor
        self.offset_x += (event.x - self.offset_x) * (1 - zoom_factor)
        self.offset_y += (event.y - self.offset_y) * (1 - zoom_factor)

        self.scale *= zoom_factor
        self.draw_shapes()

    def start_pan(self, event):
        self.start_x = event.x   #First click to get starting coords of pan
        self.start_y = event.y
        
        
    #Calculate panning change and redraw shapes to reflect change
    def pan_canvas(self, event):
        dx = event.x - self.start_x
        dy = event.y - self.start_y
        self.offset_x += dx
        self.offset_y += dy
        self.start_x = event.x
        self.start_y = event.y
        self.draw_shapes()

    def back_to_center(self):
        # Reset scale and offset to their initial values
        self.scale = self.initial_scale
        self.offset_x = self.initial_offset_x
        self.offset_y = self.initial_offset_y
        self.dx = 0
        self.dy = 0
        self.selected_shape = None
        for shape_id, shape_data in self.shape_ids.items():
            shape_data["coords"] = shape_data['initial_coords']
        print(self.shape_ids)

        # Update the canvas to reflect the reset state
        self.draw_shapes()



#Shape Manager Functions
#--------------------------------------------------------------------------------------------

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





        # Calculate the center of the shape for placing the text
        text_x = (x1 + x2) / 2
        text_y = (y1 + y2) / 2

        # Create associated text object for shape (Default text)
        text_id = self.canvas.create_text(
            text_x,
            text_y,
            text="Default",  # Default or placeholder text
            font=("Arial", 12),
            fill="black"
        )

        shape_id = len(self.shape_ids) + 1

        self.shape_ids[shape_id] = {
            "type": shape_type,
            "coords": (x1, y1, x2, y2),
            "outline": "black",
            "width": 1,
            "initial_coords":(x1, y1, x2, y2),
            "color": 'blue',
            'text': None,
            'text_id': text_id,
            "font_size": 12,
            "font_family": "Arial",
            'style': '',
            'alignment': 'center',
            'text_color': 'black',
        }


        print(self.shape_ids)

        #When adding new shape, draw it on the screen
        self.draw_shapes() #Pass in specific id associated with the shape


    #For all shapes 
    def draw_shapes(self):
        self.canvas.delete("all")
        for shape_id, shape_data in self.shape_ids.items():
            shape_data = self.shape_ids[shape_id]
            shape_type = shape_data['type']
            original_font_size = shape_data["font_size"]
            x1, y1, x2, y2 = shape_data["coords"]

            adj_x1 = (x1 * self.scale) + self.offset_x + self.dx
            adj_y1 = (y1 * self.scale) + self.offset_y + self.dy
            adj_x2 = (x2 * self.scale) + self.offset_x + self.dx
            adj_y2 = (y2 * self.scale) + self.offset_y + self.dy

            
            shape_data['adj_coords'] = (adj_x1, adj_y1, adj_x2, adj_y2)
            

            

            # draw the shapes with updated coordinates
            if shape_type == "Circle":
                canvas_id = self.canvas.create_oval(adj_x1, adj_y1, adj_x2, adj_y2, fill=shape_data['color'], outline=shape_data['outline'], width =shape_data['width'])
            elif shape_type == "Square":
                canvas_id = self.canvas.create_rectangle(adj_x1, adj_y1, adj_x2, adj_y2, fill=shape_data['color'], outline=shape_data['outline'], width =shape_data['width'])
            elif shape_type == "Triangle":
                points = [adj_x1, adj_y2, (adj_x1 + adj_x2) / 2, adj_y1, adj_x2, adj_y2]
                canvas_id = self.canvas.create_polygon(points, fill=shape_data['color'], outline=shape_data['outline'], width =shape_data['width'], tags=("shape", shape_id))
            # Update the canvas id as the shape_id
            self.shape_ids[shape_id][shape_id] = canvas_id


            scaled_font_size = max(1, round(original_font_size * self.scale))
            font_family = shape_data['font_family']
            style = shape_data['style']
            text_color = shape_data['text_color']
            alignment = shape_data['alignment']


            # Draw associated text
            cx = (adj_x1 + adj_x2) / 2
            cy = (adj_y1 + adj_y2) / 2
            text = shape_data['text']
            text_id = self.canvas.create_text(cx, cy, text=text, font=("Arial", scaled_font_size, style), fill=text_color, width = adj_x2-adj_x1, anchor = alignment)
            self.shape_ids[shape_id]['text_id'] = text_id



    #For selected shapes only
    def destroy_and_redraw(self):
        #First delete shape and text with it
        item_id = self.shape_ids[self.selected_shape][self.selected_shape]
        text_id = self.shape_ids[self.selected_shape]['text_id']
        self.canvas.delete(item_id)
        self.canvas.delete(text_id)


        shape_data = self.shape_ids[self.selected_shape]
        shape_type = shape_data['type']
        original_font_size = shape_data["font_size"]
        x1, y1, x2, y2 = shape_data["coords"]

        adj_x1 = (x1 * self.scale) + self.offset_x + self.dx
        adj_y1 = (y1 * self.scale) + self.offset_y + self.dy
        adj_x2 = (x2 * self.scale) + self.offset_x + self.dx
        adj_y2 = (y2 * self.scale) + self.offset_y + self.dy

        shape_data['adj_coords'] = (adj_x1, adj_y1, adj_x2, adj_y2)
        

        # draw the shapes with updated coordinates
        if shape_type == "Circle":
            new_id = self.canvas.create_oval(adj_x1, adj_y1, adj_x2, adj_y2, fill=shape_data['color'], outline=shape_data['outline'], width =shape_data['width'])
        elif shape_type == "Square":
            new_id = self.canvas.create_rectangle(adj_x1, adj_y1, adj_x2, adj_y2, fill=shape_data['color'], outline=shape_data['outline'], width =shape_data['width'])
        elif shape_type == "Triangle":
            points = [adj_x1, adj_y2, (adj_x1 + adj_x2) / 2, adj_y1, adj_x2, adj_y2]
            new_id = self.canvas.create_polygon(points, fill=shape_data['color'], outline=shape_data['outline'], width =shape_data['width'])
        # Update the canvas id as the shape_id
        
        self.shape_ids[self.selected_shape][self.selected_shape] = new_id

        self.canvas.itemconfig(new_id, outline="red", width=2)

        # Draw associated text with all correct parameters in middle of shape
        scaled_font_size = max(1, round(original_font_size * self.scale))
        font_family = shape_data['font_family']
        style = shape_data['style']
        text_color = shape_data['text_color']
        alignment = shape_data['alignment']



        cx = (adj_x1 + adj_x2) / 2
        cy = (adj_y1 + adj_y2) / 2
        text = shape_data['text']
        text_id = self.canvas.create_text(cx, cy, text=text, font=(font_family, scaled_font_size, style), fill=text_color, width = adj_x2-adj_x1, anchor = alignment)
        self.shape_ids[self.selected_shape]['text_id'] = text_id





    def select_shape(self, event):
        #For handling previously selected shape
        prev_selected = self.selected_shape
        if prev_selected != None:
            canvas_id = self.shape_ids[prev_selected][prev_selected]
            self.canvas.itemconfig(canvas_id, outline= "black", width = 1)


        #Loop through all shapes and check if valid selection
        for shape_id, shape_data in self.shape_ids.items():  
            real_id = shape_data[shape_id]
            if self.check_if_inside(event, real_id):    
                

                # Highlight the new selected shape
                self.selected_shape = shape_id
                text_id = self.shape_ids[self.selected_shape]['text_id']
                existing_text = self.canvas.itemcget(text_id, "text")        
                self.text_entry.delete("1.0", tk.END)
                self.text_entry.insert('1.0', existing_text)
                

                #Update the coords of the shape after its release
                shape_data = self.shape_ids[self.selected_shape]
                x1, y1, x2, y2 = shape_data["coords"]
                if self.offset_x != 0 or self.offset_y != 0:   
                    #If zoom took place meaning self.scale was changed, then store the transformed cords of the selected shape in
                    for shape_id, shape_data in self.shape_ids.items():
                        self.shape_ids[shape_id]["coords"] = self.shape_ids[shape_id]["adj_coords"]
                    self.offset_x = 0
                    self.offset_y = 0
                else:
                    self.shape_ids[self.selected_shape]["coords"] = (x1 + self.dx, y1 + self.dy, x2 + self.dx, y2 + self.dy)

                self.dx = 0
                self.dy = 0
                self.destroy_and_redraw()
                return 


        #If selected_shape did not change and the cursor is not in a shape
        if self.selected_shape == prev_selected:
            self.selected_shape = None
            self.text_entry.delete('1.0', tk.END)
            self.draw_shapes()
        

    def move_shape(self, event):
        
        
        #Get the new position of this event
        new_x, new_y = event.x, event.y
        

        #Get change between new event and initial click
        self.dx = new_x - self.initial_x
        self.dy = new_y - self.initial_y

       
        #Transform the shapes by deleting all of them and updating position
        self.destroy_and_redraw()





    def apply_text_to_shape(self):
        # Apply the text from the entry to the selected shape
        if self.selected_shape:
            input_text = self.text_entry.get("1.0", tk.END).strip() 
            color = self.chosen_color.get() # Returns (RGB, hex)
    
            self.shape_ids[self.selected_shape]['text'] = input_text
            self.shape_ids[self.selected_shape]['text_color'] = color
            self.destroy_and_redraw()


    def choose_color(self):
        # Open the color chooser dialog
        color = colorchooser.askcolor(title="Choose Text Color")[1]  # Returns (RGB, hex)
        if color:  # Check if a color was chosen
            self.chosen_color.set(color)  # Update the stored color
            # Update the canvas to show the selected color
            self.color_display_canvas.config(bg=color)
            






#Helper Functions
#--------------------------------------------------------------------------------------------


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

    def check_inside_all(self, event):
        print(self.shape_ids)
        for shape_id, shape_data in self.shape_ids.items():
            #Exclude selected shape
            real_id = shape_data[shape_id]
            print(real_id)
            bbox = self.canvas.bbox(real_id)
            print(bbox)
            print(event.x, event.y)
        
            # Get the event coordinates
            x_event = event.x
            y_event = event.y
            
            # Check if the event coordinates are inside the bounding box
            x1, y1, x2, y2 = bbox
            if x1 <= x_event <= x2 and y1 <= y_event <= y2:
                return True
            
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




#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#MenuButtons Class



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






#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------




#Main Menu 
main_menu = Menu(m)
m.config(menu = main_menu)


#Make out class objects
sc = ShapeCanvas(m)
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
        ("Circle", lambda: sc.add_shape("Circle")),
        ("Square", lambda: sc.add_shape("Square")),
        ("Triangle", lambda: sc.add_shape("Triangle"))
    ]
)















#Runs the main loop for the application
m.mainloop()



