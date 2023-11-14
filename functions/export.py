from datetime import datetime
import pyrealsense2 as rs
import os

def get_latest_folder(scipt_dir):
    
    # check if output folder exists
    if not os.path.exists(os.path.join(scipt_dir, "output")):
        os.makedirs(os.path.join(scipt_dir, "output"))
        print("Created output folder")
    
    # check if the output folder has a folder with the current year
    if not os.path.exists(os.path.join(scipt_dir, "output", str(datetime.now().year))):
        os.makedirs(os.path.join(scipt_dir, "output", str(datetime.now().year)))
        print("Created year folder")

    # check if the output folder has a folder with the current month
    if not os.path.exists(os.path.join(scipt_dir, "output", str(datetime.now().year), str(datetime.now().month))):
        os.makedirs(os.path.join(scipt_dir, "output", str(datetime.now().year), str(datetime.now().month)))
        print("Created month folder")

    # check if the output folder has a folder with the current day
    if not os.path.exists(os.path.join(scipt_dir, "output", str(datetime.now().year), str(datetime.now().month), str(datetime.now().day))):
        os.makedirs(os.path.join(scipt_dir, "output", str(datetime.now().year), str(datetime.now().month), str(datetime.now().day)))
        print("Created day folder")
    # check if the output folder has a folder with the current minute
    if not os.path.exists(os.path.join(scipt_dir, "output", str(datetime.now().year), str(datetime.now().month), str(datetime.now().day), str(datetime.now().minute))):
        os.makedirs(os.path.join(scipt_dir, "output", str(datetime.now().year), str(datetime.now().month), str(datetime.now().day), str(datetime.now().minute)))
        print("Created minute folder")

    # return the path to the minute folder
    return os.path.join(scipt_dir, "output", str(datetime.now().year), str(datetime.now().month), str(datetime.now().day), str(datetime.now().minute))

def ply(color_frame, depth_frame, filename, script_dir):
    # Declare pointcloud object, for calculating point clouds and texture mappings
    pc = rs.pointcloud()

    # Tell pointcloud object to map to this color frame
    pc.map_to(color_frame)

    # Generate the point cloud and texture mappings
    points = pc.calculate(depth_frame)

    abs_file_path = os.path.join(get_latest_folder(script_dir), filename)

    points.export_to_ply(abs_file_path, color_frame)
    print("exported the ply file to " + abs_file_path)

def png(color_image, depth_image, filename, script_dir):
    color_filename = filename + "_color_image.png"
    depth_filename = filename + "_depth_image.png"

    abs_file_path_color = os.path.join(get_latest_folder(script_dir), color_filename)
    abs_file_path_depth = os.path.join(get_latest_folder(script_dir), depth_filename)

    color_image.save(abs_file_path_color)
    depth_image.save(abs_file_path_depth)
    
    print("Saved color image to " + abs_file_path_color)
    print("Saved depth image to " + abs_file_path_depth)