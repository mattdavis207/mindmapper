import math
import sqlite3
import os
import tkinter as tk
from tkinter import filedialog
from tkinter import *
from tkinter import colorchooser
from tkinter import simpledialog
from tkinter import ttk
from tkinter import messagebox
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
        self.canvas = tk.Canvas(self.m, bg="white", relief = 'ridge', bd = 10)
        self.canvas.grid(row = 1, column = 1, sticky = 'nsew')
        for i in range(3):
            self.canvas.grid_rowconfigure(i, weight=0)  # Rows expand proportionally
            self.canvas.grid_columnconfigure(i, weight=1) #Columns expand proportionally

        self.canvas.grid_rowconfigure(1, weight = 2)



        # Variables for Panning and Zooming
        self.scale = 1.0  # Zoom scale factor
        self.offset_x = 0  # Panning offset x
        self.offset_y = 0  # Panning offset y
        self.scroll_timer = None  # Timer to detect end of scrolling
        self.dx = 0
        self.dy = 0

        # Set the percentage of the window size for the canvas
        self.canvas_width_percentage = 0.6  # 70% of the window width
        self.canvas_height_percentage = 0.7  # 70% of the window height


        #Shape Data/Intialization
        self.shape_ids = {}
        self.line_ids = {} #We want a line id paired with line data 1: {line_id: canvas_id, 'initial_coords': (x1, y1, x2, y2), (coords: x1 = shape1cx, y2 = shape1cy, x2 = shape2cx, y2 = shape2cy)  }
        self.selected_shape = None
        self.selected_line= None
        self.current_select_two = [] #Needs to hold each shape canvas_id and real shape-id as well as middle coords based on the current coords of the shape 
        self.select_two_flag = False

        #Database Variables
        self.current_file = None #To Track the currently opened file
        
        
        

        # Store the initial scale and offset to reset for backToCenter Button
        self.initial_scale = self.scale
        self.initial_offset_x = self.offset_x
        self.initial_offset_y = self.offset_y
        self.initial_x = 0
        self.initial_y = 0


 

        #Tool Panel Setup
        #--------------------------------------------------------------------------------------------

        tool_panel = PanedWindow(bd = 4, relief = 'ridge', bg = "#969998", orient = tk.VERTICAL)
        tool_panel.grid(row = 0, column = 0,  rowspan=3, sticky='nsew', padx = (10, 10), pady = (10, 10))

        #Panel Title
        panel_title = Label(tool_panel, text = "Tool Customization", font = ('Andale Mono', 12))
        tool_panel.add(panel_title, minsize = 20)
        tool_panel.paneconfig(panel_title, stretch = "never")


        #Text Pane
        text_pane = tk.Frame(tool_panel, bg="lightblue", bd = 5)
        tool_panel.add(text_pane, minsize=400)
        tool_panel.paneconfig(text_pane, stretch = "always")

        
        #Text Pane---------------------------------------

        #Text Frame
        text_frame = Frame(text_pane, bg = 'lightblue')
        text_frame.pack(side = TOP, fill = 'x') 

        #To hold the left and right frames
        content_frame = Frame(text_pane, bg='lightblue')  # Container for left/right frames
        content_frame.pack(fill='x')   

        #Left Frame
        left_frame = Frame(content_frame, bg = 'lightblue')
        left_frame.pack(side = LEFT, padx = (20, 0))

        #Right Frame 
        right_frame = Frame(content_frame, bg = 'lightblue')
        right_frame.pack(side = RIGHT, padx = (0, 20))

        #Color Frame
        color_frame = Frame(text_pane, bg = 'lightblue')
        color_frame.pack(fill = 'x')

        
        #Apply Frame
        apply_frame = Frame(text_pane, bg = 'lightblue')
        apply_frame.pack(fill = 'x')

        #Separator Frame
        separator_frame = Frame(text_pane, height = 3)
        separator_frame.pack_propagate(False)
        separator_frame.pack(fill = 'x')


        #Line B 1st Row Frame
        lb1_frame = Frame(text_pane, bg = 'lightblue')
        lb1_frame.pack(fill = 'x')


        #Line B 2nd Row Frame
        lb2_frame = Frame(text_pane, bg = 'lightblue')
        lb2_frame.pack(fill = 'x')


        #Line B 3rd Row Frame
        lb3_frame = Frame(text_pane, bg = 'lightblue')
        lb3_frame.pack(fill = 'x')


        #Line B 4th Row Frame
        lb4_frame = Frame(text_pane, bg = 'lightblue')
        lb4_frame.pack(fill = 'x')
        



        #Text Label 
        add_text = Label(text_frame, text = "Add Text to Shape", width = 17, bg = 'lightblue', font = ('Courier New', 15, 'bold'))
        add_text.pack(side = TOP, anchor = 'w', expand = True)

        #Text Entry
        self.text_entry = tk.Text(text_frame, height = 10, width = 100)
        self.text_entry.pack(fill = 'x', side = BOTTOM)





        #Coding fonts: 'Andale Mono', 'Courier New', 'Menlo', 'Monaco', 'PT Mono'

        #Text Font Label
        font_family_label = Label(left_frame, text = 'Font', width = 10, bg = 'lightblue', font = ('Courier New', 15, 'bold'))
        font_family_label.pack(anchor = 'w')

        #Text Font Combobox
        self.font_combobox = ttk.Combobox(
            left_frame,
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
        self.font_combobox.pack(fill = 'x', padx = (0, 10))




        #Text Font Size Label
        font_sizes_label = Label(left_frame, text = 'Font Size', width = 10, bg = 'lightblue', font = ('Courier New', 15, 'bold'))
        font_sizes_label.pack(anchor = 'w')

        #Text Font Size Combobox
        big_font_sizes = list(range(14, 101, 4))
        font_sizes = [2, 4, 6, 8, 10, 12] + big_font_sizes 

        self.font_size_cb = ttk.Combobox(
            left_frame,
            values = font_sizes, 
            width = 7,
            height = 10,
        )
        self.font_size_cb.set("12")  #Default
        self.font_size_cb.pack(fill = 'x', padx = (0, 10))

        


        

        #Text Style Label
        choose_style_label = tk.Label(right_frame, text = 'Font Style', width = 10, bg = 'lightblue', font = ('Courier New', 15, 'bold'))
        choose_style_label.pack(anchor = 'w')

        #Text Style Combobox
        self.choose_style_cb = ttk.Combobox(right_frame, values = ["None", "bold", "italic", "underline", "overstrike"], state="readonly", width = 7)
        self.choose_style_cb.set('None')
        self.choose_style_cb.pack(fill = 'x', padx = (10, 0))


        #Text Alignment Label
        alignment_label = tk.Label(right_frame, text = 'Alignment', width = 10, bg = 'lightblue', font = ('Courier New', 15, 'bold'))
        alignment_label.pack(anchor = 'w')

        #Text Alignment Combobox
        self.alignment_cb = ttk.Combobox(right_frame, values = ['left', 'center', 'right'], state="readonly", width = 7)
        self.alignment_cb.set('center')
        self.alignment_cb.pack(fill = 'x', padx = (10, 0))
        

        #Text Color
        # Variable to store chosen color
        self.chosen_color = tk.StringVar(value="#000000")  # Default to black

        # Canvas to display the chosen color
        self.color_display_canvas = tk.Canvas(color_frame, width=30, height=30, bg=self.chosen_color.get(), highlightthickness=1, relief="solid")
        self.color_display_canvas.pack(side = LEFT, pady = (20, 0), padx = (40, 0))
        
        self.color_button = tk.Button(color_frame, text="Choose Font Color", command=self.choose_color, highlightbackground = 'lightblue')
        self.color_button.pack(side = RIGHT, pady = (20, 0), padx = (0, 15))

        
        #Apply Text Button
        self.apply_text_button = tk.Button(apply_frame, text="Apply Text",  bg = 'lightblue', command=self.apply_text_to_shape, highlightbackground = 'lightblue', font = ('Arial', 12, 'bold'))
        self.apply_text_button.pack(pady = 20)
        self.apply_text_button.config(state = 'disabled')




        #-----------------------------------------------------------------------


        #Separator between text and line fields
        separator = ttk.Separator(separator_frame, orient = 'horizontal')
        separator.pack(fill = 'x')


        #-----------------------------------------------------------------------


        #Color Canvas/Button Frame
        line_color_frame = Frame(lb1_frame, bg = 'lightblue')
        line_color_frame.pack(fill = 'x', pady = (30, 0))

        #Variable for chosen line color
        self.chosen_line_color = tk.StringVar(value = '#000000')

        #Canvas to store line color
        self.lcolor_display_canvas = tk.Canvas(line_color_frame, width=30, height=30, bg=self.chosen_line_color.get(), highlightthickness=1, relief="solid")
        self.lcolor_display_canvas.pack(side = LEFT, padx = (40, 0))

        #Fill Line Button
        self.line_color_button = tk.Button(line_color_frame, text="Choose Line Color", command=self.choose_line_color, highlightbackground = 'lightblue')
        self.line_color_button.pack(side = RIGHT, padx = (0, 15))


        #Line Width Label and Button Frame
        line_width_frame = tk.Frame(lb2_frame, bg= 'lightblue')
        line_width_frame.pack(fill = 'x', pady = (30, 0))

        #line Width Label and Button
        line_width_label = tk.Label(line_width_frame, text="Line Width", bg = 'lightblue', font = ('Courier New', 15, 'bold'))
        line_width_label.pack(side = LEFT, padx= (30, 0))
        self.line_width_combo = ttk.Combobox(line_width_frame, values = [2, 4, 6, 8, 10, 12, 14, 16, 18, 20])
        self.line_width_combo.pack(side = RIGHT, padx = 30)
        self.line_width_combo.set(2) #Default width value


        #Helper Frames
        lg_frame = Frame(lb3_frame, highlightbackground = 'lightblue', bg = 'lightblue')
        lg_frame.pack(side = TOP)

        cb_frame = Frame(lb3_frame, highlightbackground = 'lightblue', bg = 'lightblue')
        cb_frame.pack(side = BOTTOM) 
        
        # Label and Combo box for Dash Length
        dash_length_label = tk.Label(lg_frame, text="Dash Length", bg = 'lightblue', font = ('Courier New', 15, 'bold'))
        dash_length_label.pack(side = LEFT, padx = 20, pady  = (20, 0))
        self.dash_length_combo = ttk.Combobox(cb_frame, values=['None', 2, 4, 6, 8, 10], width=7)
        self.dash_length_combo.pack(side = LEFT, padx = 20)
        self.dash_length_combo.set('None')  # Default value

        # Label and Combo box for Dash Gap
        dash_gap_label = tk.Label(lg_frame, text="Dash Gap", bg = 'lightblue', font = ('Courier New', 15, 'bold'))
        dash_gap_label.pack(side = RIGHT, padx = 20, pady  = (20, 0))
        self.dash_gap_combo = ttk.Combobox(cb_frame, values=['None', 2, 4, 6, 8, 10], width=7)
        self.dash_gap_combo.pack(side = RIGHT, padx = 20)
        self.dash_gap_combo.set('None')  # Default value

        
        #Apply Line Button
        self.apply_line_button = tk.Button(lb4_frame, text = 'Apply to Line', command = self.apply_to_line, highlightbackground = 'lightblue', width = 9)
        self.apply_line_button.pack(pady = (30, 0), padx = 30)
        self.apply_line_button.config(state = 'disabled')


        


        #Bottom Pane-------------------------------------------------------------------------------------

        bottom_pane = tk.Frame(tool_panel, bg="lightgreen")
        tool_panel.add(bottom_pane, minsize = 200)
        tool_panel.paneconfig(bottom_pane, stretch = "never")

        add_buttons_frame = Frame(bottom_pane, bg = 'lightgreen')
        add_buttons_frame.pack(fill = 'x')

        
        # Load and resize the add and connection images using Pillow
        original_image1 = Image.open("plus_icon.png")
        resized_image1 = original_image1.resize((60, 60), Image.Resampling.LANCZOS)  # Resize to 20x20 pixels
        self.plus_image = ImageTk.PhotoImage(resized_image1)

        original_image2 = Image.open("connection_icon.png")
        resized_image2 = original_image2.resize((60, 60), Image.Resampling.LANCZOS)  # Resize to 20x20 pixels
        self.connect_image = ImageTk.PhotoImage(resized_image2)

        add_frame = Frame(add_buttons_frame, bg = 'lightgreen', bd = 5, relief = 'ridge')
        add_frame.pack(padx = (50, 0), pady = (30, 0), side = LEFT)


        #Add Shape Button
        self.add_shape_button = tk.Button(
            add_frame, image = self.plus_image,
            command = self.show_shape_options, 
            width = 55, height = 55,
            cursor = 'hand2',
            highlightcolor='lightgreen',
            bg='lightgreen',
         )
        self.add_shape_button.pack(expand = True)


        con_frame = Frame(add_buttons_frame, bg = 'lightgreen', bd = 5, relief = 'ridge')
        con_frame.pack(padx = (0, 50), pady = (30, 0), side = RIGHT)

        #Add Connection Button
        self.add_connection_button = tk.Button(
            con_frame, image = self.connect_image,
            command = self.add_connection,
            width = 55, height = 55, 
            cursor = 'hand2', 
            highlightcolor='lightgreen',
            bg='lightgreen'
            )
        self.add_connection_button.pack(expand = True)

        

        
        #Shape Combobox to select shape type
        self.shape_combobox = ttk.Combobox(bottom_pane, values=["Circle", "Square", "Triangle"], state="readonly", width = 7)
        self.shape_combobox.set("Circle")  # Default to Rectangle

        # Apply button to confirm shape selection
        self.apply_button = tk.Button(bottom_pane, text="OK", command=self.apply_shape, highlightbackground = 'lightgreen', cursor = 'hand2')











        # Inner Canvas Buttons/Text
        #--------------------------------------------------------------------------------------------

        # Create some Frames for Buttons
        button_frame_1 = tk.Frame(self.canvas, highlightbackground = 'white')
        button_frame_1.grid(row = 0, column = 2, sticky = 'e', pady = (15,0), padx = (0, 15))
        button_frame_1.grid_rowconfigure(0, weight = 1)
        button_frame_2 = tk.Frame(self.canvas, highlightbackground = 'white')
        button_frame_2.grid(row = 0, column = 0, sticky ='w', pady = (15, 0), padx = (15, 0))

        # Zoom In Button
        self.zoom_in_button = tk.Button(button_frame_1, text="+", relief = 'sunken', highlightbackground = 'white', highlightthickness = 0, command=self.zoom_in)
        self.zoom_in_button.grid(row = 0, column = 1)
        
        # Zoom Out Button
        self.zoom_out_button = tk.Button(button_frame_1, text="-", relief = 'sunken', command=self.zoom_out, highlightbackground = 'white', highlightthickness = 0)
        self.zoom_out_button.grid(row = 0, column = 0)

        #Back to Center Button
        self.btc_button = tk.Button(button_frame_2, text="Back to Center", relief = 'ridge', highlightbackground = 'white', highlightthickness = 0, command = self.back_to_center)
        self.btc_button.grid(row = 0, column = 0, sticky = 'nsew')

        #File Label/Display
        self.file_label = tk.Label(self.canvas, text = f'File: {self.current_file}', foreground = 'black', font = ('Andale Mono', 12), bg = 'white')
        self.file_label.grid(row = 3, column = 0, sticky = 'sw', padx = (20, 0), pady = (0, 20))







        

        # Binding Mouse Events
        self.canvas.bind("<ButtonPress-1>", self.onLeftClick)
        self.canvas.bind("<B1-Motion>", self.onDrag)
        self.canvas.bind("<ButtonRelease-1>", self.onRelease)
        self.canvas.bind("<Button-2>", self.onRightClick)
        self.canvas.bind("<MouseWheel>", self.zoom)
        self.m.bind("<Configure>", self.resize_canvas)



#Database functions
#--------------------------------------------------------------------------------------------

    def initialize_database(self, db_path):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()

        # Create shapes table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS shapes (
                shape_id INTEGER PRIMARY KEY,
                type TEXT,
                coords TEXT,
                outline TEXT,
                width INTEGER,
                initial_coords TEXT,
                color TEXT,
                text TEXT,
                text_id INTEGER,
                font_size INTEGER,
                original_font_size INTEGER,
                font_family TEXT,
                style TEXT,
                alignment TEXT,
                text_color TEXT, 
                canvas_id INTEGER
            )
        """)

        # Create lines table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS lines (
                line_id TEXT PRIMARY KEY,
                coords TEXT,
                width INTEGER,
                initial_coords TEXT,
                fill TEXT,
                dash_gap TEXT,
                dash_length TEXT, 
                lcanvas_id INTEGER
            )
        """)

        self.conn.commit()




    def save_to_database(self):
        # Clear existing data
        self.cursor.execute("DELETE FROM shapes")
        self.cursor.execute("DELETE FROM lines")

        # Save shapes
        for shape_id, shape_data in self.shape_ids.items():
            self.cursor.execute("""
                INSERT INTO shapes (shape_id, type, coords, outline, width, initial_coords, color, text, text_id, 
                                    font_size, original_font_size, font_family, style, alignment, text_color, canvas_id)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                shape_id,
                shape_data["type"],
                str(shape_data["coords"]),
                shape_data["outline"],
                shape_data["width"],
                str(shape_data["initial_coords"]),
                shape_data["color"],
                shape_data["text"],
                shape_data["text_id"],
                shape_data["font_size"],
                shape_data["original_font_size"],
                shape_data["font_family"],
                shape_data["style"],
                shape_data["alignment"],
                shape_data["text_color"],
                shape_data[shape_id],
            ))

        # Save lines
        for line_id, line_data in self.line_ids.items():
            self.cursor.execute("""
                INSERT INTO lines (line_id, coords, width, initial_coords, fill, dash_gap, dash_length, lcanvas_id)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                str(line_id),
                str(line_data["coords"]),
                line_data["width"],
                str(line_data["initial_coords"]),
                line_data["fill"],
                line_data["dash_gap"],
                line_data["dash_length"],
                line_data[line_id]
            ))

        self.conn.commit()





    def open_file(self, db_path):
        self.initialize_database(db_path)

        # Clear current canvas
        self.canvas.delete("all")
        self.shape_ids.clear()
        self.line_ids.clear()

        # Load shapes
        self.cursor.execute("SELECT * FROM shapes")
        for row in self.cursor.fetchall():
            shape_data = {
                "type": row[1],
                "coords": eval(row[2]),
                "outline": row[3],
                "width": row[4],
                "initial_coords": eval(row[5]),
                "color": row[6],
                "text": row[7],
                "text_id": row[8],
                "font_size": row[9],
                "original_font_size": row[10],
                "font_family": row[11],
                "style": row[12],
                "alignment": row[13],
                "text_color": row[14],
                'canvas_id': row[15]
            }
            shape_id = row[0]
            self.shape_ids[shape_id] = shape_data

        

        # Load lines
        self.cursor.execute("SELECT * FROM lines")
        for row in self.cursor.fetchall():
            line_data = {
                "coords": eval(row[1]),
                "width": row[2],
                "initial_coords": eval(row[3]),
                "fill": row[4],
                "dash_gap": row[5],
                "dash_length": row[6],
                'lcanvas_id': row[7]
            }
            line_id = eval(row[0])
            self.line_ids[line_id] = line_data

        # Recreate everything back on the canvas
        self.draw_shapes()


    def open_file_command(self):
        # Open a file dialog to select a database file
        file_path = filedialog.askopenfilename(
            title="Open File",
            filetypes=[("Database Files", "*.db"), ("All Files", "*.*")]
        )
        
        if file_path:  # If a file is selected
            if os.path.exists(file_path):
                self.open_file(file_path)  # Load the selected database
                self.current_file = file_path
                file_menu.entryconfig("Save", state="normal")  # Enable Save button
                file_name = os.path.basename(file_path)
                self.file_label.config(text = f'File: {file_name}')
            else:
                print("File not found!")

    def save_as_command(self):
        # Open a file dialog to specify a file name for saving
        file_path = filedialog.asksaveasfilename(
            title="Save As",
            defaultextension=".db",
            filetypes=[("Database Files", "*.db"), ("All Files", "*.*")]
        )
        
        if file_path:  # If a file name is specified
            file_menu.entryconfig("Save", state="normal")  # Enable Save button
            file_name = os.path.basename(file_path)
            self.file_label.config(text = f'File: {file_name}')
            self.save_as(file_path)  # Save the application state to the selected file


    def file_new(self):
        self.current_file = None
        file_menu.entryconfig("Save", state="disabled")  # Disable Save button
        self.file_label.config(text = f'File: {self.current_file}')

        self.canvas.delete("all")
        self.shape_ids.clear()
        self.line_ids.clear()

    def save_as(self, new_db_path):
        self.initialize_database(new_db_path)
        self.save_to_database()






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
        self.add_connection_button.config(state = 'disabled')
        self.shape_combobox.pack(padx=35, pady=10, anchor = 'sw')
        self.apply_button.pack(padx=(50, 0), pady=10, anchor = 'sw')

        # Disable the "Add Shape" button once the ComboBox is visible
        self.add_shape_button.config(state="disabled")


    def apply_shape(self):
        shape_type = self.shape_combobox.get()
        self.add_shape(shape_type)
        self.shape_combobox.pack_forget()  # Hide the ComboBox after selection
        self.apply_button.pack_forget()   # Hide the Apply button
        self.add_shape_button.config(state="normal")  # Re-enable the Add Shape button
        self.add_connection_button.config(state = 'normal')
    


    def add_connection(self):
        #Check for more than two connections
        if len(self.shape_ids) < 2:
            message = "Add connection needs to have two shapes."
            self.show_error_message(self.m, message)
        else:
            #First lets isolate the canvas 
            self.isolate_canvas()
            self.selected_shape = None
            self.draw_shapes()
            
            self.select_two_flag = True
            





    def show_error_message(self, m, message):
        """
        Pops up an error dialog box with the given message in the center of the root window.
        """

        error_dialog = tk.Toplevel(self.m)
        error_dialog.title("Error")
        error_dialog.geometry("300x150")  # Set a fixed size
        error_dialog.transient(self.m)  # Make it modal
        error_dialog.grab_set()  # Prevent interaction with the main window

        # Add the error message
        tk.Label(error_dialog, text=message, fg="red", font=("Arial", 12)).pack(pady=20)
        tk.Button(error_dialog, text="OK", command=error_dialog.destroy).pack(pady=10)

      






