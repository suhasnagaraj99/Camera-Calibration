import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
import math
import os

"""-----

The camera parameters are used to undistort the images using the function cv.undistort function. For the ease of visualization, a new video 'project3_undistorted_video.mp4', is created with the undistorted images. This video can be compared with the 'project3_calib_video.mp4' to see the difeerence between the distorted and undistorted frames.

Link for the undistorted video: https://drive.google.com/file/d/1-1ZGvZM-H5trKNQ95D6x4WSqIFO0RcFP/view?usp=sharing

A single image and its undistorted version is also plotted below.
"""

## The parameter 'frame_number' is used for selecting a particular frame number (image) for visualization.
## As an example, the 20th frame of the video is plotted below. Please change this parameter to plot different frames.
frame_number=20
index_number=1

criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

with np.load("calibration_data.npz") as data:
    camera_matrix = data['camera_matrix']
    new_camera_matrix = data['new_camera_matrix']
    distortion_coefficients = data['distortion_coefficients']

## list for storing the corners detected from undistorted pics
undistorted_corners=[]

## The video is read to extract frames
video2 = cv.VideoCapture("project3_calib_video.mp4")

## Creating a video object 'out3'
fourcc3 = cv.VideoWriter_fourcc(*'XVID')
## The video is named 'project3_undistorted_video.mp4'
out3 = cv.VideoWriter('project3_undistorted_video.mp4', fourcc3, 10, (1920, 1080))

## Each frame of the video is extracted
while video2.isOpened():
  ret1, frame = video2.read()
  if ret1 == False:
    break
  ## The frame is undistorted using the intrinsic parametres of the camera. OpenCV documentation is taken as reference.
  undistorted_frame = cv.undistort(frame, camera_matrix, distortion_coefficients, None, new_camera_matrix)

  ## The undistorted image is converted to grayframe to extract its corners. This step is not required for the calibration and it is only used for visualization of calibration results.
  undistorted_frame_gray = cv.cvtColor(undistorted_frame, cv.COLOR_BGR2GRAY)
  ## cv.findChessboardCorners function is used to find the corners of the undistorted Chessboard images
  ret2, undistorted_checkerboard_corners = cv.findChessboardCorners(undistorted_frame_gray, (7,9))

  if ret2==True:
    ## cv.cornerSubPix is again used to refine the detected corners.
    undistorted_checkerboard_corners = cv.cornerSubPix(undistorted_frame_gray, undistorted_checkerboard_corners, (15, 15), (-1, -1), criteria)
    ## The detected corners are stored in a list
    undistorted_corners.append(undistorted_checkerboard_corners)

  ## undistorted frames are written to the video
  out3.write(undistorted_frame)

  # Plotting the distorted and the undistorted image
  if index_number==frame_number:
    fig, axes = plt.subplots(1, 2, figsize=(20, 10))
    axes[0].imshow(cv.cvtColor(frame, cv.COLOR_BGR2RGB))
    axes[0].axis('off')
    axes[0].set_title('Distorted Image')
    axes[1].imshow(cv.cvtColor(undistorted_frame, cv.COLOR_BGR2RGB))
    axes[1].axis('off')
    axes[1].set_title('Undistorted_image')
    plt.tight_layout()
  index_number = index_number + 1

out3.release()