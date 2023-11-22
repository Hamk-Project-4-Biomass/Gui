import pyrealsense2 as rs
import numpy as np
import cv2
from PIL import Image


class RealSense:

    def __init__(self):

        self.depth_pil_image = None
        self.color_pil_image = None
        self.color_image = None
        self.depth_image = None
        self.color_frame = None
        self.depth_frame = None
        self.frames = None

        try: 
            self.pipe = rs.pipeline()

            self.rs_config = rs.config()
            
            
            self.rs_config.enable_stream(rs.stream.depth, rs.format.z16, 30)
            self.rs_config.enable_stream(rs.stream.color, rs.format.bgr8, 30)

            cfg = self.pipe.start(self.rs_config)

            # profile = cfg.get_stream(rs.stream.depth) # Fetch stream profile for depth stream
            # profile_color = cfg.get_stream(rs.stream.color) # Fetch stream profile for color stream
            # intr = profile.as_video_stream_profile().get_extrinsics() # Downcast to video_stream_profile and fetch intrinsics
            # intr_color = profile_color.as_video_stream_profile().get_extrinsics() # Downcast to video_stream_profile and fetch intrinsics
            # print(intr)
            # print(intr_color)

            self.sensor_rgb = self.pipe.get_active_profile().get_device().query_sensors()[1]

            self.sensor_depth = self.pipe.get_active_profile().get_device().query_sensors()[0]

            self.update()
        except:
            print("No device detected")
            pass

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
        self.color_image = cv2.resize(self.color_image, dim, interpolation=cv2.INTER_AREA)

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

    def color_auto_exposure(self):
        if self.sensor_rgb.get_option(rs.option.enable_auto_exposure):
            self.sensor_rgb.set_option(rs.option.enable_auto_exposure, False)
        else:
            self.sensor_rgb.set_option(rs.option.enable_auto_exposure, True)

    def set_color_exposure(self, value):
        self.sensor_rgb.set_option(rs.option.exposure, value)

    def set_color_gain(self, value):
        self.sensor_rgb.set_option(rs.option.gain, value)

    def set_color_brightness(self, value):
        self.sensor_rgb.set_option(rs.option.brightness, value)

    def set_color_contrast(self, value):
        self.sensor_rgb.set_option(rs.option.contrast, value)

    def set_color_hue(self, value):
        self.sensor_rgb.set_option(rs.option.hue, value)

    def set_color_saturation(self, value):
        self.sensor_rgb.set_option(rs.option.saturation, value)

    def set_color_sharpness(self, value):
        self.sensor_rgb.set_option(rs.option.sharpness, value)

    def set_color_gamma(self, value):
        self.sensor_rgb.set_option(rs.option.gamma, value)

    def set_color_white_balance(self, value):
        self.sensor_rgb.set_option(rs.option.white_balance, value)

    def toggle_color_auto_white_balance(self):
        if self.sensor_rgb.get_option(rs.option.enable_auto_white_balance):
            self.sensor_rgb.set_option(rs.option.enable_auto_white_balance, False)
        else:
            self.sensor_rgb.set_option(rs.option.enable_auto_white_balance, True)

    def color_backlight_compensation(self):
        if self.sensor_rgb.get_option(rs.option.backlight_compensation):
            self.sensor_rgb.set_option(rs.option.backlight_compensation, False)
        else:
            self.sensor_rgb.set_option(rs.option.backlight_compensation, True)

    def color_low_light_compensation(self):
        if self.sensor_rgb.get_option(rs.option.low_light_comp):
            self.sensor_rgb.set_option(rs.option.low_light_comp, False)
        else:
            self.sensor_rgb.set_option(rs.option.low_light_comp, True)

    def set_color_power_line_frequency(self, value):
        self.sensor_rgb.set_option(rs.option.power_line_frequency, value)

    def set_depth_exposure(self, value):
        self.sensor_depth.set_option(rs.option.exposure, value)

    def set_depth_gain(self, value):
        self.sensor_depth.set_option(rs.option.gain, value)

    def set_depth_power(self,value):
        self.sensor_depth.set_option(rs.option.laser_power, value)

    def depth_auto_exposure(self):
        if self.sensor_depth.get_option(rs.option.enable_auto_exposure):
            self.sensor_depth.set_option(rs.option.enable_auto_exposure, False)
        else:
            self.sensor_depth.set_option(rs.option.enable_auto_exposure, True)


    # Getters
    def get_color_power_line_frequency(self):
        return self.sensor_rgb.get_option(rs.option.power_line_frequency)

    def get_color_auto_white_balance(self):
        return self.sensor_rgb.get_option(rs.option.enable_auto_white_balance)

    def get_color_auto_exposure(self):
        return self.sensor_rgb.get_option(rs.option.enable_auto_exposure)

    def get_color_exposure(self):
        return self.sensor_rgb.get_option(rs.option.exposure)

    def get_color_gain(self):
        return self.sensor_rgb.get_option(rs.option.gain)

    def get_color_brightness(self):
        return self.sensor_rgb.get_option(rs.option.brightness)

    def get_color_contrast(self):
        return self.sensor_rgb.get_option(rs.option.contrast)

    def get_color_hue(self):
        return self.sensor_rgb.get_option(rs.option.hue)

    def get_color_saturation(self):
        return self.sensor_rgb.get_option(rs.option.saturation)

    def get_color_sharpness(self):
        return self.sensor_rgb.get_option(rs.option.sharpness)

    def get_color_gamma(self):
        return self.sensor_rgb.get_option(rs.option.gamma)

    def get_color_white_balance(self):
        return self.sensor_rgb.get_option(rs.option.white_balance)

    def get_backlight_compensation(self):
        return self.sensor_rgb.get_option(rs.option.backlight_compensation)

    def get_low_light_compensation(self):
        return self.sensor_rgb.get_option(rs.option.low_light_compensation)
    
    def get_depth_exposure(self):
        return self.sensor_depth.get_option(rs.option.exposure)
    
    def get_depth_gain(self):
        return self.sensor_depth.get_option(rs.option.gain)
    
    def get_depth_power(self):
        return self.sensor_depth.get_option(rs.option.laser_power)
    
    def get_depth_auto_exposure(self):
        return self.sensor_depth.get_option(rs.option.enable_auto_exposure)
    