#Click/Motion Event functions 
#--------------------------------------------------------------------------------------------


    def onLeftClick(self, event):
        
        #Check conditions for starting pan    
        if self.selected_shape is None and not self.select_two_flag:
            self.start_pan(event)

        #Save the click coords
        self.set_initial_click(event)

        #For adding connection
        if self.select_two_flag:
            self.two_select(event)


    def onDrag(self, event):
        """Handle drag motion."""
        if self.selected_shape:
            # If a shape is selected, move the shape
            self.move_shape(event)
            
        elif not self.check_inside_all(event) and not self.selected_shape:
            # If no shape is selected, pan the canvas
            self.pan_canvas(event)

    def onRelease(self, event):
        if self.select_two_flag:
            self.two_select(event)
        else:
            #For processing connection and selection
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

        #If click is on line
        elif self.is_cursor_on_line(event) in self.line_ids:
            self.select_shape(event)

            self.line_menu = tk.Menu(self.canvas, tearoff=0)
            self.line_menu.add_command(label="Delete", command=self.delete_selected_line)
            self.line_menu.post(event.x_root, event.y_root)

        else:
            self.selected_shape = None


#Tool Menu Functions 
#--------------------------------------------------------------------------------------------

    def open_resize_dialog(self):
        
        if not self.selected_shape:
            return

        shape_data = self.shape_ids[self.selected_shape]
        x1, y1, x2, y2 = shape_data['coords']
        current_width = x2 - x1
        current_height = y2 - y1
        
        # Open the resize dialog with Comboboxes for width and height selection
        resize_dialog = tk.Toplevel(self.m)
        resize_dialog.title("Resize Shape")
        resize_dialog.geometry("300x200+{}+{}".format(self.m.winfo_x() + 100, self.m.winfo_y() + 100))  # Center the dialog

        # Label for current size
        label = tk.Label(resize_dialog, text=f"Current size: {current_width}x{current_height}")
        label.pack(pady=10)

        # Comboboxes for width and height
        width_label = tk.Label(resize_dialog, text="New Width:")
        width_label.pack()
        width_combobox = ttk.Combobox(resize_dialog, values=[i for i in range(10, 501, 10)])
        width_combobox.set(int(current_width))  # Set current width
        width_combobox.pack(pady=5)

        height_label = tk.Label(resize_dialog, text="New Height:")
        height_label.pack()
        height_combobox = ttk.Combobox(resize_dialog, values=[i for i in range(10, 501, 10)])
        height_combobox.set(int(current_height))  # Set current height
        height_combobox.pack(pady=5)

        # Submit button to resize the shape
        submit_button = tk.Button(resize_dialog, text="Resize", command=lambda: self.apply_resize(resize_dialog, width_combobox, height_combobox))
        submit_button.pack(pady=20)

    def apply_resize(self, resize_dialog, width_combobox, height_combobox):

        try:
            new_width = int(width_combobox.get())
            new_height = int(height_combobox.get())

            if new_width <= 0 or new_height <= 0:
                raise ValueError("Width and height must be positive integers.")

            # Apply the new width and height
            x1, y1, x2, y2 = self.shape_ids[self.selected_shape]['coords']
            cx = (x1 + x2) / 2  # Center x
            cy = (y1 + y2) / 2  # Center y
            half_width = new_width / 2
            half_height = new_height / 2

            new_x1 = cx - half_width
            new_y1 = cy - half_height
            new_x2 = cx + half_width
            new_y2 = cy + half_height

            # Update shape data
            self.shape_ids[self.selected_shape]['coords'] = (new_x1, new_y1, new_x2, new_y2)

            # Redraw all shapes
            self.draw_shapes()

            # Close the resize dialog
            resize_dialog.destroy()

        except ValueError as e:
            messagebox.showerror("Invalid Input", f"Error: {e}")
            return
        

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
            self.shape_ids[self.selected_shape]['color'] = get_color[1]
            self.draw_shapes()


    def delete_selected_line(self):
        if self.selected_line:
            real_id = self.line_ids[self.selected_line][self.selected_line]
            del self.line_ids[self.selected_line]
            self.canvas.delete(real_id)
            self.selected_line = None
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
                scaled_font_size = max(1, round(int(original_font_size) * self.scale))
                self.shape_ids[shape_id]['font_size'] = scaled_font_size
            self.scale = 1.0
        

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

        if self.scale <= 20 and self.scale >= 0.10:

            self.scale *= zoom_factor
        else:
            # Clamp the scale to valid bounds
            if self.scale > 20:
                self.scale = 20
            elif self.scale < 0.10:
                self.scale = 0.10

            # Adjust the zoom factor to align with the corrected scale
            correction_factor = self.scale / (self.scale * zoom_factor)
            self.offset_x += (event.x - self.offset_x) * (1 - correction_factor)
            self.offset_y += (event.y - self.offset_y) * (1 - correction_factor)
                

        print(self.scale)
        self.draw_shapes()
        

        # Restart scroll timer
        #if self.scroll_timer is not None:
        #     self.m.after_cancel(self.scroll_timer)
        #self.scroll_timer = self.m.after(100, self.update_shape_references)



    def update_shape_references(self):
        for shape_id, shape_data in self.shape_ids.items():
            self.shape_ids[shape_id]["coords"] = self.shape_ids[shape_id]["adj_coords"]
            original_font_size = shape_data['font_size']
            scaled_font_size = max(1, round(int(original_font_size) * self.scale))
            self.shape_ids[shape_id]['font_size'] = scaled_font_size
        self.scale = 1.0

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
        self.selected_line = None
        for shape_id, shape_data in self.shape_ids.items():

            shape_data["coords"] = shape_data['initial_coords']
            shape_data['font_size'] = shape_data['original_font_size']


        

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
            'original_font_size': 12,
            "font_family": "Arial",
            'style': 'None',
            'alignment': 'center',
            'text_color': 'black',
        }


        

        #When adding new shape, draw it on the screen
        self.draw_shapes() #Pass in specific id associated with the shape


    #For all shapes 
    def draw_shapes(self):
        self.canvas.delete("all")

        #First update adjusted coords
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

            



        #Once coords are updated for each shape, then draw in the associated lines with correct adjusted coords----------------------------- 
        for line_id, line_data in self.line_ids.items():
            shape_id1 = line_id[0]
            shape_id2 = line_id[1]
            x11, y11, x12, y12= self.shape_ids[shape_id1]['adj_coords']
            x21, y21, x22, y22 = self.shape_ids[shape_id2]['adj_coords']
            cx1 = (x11 + x12) / 2
            cy1 = (y11 + y12) / 2
            cx2 = (x21 + x22) / 2
            cy2 = (y21 + y22) / 2

            
            if line_data['dash_gap'] == 'None' or line_data['dash_length'] == 'None':
                dash_params = None
            else:
                dash_params = (int(line_data['dash_length']), int(line_data['dash_gap']))
            
            new_id = self.canvas.create_line(cx1, cy1, cx2, cy2, fill=line_data['fill'], width=line_data['width'], dash = dash_params)
            
            #Store the new coords associated with the shapes and the new canvas id for the shape
            self.line_ids[line_id]['coords'] = (cx1, cy1, cx2, cy2)
            self.line_ids[line_id][line_id] = new_id



        for shape_id, shape_data in self.shape_ids.items():
            shape_data = self.shape_ids[shape_id]
            shape_type = shape_data['type']
            original_font_size = shape_data["font_size"]
            
            adj_x1, adj_y1, adj_x2, adj_y2 = shape_data['adj_coords']

            # draw the shapes with updated coordinates-----------------------------
            if shape_type == "Circle":
                canvas_id = self.canvas.create_oval(adj_x1, adj_y1, adj_x2, adj_y2, fill=shape_data['color'], outline=shape_data['outline'], width =shape_data['width'])
            elif shape_type == "Square":
                canvas_id = self.canvas.create_rectangle(adj_x1, adj_y1, adj_x2, adj_y2, fill=shape_data['color'], outline=shape_data['outline'], width =shape_data['width'])
            elif shape_type == "Triangle":
                points = [adj_x1, adj_y2, (adj_x1 + adj_x2) / 2, adj_y1, adj_x2, adj_y2]
                canvas_id = self.canvas.create_polygon(points, fill=shape_data['color'], outline=shape_data['outline'], width =shape_data['width'], tags=("shape", shape_id))
            # Update the canvas id as the shape_id
            self.shape_ids[shape_id][shape_id] = canvas_id


            scaled_font_size = max(1, round(int(original_font_size) * self.scale))
            font_family = shape_data['font_family']
            style = shape_data['style']
            text_color = shape_data['text_color']
            alignment = shape_data['alignment']


            if style == 'None':
                style = ''

            alignment_map = {'left': 'e', 'right': 'w', 'center': 'center'}


            # Draw associated text-----------------------------
            cx = (adj_x1 + adj_x2) / 2
            cy = (adj_y1 + adj_y2) / 2
            text = shape_data['text']
            text_id = self.canvas.create_text(cx, cy, text=text, font=(font_family, scaled_font_size, style), fill=text_color, width = adj_x2-adj_x1, anchor = alignment_map[alignment])
            self.shape_ids[shape_id]['text_id'] = text_id

        





    #For selected shapes only
    def destroy_and_redraw(self):


        #For a selected shape
        if self.selected_shape:
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


            #Once coords are updated for each shape, then draw in the associated lines with correct adjusted coords-----------------------------
            for line_id, line_data in self.line_ids.items():
                
                #Check for correct line of selected shape
                if self.selected_shape in line_id:
                    shape_id1 = line_id[0]
                    shape_id2 = line_id[1]
                    #If the first shape was moved, update first line pair
                    x1, y1, x2, y2 = self.shape_ids[self.selected_shape]['adj_coords']
                    
                    cx1 = (x1 + x2) / 2
                    cy1 = (y1 + y2) / 2
                    
                    reg_x1, reg_y1, reg_x2, reg_y2 = self.line_ids[line_id]['coords']

                    #First delete the previous line
                    item_id = self.line_ids[line_id][line_id]
                    self.canvas.delete(item_id)

                    

                    #If selected shape correspond to first line pair, update the line with new adjusted coords
                    if self.selected_shape == shape_id1:
                        
                        #Draw new line with updated first pair
                        if line_data['dash_gap'] == 'None' or line_data['dash_length'] == 'None':
                            dash_params = None
                        else:
                            dash_params = (int(line_data['dash_length']), int(line_data['dash_gap']))
                        
                        new_id = self.canvas.create_line(cx1, cy1, reg_x2, reg_y2, fill=line_data['fill'], width=line_data['width'], dash = dash_params)
                        #Store the new coords associated with the shapes and the new canvas id for the shape
                        self.line_ids[line_id]['coords'] = (cx1, cy1, reg_x2, reg_y2)
                        self.line_ids[line_id][line_id] = new_id


                        #Redraw the other shape to be ontop of line as well
                        self.redraw_a_shape(shape_id2)


                    #If selected shape correspond to second line pair, update the line with new adjusted coords
                    else:
                        
                        #Draw new line with updated second pair
                        if line_data['dash_gap'] == 'None' or line_data['dash_length'] == 'None':
                            dash_params = None
                        else:
                            dash_params = (int(line_data['dash_length']), int(line_data['dash_gap']))
                        
                        new_id = self.canvas.create_line(reg_x1, reg_y1, cx1, cy1, fill=line_data['fill'], width=line_data['width'], dash = dash_params)
                        #Store the new coords associated with the shapes and the new canvas id for the shape
                        self.line_ids[line_id]['coords'] = (reg_x1, reg_y1, cx1, cy1)
                        self.line_ids[line_id][line_id] = new_id



                        #Redraw the other shape to be ontop of line as well
                        self.redraw_a_shape(shape_id1)


            




            # draw the shapes with updated coordinates-----------------------------
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







            # Draw associated text with all correct parameters in middle of shape-----------------------------
            scaled_font_size = max(1, round(int(original_font_size) * self.scale))
            font_family = shape_data['font_family']
            style = shape_data['style']
            text_color = shape_data['text_color']
            alignment = shape_data['alignment']

            if style == 'None':
                style = ''

            alignment_map = {'left': 'e', 'right': 'w', 'center': 'center'}


            cx = (adj_x1 + adj_x2) / 2
            cy = (adj_y1 + adj_y2) / 2
            text = shape_data['text']
            text_id = self.canvas.create_text(cx, cy, text=text, font=(font_family, scaled_font_size, style), fill=text_color, width = adj_x2-adj_x1, anchor = alignment_map[alignment])
            self.shape_ids[self.selected_shape]['text_id'] = text_id




                        



        #For selecting two shapes and redrawing both---------------------------------------------------------------------------------------
        if self.current_select_two:
            print(self.current_select_two)
            for shape_id in self.current_select_two:
                item_id = self.shape_ids[shape_id][shape_id]
                self.canvas.delete(item_id)
                shape_data = self.shape_ids[shape_id]
                shape_type = shape_data['type']
                original_font_size = shape_data["font_size"]
                x1, y1, x2, y2 = shape_data["coords"]


                adj_x1 = (x1 * self.scale) + self.offset_x + self.dx
                adj_y1 = (y1 * self.scale) + self.offset_y + self.dy
                adj_x2 = (x2 * self.scale) + self.offset_x + self.dx
                adj_y2 = (y2 * self.scale) + self.offset_y + self.dy

                shape_data['adj_coords'] = (adj_x1, adj_y1, adj_x2, adj_y2)
                

                # draw the shapes with updated coordinates-----------------------------
                if shape_type == "Circle":
                    new_id = self.canvas.create_oval(adj_x1, adj_y1, adj_x2, adj_y2, fill=shape_data['color'], outline=shape_data['outline'], width =shape_data['width'])
                elif shape_type == "Square":
                    new_id = self.canvas.create_rectangle(adj_x1, adj_y1, adj_x2, adj_y2, fill=shape_data['color'], outline=shape_data['outline'], width =shape_data['width'])
                elif shape_type == "Triangle":
                    points = [adj_x1, adj_y2, (adj_x1 + adj_x2) / 2, adj_y1, adj_x2, adj_y2]
                    new_id = self.canvas.create_polygon(points, fill=shape_data['color'], outline=shape_data['outline'], width =shape_data['width'])
                # Update the canvas id as the shape_id
                
                self.shape_ids[shape_id][shape_id] = new_id

                self.canvas.itemconfig(new_id, outline="green", width=2)

                # Draw associated text with all correct parameters in middle of shape-----------------------------
                scaled_font_size = max(1, round(int(original_font_size) * self.scale))
                font_family = shape_data['font_family']
                style = shape_data['style']
                text_color = shape_data['text_color']
                alignment = shape_data['alignment']

                if style == 'None':
                    style = ''

                alignment_map = {'left': 'e', 'right': 'w', 'center': 'center'}



                cx = (adj_x1 + adj_x2) / 2
                cy = (adj_y1 + adj_y2) / 2
                text = shape_data['text']
                text_id = self.canvas.create_text(cx, cy, text=text, font=(font_family, scaled_font_size, style), fill=text_color, width = adj_x2-adj_x1, anchor = alignment_map[alignment])
                self.shape_ids[shape_id]['text_id'] = text_id




        #For selecting line and redrawing its border---------------------------------------------------------------------------------------
        if self.selected_line:

            real_id= self.line_ids[self.selected_line][self.selected_line]
            self.canvas.itemconfig(real_id, fill = 'lightblue')






    def redraw_a_shape(self, shape_id):
        shape_data = self.shape_ids[shape_id]
        real_id = shape_data[shape_id]
        shape_type = shape_data['type']
        original_font_size = shape_data["font_size"]
        adj_x1, adj_y1, adj_x2, adj_y2 = shape_data['adj_coords']


        self.canvas.delete(real_id)

        # draw the shapes with updated coordinates-----------------------------
        if shape_type == "Circle":
            new_id = self.canvas.create_oval(adj_x1, adj_y1, adj_x2, adj_y2, fill=shape_data['color'], outline=shape_data['outline'], width =shape_data['width'])
        elif shape_type == "Square":
            new_id = self.canvas.create_rectangle(adj_x1, adj_y1, adj_x2, adj_y2, fill=shape_data['color'], outline=shape_data['outline'], width =shape_data['width'])
        elif shape_type == "Triangle":
            points = [adj_x1, adj_y2, (adj_x1 + adj_x2) / 2, adj_y1, adj_x2, adj_y2]
            new_id = self.canvas.create_polygon(points, fill=shape_data['color'], outline=shape_data['outline'], width =shape_data['width'])
        
        # Update the canvas id as the new_id of the drawn shape
        self.shape_ids[shape_id][shape_id] = new_id


        # Draw associated text with all correct parameters in middle of shape-----------------------------
        scaled_font_size = max(1, round(int(original_font_size) * self.scale))
        font_family = shape_data['font_family']
        style = shape_data['style']
        text_color = shape_data['text_color']
        alignment = shape_data['alignment']
        if style == 'None':
            style = ''
        alignment_map = {'left': 'e', 'right': 'w', 'center': 'center'}
        cx = (adj_x1 + adj_x2) / 2
        cy = (adj_y1 + adj_y2) / 2
        text = shape_data['text']
        text_id = self.canvas.create_text(cx, cy, text=text, font=(font_family, scaled_font_size, style), fill=text_color, width = adj_x2-adj_x1, anchor = alignment_map[alignment])
        self.shape_ids[shape_id]['text_id'] = text_id







    def select_shape(self, event):
        #For handing already previously selected line
        prev_line = self.selected_line
        if prev_line != None:
            real_id = self.line_ids[prev_line][prev_line]
            line_fill = self.line_ids[self.selected_line]['fill']
            self.canvas.itemconfig(real_id, fill = line_fill)



        #Check for line selection and update fields
        line_id = self.is_cursor_on_line(event, 10)
        if self.is_cursor_on_line(event, 10) != None:
            #If true then change self.selected_line and update canvas
            self.selected_line = line_id
            self.selected_shape = None
            self.destroy_and_redraw()

            #Update line field values
            line_fill = self.line_ids[self.selected_line]['fill']
            line_width = self.line_ids[self.selected_line]['width']
            line_dash_gap = self.line_ids[self.selected_line]['dash_gap']
            line_dash_length = self.line_ids[self.selected_line]['dash_length']
            self.lcolor_display_canvas.config(bg = line_fill)
            self.line_width_combo.set(line_width)
            self.dash_gap_combo.set(line_dash_gap)
            self.dash_length_combo.set(line_dash_length)
            self.apply_line_button.config(state = 'normal')

        #If cursor not in line, reset to default
        else:
            
            self.lcolor_display_canvas.config(bg = 'black')
            self.line_width_combo.set(2)
            self.dash_gap_combo.set('None')
            self.dash_length_combo.set('None')
            self.apply_line_button.config(state = 'disabled')
            
            self.selected_line = None



        #For handling previously selected shape
        prev_selected = self.selected_shape
        if prev_selected != None:
            canvas_id = self.shape_ids[prev_selected][prev_selected]
            self.canvas.itemconfig(canvas_id, outline= "black", width = 2)


        #Loop through all shapes and check if valid selection
        
        for shape_id, shape_data in self.shape_ids.items():  
            real_id = shape_data[shape_id]
            if self.check_if_inside(event, real_id):    
                

                # Highlight the new selected shape and update with its data
                self.selected_shape = shape_id
                self.selected_line = None
                text_id = self.shape_ids[self.selected_shape]['text_id']
                existing_text = self.canvas.itemcget(text_id, "text")        
                self.text_entry.delete("1.0", tk.END)
                self.text_entry.insert('1.0', existing_text)
                font_family = self.shape_ids[self.selected_shape]['font_family']
                font_size  = self.shape_ids[self.selected_shape]['font_size']
                color = self.shape_ids[self.selected_shape]['text_color']
                alignment = self.shape_ids[self.selected_shape]['alignment']
                style = self.shape_ids[self.selected_shape]['style']
                self.font_size_cb.set(font_size)
                self.font_combobox.set(font_family)
                self.alignment_cb.set(alignment)
                self.choose_style_cb.set(style)
                self.color_display_canvas.config(bg=color)
                self.apply_text_button.config(state = 'normal')

                

                #Update the coords of the shape after its release
                shape_data = self.shape_ids[self.selected_shape]
                x1, y1, x2, y2 = shape_data["coords"]
                if self.offset_x != 0 or self.offset_y != 0:   
                    #If zoom took place meaning self.scale was changed, then store the transformed cords of the selected shape
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
            self.font_size_cb.set('12')
            self.font_combobox.set('Arial')
            self.alignment_cb.set('center')
            self.choose_style_cb.set('None')
            self.color_display_canvas.config(bg='black')
            self.apply_text_button.config(state = 'disabled')


        
            

           
        

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

            #Get the input data
            input_text = self.text_entry.get("1.0", tk.END).strip() 
            color = self.chosen_color.get() # Returns (RGB, hex)
            font_size =  self.font_size_cb.get()
            font_family = self.font_combobox.get()
            style = self.choose_style_cb.get()
            alignment = self.alignment_cb.get()

            #Update the selected shape dictionary data
            self.shape_ids[self.selected_shape]['style'] = style
            self.shape_ids[self.selected_shape]['font_family'] = font_family
            self.shape_ids[self.selected_shape]['font_size'] = font_size
            self.shape_ids[self.selected_shape]['text'] = input_text
            self.shape_ids[self.selected_shape]['text_color'] = color
            self.shape_ids[self.selected_shape]['alignment'] = alignment

            #Redraw the shape with updated data
            self.destroy_and_redraw()


    def choose_color(self):


        # Open the color chooser dialog
        color = colorchooser.askcolor(title="Choose Text Color")[1]  # Returns (RGB, hex)
        if color:  # Check if a color was chosen
            self.chosen_color.set(color)  # Update the stored color
            # Update the canvas to show the selected color
            self.color_display_canvas.config(bg=color)




            
