import pyrealsense2 as rs
import os

def ply(color_frame, depth_frame, filename, script_dir):
    # Declare pointcloud object, for calculating point clouds and texture mappings
    pc = rs.pointcloud()

    # Tell pointcloud object to map to this color frame
    pc.map_to(color_frame)

    # Generate the point cloud and texture mappings
    points = pc.calculate(depth_frame)

    rel_path = "output\ply\\" + filename
    abs_file_path = os.path.join(script_dir, rel_path)

    points.export_to_ply(abs_file_path, color_frame)
    print("exported the ply file to " + abs_file_path)

def png(color_image, depth_image, filename, script_dir):
    try:
        color_filename = filename + "_color_image.png"
        depth_filename = filename + "_depth_image.png"
        
        rel_path_color = "output\png\color\\" + color_filename
        rel_path_depth = "output\png\depth\\" + depth_filename

        abs_file_path_color = os.path.join(script_dir, rel_path_color)
        abs_file_path_depth = os.path.join(script_dir, rel_path_depth)

        color_image.save(abs_file_path_color)
        depth_image.save(abs_file_path_depth)

        print("Saved color image to " + abs_file_path_color)
        print("Saved depth image to " + abs_file_path_depth)
    except:
        print("No device detected")
        pass
