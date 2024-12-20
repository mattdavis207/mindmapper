# Mindmapper Study Tool

Mindmapper is an intuitive Python application designed to aid brainstorming, studying, and knowledge mapping. By creating dynamic tree diagrams, this tool enables users to connect and organize ideas visually, making it ideal for conceptualizing and exploring complex topics.

## Features

- **Interactive Canvas**: A resizable canvas allows users to add, move, and connect shapes (circle, square, triangle).
- **Dynamic Tree Diagrams**: Build structures that map ideas or concepts in a tree-like format.
- **Panning and Zooming**: Navigate and adjust the view to focus on specific parts of the diagram.
- **Shape Customization**:
  - Add custom text to shapes.
  - Modify fonts, sizes, colors, and alignment.
  - Resize or delete shapes as needed.
- **Line Connections**:
  - Connect shapes with customizable lines.
  - Adjust line width, color, and dash patterns.
- **File Management**:
  - Save and load diagrams using SQLite for persistent storage.
  - Start new diagrams or modify existing ones.

## How to Use

1. **Add Shapes**: Select a shape (Circle, Square, or Triangle) and place it on the canvas.
2. **Customize Shapes**: Add text, choose fonts and styles, or change colors.
3. **Connect Shapes**: Select two shapes and create lines to represent connections.
4. **Navigate the Canvas**:
   - Use panning to move around the canvas.
   - Zoom in or out for a closer or broader view.
5. **Save Your Work**: Save diagrams to a `.db` file for future editing or load an existing file.

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/mindmapper.git

2. Navigate to the project directory:
   ```bash
   cd mindmapper
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
4. Run the application:
    ```bash
   python mm_main.py

# Dependencies
- Python 3.x
- Tkinter: GUI library included in Python.
- Pillow: For image processing.
- SQLite: Embedded database for saving and loading diagrams.

Install Dependencies Using:

```bash
pip install Pillow
