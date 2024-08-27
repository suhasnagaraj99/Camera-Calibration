import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
import math
import os


## The video created in the above step is read for further processing
video2 = cv.VideoCapture("project3_pics_video.mp4")

# Condition statement to check if the video is opened and loaded, without errors
if video2.isOpened():
  print("Video is Opened",'\n')
  # Extracting video properties
  # width of each frame in the video
  width2 = int(video2.get(cv.CAP_PROP_FRAME_WIDTH))
  # height of each frame in the video
  height2 = int(video2.get(cv.CAP_PROP_FRAME_HEIGHT))
else:
  print("Error")

"""# Calibration Pipeline:

After creating a video from the collected images, the frames of the video are further filtered to include only those frames which are useful for calibration.

From the filtered frames, a new video is created.

The process is explained in the below cell.
"""

## Creating a video object 'out2'
fourcc2 = cv.VideoWriter_fourcc(*'XVID')
## The video is named 'project3_calib_video.mp4'
out2 = cv.VideoWriter('project3_calib_video.mp4', fourcc2, 10, (1920, 1080))

## Properties of the calibration board
## It has 9 rows and 7 columns of corners
point_row_no = 9
point_col_no = 7

## Each side of the square is 20 mm
calibration_square_size = 20

## Index value to keep a track of how many frames are considered for calibration
n1=0

## Initializing a numpy array to store the coordinate values of the corners in the calibration board
xyz_coords = np.zeros((point_row_no * point_col_no, 3), np.float32)

## Each point is assigned a x,y,z value
## It is assumed that the calibration board is on xy plane (z=0) and it is considered that the top left corner is the origin
for i in range(point_row_no):
    for j in range(point_col_no):
        index = i * point_col_no + j
        xyz_coords[index, 0] = j * 20
        xyz_coords[index, 1] = i * calibration_square_size
        xyz_coords[index, 2] = 0

## Creating an empty array to store the values of image coordinate and the corresponding object coordinate points
image_coords=[]
object_coords=[]

## Defining the criteria for accurate determination of the corners (subpixel level) using function cv2.SubPix. This function refines the detected corners and accurately places them.
criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

## The parameter 'plot_frame' is used for selecting a particular frame number (image) for visualization.
## As an example, the 20th frame of the video is plotted below. Please change this parameter to plot different frames. 70 frames are considered for calibration.
plot_frame = 20
plot_index = 1

while video2.isOpened():

  ## The frames of the video is extracted. Each frame is an image used for calibration.
  ret1, frame = video2.read()

  if ret1 == False:
    break

  ## The image is converted to grayscale
  gray_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

  ## cv.findChessboardCorners is used to get the calibration board corners
  ret2, checkerboard_corners = cv.findChessboardCorners(gray_frame, (point_col_no,point_row_no))
  corner_image=frame.copy()

  ## If the cv.findChessboardCorners function clearly detects the corners, that frame is considered for further calibration. Other frames are ignored.
  if ret2==True:
    n1=n1+1

    ## cv.cornerSubPix function is used to further refine the coordinates of the detetcted camera. If the corners detected are accurate, the calibration will be accurate.
    check_corners = cv.cornerSubPix(gray_frame, checkerboard_corners, (15, 15), (-1, -1), criteria)

    ## The frames in which the corners have been detected correctly is written into a new video file. This video will be used for further steps of calibration process.
    ## In my case, the function was able to detect the corners in all the frames considered. Hence both the 'project3_pics_video.mp4' and 'project3_calib_video.mp4' are the same.
    ## But I have included this line of code so that, if the input pics are changed, same code can be used to calibrate the camera.
    out2.write(frame)

    ## Plotting a single frame with detected corners
    if plot_index==plot_frame:
        for corners in check_corners:
            x, y = corners.ravel()
            cv.circle(corner_image, (int(x), int(y)), 5, (0, 255, 0), -1)
        plt.figure(figsize=(20, 10))
        plt.imshow(cv.cvtColor(corner_image, cv.COLOR_BGR2RGB))

    ## The detected image-corner-coordinate values and the corresponding world-corner-cordinate values are appended to the lists.
    image_coords.append(check_corners)
    object_coords.append(xyz_coords)
    plot_index=plot_index+1

## From the list of image coordinates and the world cordinates, the camera is calibrated using cv.calibrateCamera function.
## Here the camera_matrix and distortion coefficients represents the intrinsic parameters of the camera whereas the rotation and translation vectors corresponds to the extrinsic parameters.
ret3, camera_matrix, distortion_coefficients, rotation_vectors, translation_vectors = cv.calibrateCamera(object_coords, image_coords, (width2,height2), None, None)
out2.release()

"""The above image shows the detected corners (in green) drawn on the corresponding image."""

print("Number of frames/images considered for calibrating the camera: ",n1)

print("The camera matrix is: ",'\n',camera_matrix)

print("The distortion coefficients are: ",'\n',distortion_coefficients)

## The obtained camera matrix is then optimised by using the distortion coefficients to obtain a optimised camera matrix
new_camera_matrix, roi = cv.getOptimalNewCameraMatrix(camera_matrix, distortion_coefficients, (1920,1080), 1, (1920,1080))
print("The optimized camera matrix is: ",'\n',new_camera_matrix)

npz_file = 'calibration_data.npz'

# Save to .npz file
np.savez(npz_file,
         camera_matrix=camera_matrix, 
         new_camera_matrix=new_camera_matrix, 
         distortion_coefficients=distortion_coefficients)

"""
# Reprojection Error Analysis:

For each frame of the video / for each image, the reprojection error is calculated based on the 3d world proints projected on the image plane by taking into account the intrinsic and extrensic parameters of the camera. OpenCV documentation is taken as reference for this step. The reprojection error for each image is calculated and is plotted.
"""
## reprojection error is stored in a list
reprojection_errors = []
## Corresponding frame numbers are stored for plotting
frame_number=[]
## The reprojection points obtained are stored for visualization
reprojection_points=[]


## For each frame/image, the reprojection error is calculated by taking the norm between projected corners and the detected corners
for i in range(len(rotation_vectors)):
  proj_img_pts, _ = cv.projectPoints(xyz_coords, rotation_vectors[i], translation_vectors[i], camera_matrix, distortion_coefficients)
  dist = cv.norm(image_coords[i], proj_img_pts, cv.NORM_L2) / len(proj_img_pts)
  reprojection_errors.append(dist)
  frame_number.append(i+1)
  reprojection_points.append(proj_img_pts)

## The reprojection error graph is plotted based on the values stored in the list
plt.figure(figsize=(10, 8))
plt.plot(frame_number, reprojection_errors,marker=".")
plt.title('Reprojection Errors for Each Image')
plt.xlabel('Image Number ')
plt.ylabel('Reprojection Error')
plt.savefig('reprojection_errors_plot.png', dpi=300)
plt.show()