#Line Manager Functions
#--------------------------------------------------------------------------------------------

    def two_select(self, event):
        

        #Check conditions for selecting shapes
        if len(self.current_select_two) < 2:
            #Now check which shape and add blue shape selection 
            for shape_id, shape_data in self.shape_ids.items():
                if shape_id in self.current_select_two:
                    continue
                real_id = shape_data[shape_id] #Returns the real canvas id 
                x1, y1, x2, y2 = shape_data['coords']
                if self.check_if_inside(event, real_id):
                    #If it is selected shape
                    
                    
                    #Store reference to shape id
                    self.current_select_two.append(shape_id)
                    print(self.current_select_two)


                    #Also make the shape border change
                    self.destroy_and_redraw()

        else:
            #If we have 2 shapes selected, draw line 
            self.add_line()


    def add_line(self):


        #Define point coords for line
        shape_id1 = self.current_select_two[0]
        shape_id2 = self.current_select_two[1]
        x11, y11, x12, y12= self.shape_ids[shape_id1]['coords']
        x21, y21, x22, y22 = self.shape_ids[shape_id2]['coords']

        cx1 = (x11 + x12) / 2
        cy1 = (y11 + y12) / 2

        cx2 = (x21 + x22) / 2
        cy2 = (y21 + y22) / 2
        



        line_id = (shape_id1, shape_id2)

        #Intiialize Line Data
        self.line_ids[line_id] = {
            "coords": (cx1, cy1, cx2, cy2),
            "width": 2,
            "initial_coords":(cx1, cy1, cx2, cy2),
            "fill": 'black', 
            'dash_gap': 'None',
            'dash_length': 'None',

        }

        

        #Reset selection data 
        self.current_select_two = []
        self.select_two_flag = False

        #Redraw once for updating selection borders
        self.destroy_and_redraw()

        self.draw_shapes()

        self.revert_canvas()





    def choose_line_color(self):

        # Open the color chooser dialog
        color = colorchooser.askcolor(title="Choose Line Color")[1]  # Returns (RGB, hex)
        if color:  # Check if a color was chosen
            self.chosen_line_color.set(color)  # Update the stored color
            # Update the canvas to show the selected color
            self.lcolor_display_canvas.config(bg=color)



    def apply_to_line(self):
        if self.selected_line:
            print('apply to line')
            #Apply to the line by updating data dicionary
            line_fill = self.chosen_line_color.get()
            line_width = self.line_width_combo.get()
            line_dash_gap = self.dash_gap_combo.get()
            line_dash_length = self.dash_length_combo.get()

            self.line_ids[self.selected_line]['fill'] = line_fill
            self.line_ids[self.selected_line]['width'] = line_width
            self.line_ids[self.selected_line]['dash_gap'] = line_dash_gap
            self.line_ids[self.selected_line]['dash_length'] = line_dash_length

            
            self.draw_shapes()

            





















