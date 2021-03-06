from functions import Dimensioning, Convert
import time
from subprocess import run
import open3d as o3d
import os.path

# store starting time
start = time.time()
userId = "3"
front_image = "TestBench/"+userId+"/front.jpg"
side_image = "TestBench/"+userId+"/side.jpg"
top_image = "TestBench/"+userId+"/top.jpg"

d1 = Dimensioning(userId, "front", front_image)
d2 = Dimensioning(userId, "side", side_image)
d3 = Dimensioning(userId, "top", top_image)
if(d1 == None or d2 == None or d3 == None):
    exit(0)

# front view length of highlighted line
fratio = float(d1["ratio"]) * 2
# side view length of highlighted line
sratio = float(d2["ratio"]) * 2
# top view length of highlighted line
tratio = float(d3["ratio"]) * 2

print(Convert(userId, front_image, side_image, top_image, fratio, sratio, tratio))

# store end time
end = time.time()
print("Total time taken to convert:", end-start)

# store starting time
start = time.time()
scad_filename = "static/" + userId + '/' + userId + ".scad"
stl_filename = "static/" + userId + '/' + userId + ".stl"
pcd_filename = "static/" + userId + '/' + userId + ".pcd"

if(os.path.isfile(scad_filename)):
    run("openscad -o " + stl_filename + " " + scad_filename)

    if(os.path.isfile(stl_filename)):
        mesh = o3d.io.read_triangle_mesh(stl_filename)
        pointcloud = mesh.sample_points_poisson_disk(100000)
        o3d.io.write_point_cloud(pcd_filename, pointcloud)
        o3d.visualization.draw_geometries([pointcloud])
        # store end time
        end = time.time()
        print("Total time taken to convert from stl to point cloud:", end-start)
