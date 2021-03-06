# Dashcam recorder with GPS

This Python program can be used to record videos using Gstreamer along with GPS on Jetson family devices such as Jetson Nano, Jetson Xavier NX, Jetson Xavier AGX, Jetson TX2, etc. 
This program uses Assisted GPS (A-GPS) for faster location retrieval from the satellite by downloading satellite almanac data based on approximate location from the IP address.

## Requirements

- A Jetson device
- USB camera
- A GNSS receiver
- 4G/LTE module (Optional, required for A-GPS)
- IPINFO API token (Optional, required for A-GPS)
- u-blox AssistNow API token (Optional, required for A-GPS)

## Installation

Before installtion, make sure whether you want to use A-GPS or not. If you do not wish to use A-GPS, then modify line 55 of video_gps.py to False.

If you wish to use A-GPS, please obtain API token for IPINFO and u-blox AssistNow service and input them in string format on [L42](https://github.com/sekilab/dashcam_gps_jetson/blob/b93cb6278f19fca51c3d35a98c5c114bb2eb929a/video_gps.py#L42) and [L43](https://github.com/sekilab/dashcam_gps_jetson/blob/b93cb6278f19fca51c3d35a98c5c114bb2eb929a/video_gps.py#L43).

Installation of Gstreamer plugins:
`sudo bash gstreamer_install.sh`

Installation of main program with all dependencies:
`sudo bash install_dtn_gps_cam.sh`

## Running program

The program runs automatically on startup and saves video (approx. one minute duration files) and GPS logs in the `$HOME` directory. 
