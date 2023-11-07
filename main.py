import math
import time
import cv2
import numpy as np
import pyrealsense2 as rs
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os
import sys

class AppState:

    def __init__(self, *args, **kwargs):
        self.pipeline = rs.pipeline()
        config = rs.config()

        config.enable_stream(rs.stream.depth, rs.format.z16, 30)
        config.enable_stream(rs.stream.color, rs.format.bgr8, 30)

        # Start streaming
        self.pipeline.start(config)

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
    # Wait for a coherent pair of frames: depth and color
    frames = state.pipeline.wait_for_frames()
    depth_frame = frames.get_depth_frame()
    color_frame = frames.get_color_frame()

    # Convert images to numpy arrays
    depth_image = np.asanyarray(depth_frame.get_data())
    color_image = np.asanyarray(color_frame.get_data())

    # resize the color image to match depth image for display but keep aspect ratio
    scale = depth_frame.get_width() / color_frame.get_width()
    dim = (depth_frame.get_width(), int(color_frame.get_height() * scale))
    color_image = cv2.resize(color_image, dim, interpolation = cv2.INTER_AREA)

    # Apply colormap on depth image (image must be converted to 8-bit per pixel first)
    depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.07), cv2.COLORMAP_MAGMA)

    # Convert the NumPy arrays to images suitable for displaying in Tkinter
    color_pil_image = Image.fromarray(cv2.cvtColor(color_image, cv2.COLOR_BGR2RGB))
    depth_pil_image = Image.fromarray(depth_colormap)
    
    color_tk_image = ImageTk.PhotoImage(image=color_pil_image)
    depth_tk_image = ImageTk.PhotoImage(image=depth_pil_image)

    # Update the canvas widgets with the new images
    color_canvas.create_image(0, 0, anchor=tk.NW, image=color_tk_image)
    depth_canvas.create_image(0, 0, anchor=tk.NW, image=depth_tk_image)
    
    # Keep references to prevent garbage collection
    color_canvas.image = color_tk_image
    depth_canvas.image = depth_tk_image

# Create canvas widgets for color and depth images
color_canvas = tk.Canvas(root, width=640, height=480)
color_canvas.pack(side="left")
depth_canvas = tk.Canvas(root, width=640, height=480)
depth_canvas.pack(side="right")

pk_canvas = tk.Canvas(root, width=1280, height=480)
pk_canvas.pack(side="bottom")

# Create a "Start/Stop" button
toggle_button = ttk.Button(button_frame, text="Start/Stop", command=update_canvas)
toggle_button.pack(side="left")

# Create a "Save PNG" button
def save_png():
    # Replace 'canvas.image' with the image you want to save
    pass

save_button = ttk.Button(button_frame, text="Save PNG", command=save_png)
save_button.pack(side="left")

def save_ply():

    print("save_ply")

save_button = ttk.Button(button_frame, text="Export Ply", command=save_ply)
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
