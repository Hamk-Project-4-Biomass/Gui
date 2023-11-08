import tkinter as tk
from tkinter import ttk
from PIL import ImageTk
from datetime import datetime
from functions import *
from pyrealsense import *
import os
import subprocess

class AppState:

    def __init__(self, *args, **kwargs):
        self.realsense = RealSense() # Create a RealSense object
# Create a Tkinter window
root = tk.Tk()
root.title("RealSense Viewer")

# Create an instance of the AppState class
state = AppState()

# Create a frame for buttons
button_frame = tk.Frame(root)
button_frame.pack(fill="x")

# Create a function to update the canvas
def update_canvas():
    try:
        color_tk_image = ImageTk.PhotoImage(image=state.realsense.get_color_pill_image())
        depth_tk_image = ImageTk.PhotoImage(image=state.realsense.get_depth_pill_image())

        # Update the canvas widgets with the new images
        color_canvas.create_image(0, 0, anchor=tk.NW, image=color_tk_image)
        depth_canvas.create_image(0, 0, anchor=tk.NW, image=depth_tk_image)
        
        # Keep references to prevent garbage collection
        color_canvas.image = color_tk_image
        depth_canvas.image = depth_tk_image
    except:
        print("No device detected")
        pass

# Create canvas widgets for color and depth images
color_canvas = tk.Canvas(root, width=640, height=480)
color_canvas.pack(side="left")
depth_canvas = tk.Canvas(root, width=640, height=480)
depth_canvas.pack(side="right")

# Create a "Save PNG" button
def save_png():
    # Save the color and depth images to the current directory
    color_image = state.realsense.get_color_pill_image()
    depth_image = state.realsense.get_depth_pill_image()

    fulldatestring = datetime.now().strftime("%Y-%m-%d.%H.%M.%S")

    script_dir = os.path.dirname(__file__)

    export.png(color_image,depth_image,fulldatestring, script_dir)

save_button = ttk.Button(button_frame, text="Save PNG", command=save_png)
save_button.pack(side="left")

def save_ply():
    color_frame = state.realsense.get_color_frame()
    depth_frame = state.realsense.get_depth_frame()

    fulldatestring = datetime.now().strftime("%Y-%m-%d.%H.%M.%S")

    script_dir = os.path.dirname(__file__)

    export.ply(color_frame,depth_frame,fulldatestring + ".ply", script_dir)


save_button = ttk.Button(button_frame, text="Export Ply", command=save_ply)
save_button.pack(side="left")

def viewer():
    state.realsense.pipe_stop()
    procces = subprocess.Popen(["python", "opencv_pointcloud_viewer.py"])
    procces.wait()
    state.realsense.pipe_start()

save_button = ttk.Button(button_frame, text="Pointcloud viewer", command=viewer)
save_button.pack(side="left")


# Create a "Quit" button
quit_button = ttk.Button(button_frame, text="Quit", command=root.destroy)
quit_button.pack(side="left")

# Add an update loop to periodically update the canvas
def update():
    update_canvas()
    root.after(10, update)  # Adjust the update interval as needed

update()  # Start the update loop

# Start the Tkinter main loop
root.mainloop()
