# Camera-Calibration

## Project Description
This repository contains code for ENPM673 Project 3A  - Camera Calibration, UnDistortion and Reprojection error analysis

### Required Libraries
Before running the code, ensure that the following Python libraries are installed:

- `cv2`
- `numpy`
- `matplotlib`

You can install if they are not already installed:

```bash
sudo apt-get install python3-opencv python3-numpy python3-matplotlib
```

## Camera Calibration

1. The images of the calibration board/grid are taken at different angles and orientations. These images are saved in the `Questions1_images` folder.
2. Make sure the folder `Questions1_images` is pasted in the same directory as the `img2vid.py` file.
3. The `img2vid.py` script reads the images and converts it into a video, `project3_pics_video.mp4`. This eases further processes.
```bash
python3 img2vid.py
```
4. Only valid frames are selected from `project3_pics_video.mp4` and are written into video `project3_calib_video.mp4`. These valid frames are used for calibration:

```bash
python3 calibrate_camera.py
```
5. The above script aslo saves the calibration output in the form of .npz file, `calibration_data.npz`
6. The `calibrate_camera.py` script also computes the reporojection error and stores the result as a plot in `reprojection_errors_plot.png`
7. The script `undistort.py` undistorts the initial frames using the computed camera/calibration parameters. The resulting undistorted frames are stored as a video `project3_undistorted_video.mp4`
```bash
python3 undistort.py
```
