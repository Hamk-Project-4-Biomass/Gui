import pyrealsense2 as rs

# Declare pointcloud object, for calculating point clouds and texture mappings
pc = rs.pointcloud()
# We want the points object to be persistent so we can display the last cloud when a frame drops
points = rs.points()

# Declare RealSense pipeline, encapsulating the actual device and sensors
pipe = rs.pipeline()
config = rs.config()

# enable the right streams
config.enable_stream(rs.stream.depth, rs.format.z16, 30)
config.enable_stream(rs.stream.color, rs.format.bgr8, 30)

# Start streaming with the chosen configuration
prof = pipe.start(config)

# Get the active device and the camera (rgb) sensor
sensor_dep = prof.get_device()

# add the depth sensor to the pipeline
sensor_dep = sensor_dep.first_depth_sensor()

# get the depth scale
depth_scale = sensor_dep.get_depth_scale()
print("Depth Scale is: " , depth_scale)

# get the camera sensor
sensor_rgb = prof.get_device().query_sensors()[1]

# the color of the rgb is to dark adjust the camera settings
# set the auto exposure of the camera to false
sensor_rgb.set_option(rs.option.enable_auto_exposure, False)
# set the exposure to 10000
sensor_rgb.set_option(rs.option.exposure, 1000)
# set the gain to 100
sensor_rgb.set_option(rs.option.gain, 10)

    
try:
    # Wait for the next set of frames from the camera
    frames = pipe.wait_for_frames()

    # instead of the colorizer we can also take the color image
    color_frame = frames.get_color_frame()

    # Create alignment primitive with color as its target stream:
    align = rs.align(rs.stream.color)
    frameset = align.process(frames)

    # Update color and depth frames:
    aligned_depth_frame = frameset.get_depth_frame()

    # Tell pointcloud object to map to this color frame
    pc.map_to(color_frame)

    # Generate the point cloud and texture mappings
    points = pc.calculate(aligned_depth_frame)



    # Save point cloud to disk
    print("Saving to test.ply...")
    points.export_to_ply("test.ply", color_frame)
    print("Done")

finally:
    pipe.stop()
