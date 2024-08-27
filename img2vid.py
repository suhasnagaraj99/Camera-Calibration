import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
import math
import os

"""# Problem 1: Single Camera Calibration
# Image Collection:
70 images of the calibration board have been collected using a fixed focus webcam.
"""

## Creating a video object 'out'
fourcc = cv.VideoWriter_fourcc(*'XVID')
## The video is named 'project3_pics_video.mp4'
out = cv.VideoWriter('project3_pics_video.mp4', fourcc, 10, (1920, 1080))

## Defining the path to the images collected for calibration
image_folder_path = "/home/suhas99/ENPM673/HW3/Question1_images"

## Extracting each image in the given folder
for filename in os.listdir(image_folder_path):

  image_path = os.path.join(image_folder_path, filename)
  image = cv.imread(image_path)

  ## Writing the image to the video object
  out.write(image)

out.release()