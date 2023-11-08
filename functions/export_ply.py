import pyrealsense2 as rs
import os

def export(color_frame, depth_frame, filename, script_dir):
    # Declare pointcloud object, for calculating point clouds and texture mappings
    pc = rs.pointcloud()

    # Tell pointcloud object to map to this color frame
    pc.map_to(color_frame)

    # Generate the point cloud and texture mappings
    points = pc.calculate(depth_frame)

    # Save point cloud to disk to the output folder in the current directory
    print("Saving to " + filename + "...")

    rel_path = "output\ply\\" + filename
    abs_file_path = os.path.join(script_dir, rel_path)

    print(abs_file_path)
    points.export_to_ply(abs_file_path, color_frame)
    print("exported the ply file")
