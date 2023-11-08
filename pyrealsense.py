import pyrealsense2 as rs
import numpy as np
import cv2
from PIL import Image

class RealSense:

    def __init__(self):
        try:
            self.pipe = rs.pipeline()

            self.rs_config = rs.config()

            self.rs_config.enable_stream(rs.stream.depth, rs.format.z16, 30)
            self.rs_config.enable_stream(rs.stream.color, rs.format.bgr8, 30)



            self.pipe.start(self.rs_config)

            self.update()
        except:
            print("No device detected")
        

    

    def update(self):
        self.frames = self.pipe.wait_for_frames()
        self.depth_frame = self.frames.get_depth_frame()
        self.color_frame = self.frames.get_color_frame()

        # Convert images to numpy arrays
        self.depth_image = np.asanyarray(self.depth_frame.get_data())
        self.color_image = np.asanyarray(self.color_frame.get_data())

        # resize the color image to match depth image for display but keep aspect ratio
        scale = self.depth_frame.get_width() / self.color_frame.get_width()
        dim = (self.depth_frame.get_width(), int(self.color_frame.get_height() * scale))
        self.color_image = cv2.resize(self.color_image, dim, interpolation = cv2.INTER_AREA)

        # Apply colormap on depth image (image must be converted to 8-bit per pixel first)
        depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(self.depth_image, alpha=0.07), cv2.COLORMAP_MAGMA)

        # Convert the NumPy arrays to images suitable for displaying in Tkinter
        self.color_pil_image = Image.fromarray(cv2.cvtColor(self.color_image, cv2.COLOR_BGR2RGB))
        self.depth_pil_image = Image.fromarray(depth_colormap)

    def get_depth_pill_image(self):
        self.update()
        return self.depth_pil_image

    def get_color_pill_image(self):
        self.update()
        return self.color_pil_image

    def get_color_frame(self):
        self.update()
        return self.color_frame

    def get_depth_frame(self):
        self.update()
        return self.depth_frame

    def pipe_stop(self):
        self.pipe.stop()

    def pipe_start(self):
        self.pipe.start(self.rs_config)
