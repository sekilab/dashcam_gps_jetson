# Author: Ashutosh Kumar, The University of Tokyo
# Date: 2021/03/10
# Program Version: 1.1.0

# Please obtain API token from U-BLOX and IPINFO for Assisted GPS (A-GPS) service. They can be substituted on Line 46 and 47 of this program


import pprint
import ipinfo
import pynmea2
import serial
import requests
import time
import os
import threading
import multiprocessing
from datetime import datetime
import subprocess
from random import randint

# Get a random digit of n digits. This is used to name video files.
def rand_n(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)

# This function uses location based on the IP address and passes it to the device to assist obtaining GPS location
def get_initial_location(ipinfo_access_token):
	api_handler = ipinfo.getHandler(ipinfo_access_token)
	details = api_handler.getDetails()

	latitude, longitude = details.details["loc"].split(",")

	return {"latitude": latitude, "longitude": longitude}

# get_lat_lon function is used to get the latitude and longitude in real time and updates the global latitude and longitude variable. This function runs on a separate thread.
def get_lat_lon(latitude, longitude):
    INTERNET_AVAILABLE = True
    GPS_FAILURE_TIME_LIMIT = 40
    COM_PORT = "/dev/ttyUSB0"
    BAUDRATE = 115200
    API_TOKEN = "API_TOKEN_FOR_ASSIST_NOW"
    IPINFO_ACCESS_TOKEN = "API_TOKEN_FOR_IPINFO"
    gps_failure_time = 0
    internet_failure_count = 0

    print("Running get_lat_lon function")
    f = open(f"/home/{os.getlogin()}/gps_data/{datetime.now().strftime('%Y%m%d%H%M%S')}.log", "a")

    if INTERNET_AVAILABLE:
        a_gps = True
        while a_gps:
            try:
                initial_location = get_initial_location(IPINFO_ACCESS_TOKEN)
                http_response = requests.get("https://online-live1.services.u-blox.com/GetOnlineData.ashx?token=" +
                API_TOKEN + ";gnss=gps,glo,qzss,bds,gal;datatype=eph,alm,aux,pos;lat=" + initial_location["latitude"] + ";lon=" + initial_location["longitude"] +";alt=0.000000;pacc=5000.000000;filteronpos")
                a_gps = False
            except:
                print("Internet is not available, trying again!")
                time.sleep(5)
                internet_failure_count += 1
                if internet_failure_count >= 5:
                    INTERNET_AVAILABLE = False
                    break
                else:
                    continue

    serial_port = serial.Serial(COM_PORT, BAUDRATE, timeout = None)

    # Wait until GPS is released
    pipe = True
    while pipe:
        pipe = serial_port.inWaiting()
        serial_port.read(pipe)

    # Write A-GPS Data
    if INTERNET_AVAILABLE:
        print("Sending A-GPS Data To GPS Module")
        serial_port.write(http_response.content)
        print("Finished !")
    else:
        print("Continue without internet or A-GPS")

    try:
        while True:
            line = serial_port.readline()
            line2 = line.decode('latin-1')

            if line2.startswith("$GNGGA"):
                msg = pynmea2.parse(line2.strip())
                latitude.value, longitude.value = msg.latitude, msg.longitude
                f.write(f"{datetime.now().strftime('%Y:%m:%d:%H:%M:%S')} {msg.timestamp} {str(latitude.value)} {str(longitude.value)} \n")
                f.flush()
            else:
                pass
    except KeyboardInterrupt:
        serial_port.close()


def gstreamer_nano():

    cmd = f"gst-launch-1.0 -e v4l2src device=/dev/video0  ! image/jpeg,width=1280,height=720,framerate=30/1 ! jpegdec ! videoflip method=rotate-180 ! nvvidconv ! queue ! clockoverlay ! omxh264enc ! splitmuxsink location=/home/{os.getlogin()}/video_data/{rand_n(5)}-%04d.mp4 max-size-time=60000000000 max-size-bytes=10000000"  
    process = subprocess.Popen(cmd, shell = True)

if __name__ == "__main__":
    

    # Here we do not put any values to the latitude and longitude in the beginning. The values will be updated using the global variable in get_lat_lon function running on an independent thread
    latitude = multiprocessing.Value('d', 1.0)
    longitude = multiprocessing.Value('d', 1.0)

    gps_thread = multiprocessing.Process(target = get_lat_lon, args=(latitude, longitude))
    gps_thread.start()
    
    gstreamer_nano()