#Helper Functions
#--------------------------------------------------------------------------------------------

    def is_cursor_on_line(self, event, threshold=5):
        #Check if cursor in the bounding box of line
        if self.check_inside_all(event):
            return None

        for line_id, line_data in self.line_ids.items():
            # Get line coordinates
            
            x1, y1, x2, y2 = line_data['coords']
            
            # Calculate bounding box with margin
            bbox_x1 = min(x1, x2) - threshold
            bbox_y1 = min(y1, y2) - threshold
            bbox_x2 = max(x1, x2) + threshold
            bbox_y2 = max(y1, y2) + threshold
            

            # Check if the cursor is inside the bounding box
            if not bbox_x1 <= event.x <= bbox_x2 and bbox_y1 <= event.y <= bbox_y2:
                continue

            # Precise check: Point-to-line distance
            px, py = event.x, event.y
            dx, dy = x2 - x1, y2 - y1
            line_length_squared = dx**2 + dy**2

            # Handle case where the line is a point
            if line_length_squared == 0:
                distance = math.hypot(px - x1, py - y1)
                return distance <= threshold

            # Project point onto line segment and find closest point
            t = max(0, min(1, ((px - x1) * dx + (py - y1) * dy) / line_length_squared))
            closest_x = x1 + t * dx
            closest_y = y1 + t * dy

            # Check if the point is within the threshold distance
            distance = math.hypot(px - closest_x, py - closest_y)
            if distance <= threshold:
                return line_id

        return None



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



    def isolate_canvas(self):
        self.add_shape_button.config(state = 'disabled')
        self.add_connection_button.config(state = 'disabled')
        self.font_combobox.config(state = 'disabled')
        self.font_size_cb.config(state = 'disabled')
        self.alignment_cb.config(state = 'disabled')
        self.choose_style_cb.config(state = 'disabled')
        self.color_button.config(state = 'disabled')
        self.canvas.config(bg = 'lightgray')
        self.btc_button.config(state = 'disabled', highlightbackground = 'lightgray')
        self.zoom_in_button.config(highlightbackground = 'lightgray', state = 'disabled')
        self.zoom_out_button.config(highlightbackground = 'lightgray', state = 'disabled')

    def revert_canvas(self):
        self.add_shape_button.config(state = 'normal')
        self.add_connection_button.config(state = 'normal')
        self.font_combobox.config(state = 'normal')
        self.font_size_cb.config(state = 'normal')
        self.alignment_cb.config(state = 'normal')
        self.choose_style_cb.config(state = 'normal')
        self.color_button.config(state = 'normal')
        self.canvas.config(bg = 'white')
        self.btc_button.config(state = 'normal', highlightbackground = 'white')
        self.zoom_in_button.config(highlightbackground = 'white', state = 'normal')
        self.zoom_out_button.config(highlightbackground = 'white', state = 'normal')
        










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
                    menu_obj.add_command(label = item[0], command = item[1], state = item[2])
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


#Define class objects
sc = ShapeCanvas(m)
mbs = MenuButtons(m, main_menu)



#Menus inside main menu
file_menu = mbs.create_menu("File", 
    [
    ('New', lambda: sc.file_new(), 'normal'),
    ('Open', lambda: sc.open_file_command(), 'normal'),
    ('Save', lambda: sc.save_to_database(), 'disabled'),
    ('Save as', lambda: sc.save_as_command(), 'normal'),
    ("Save Canvas as Image", mbs.placeholder, 'normal'),
    ("Export", mbs.placeholder, 'normal'),
    ("Clear Canvas", mbs.placeholder, 'normal'),
    ("Undo", mbs.placeholder, 'normal'),
    ("Canvas Settings", mbs.placeholder, 'normal'),
    ("Exit", mbs.end, 'normal') #Passes function reference instead of calling the funciton

    ])

edit_menu = mbs.create_menu('Edit',
    tabs = [
        ("Undo", mbs.placeholder, 'normal'),
        ("Redo", mbs.placeholder, 'normal'),
        ("separator", None, 'normal'),
        ("Cut", mbs.placeholder, 'normal'),
        ("Copy", mbs.placeholder, 'normal'),
        ("Paste", mbs.placeholder, 'normal'),
        ("separator", None, 'normal'),
        ("Delete", mbs.placeholder, 'normal'),
        ("Clear Canvas", mbs.placeholder, 'normal'),
        ("separator", None, 'normal'),
        ("Resize/Scale", mbs.placeholder, 'normal'),
        ("Rotate", mbs.placeholder, 'normal'),
        ("Change Properties", mbs.placeholder, 'normal'),
        ("Zooming", mbs.placeholder, 'normal'),
    ])


add_menu = mbs.create_menu("Add")
shape_submenu = mbs.create_submenu(add_menu, "Add Shape",
    [
        ("Circle", lambda: sc.add_shape("Circle"), 'normal'),
        ("Square", lambda: sc.add_shape("Square"), 'normal'),
        ("Triangle", lambda: sc.add_shape("Triangle"), 'normal')
    ]
)










#Runs the main loop for the application
if __name__ == "__main__": 
    m.mainloop()



