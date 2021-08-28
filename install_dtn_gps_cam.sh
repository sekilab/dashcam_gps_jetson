mkdir ~/gps_data
mkdir ~/video_data
sudo apt install -y python3-pip
sudo apt -y autoremove
python3 -m pip install pynmea2
python3 -m pip install ipinfo
python3 -m pip install pyserial
echo "$USER ALL=(ALL:ALL) NOPASSWD:/home/"$USER"/video_gps_rpi/run_main.sh" | sudo EDITOR='tee -a' visudo
mkdir -p ~/.config/autostart
echo "[Desktop Entry]
Type=Application
Exec=sudo /home/"$USER"/video_gps_rpi/run_main.sh
Hidden=false
NoDisplay=false
X-GNOME-Autostart-enabled=true
Name[en_US]=DTN-CAM
Name=DTN-CAM
Comment[en_US]=Record video with GPS
Comment=Record video with GPS
" > ~/.config/autostart/sudo.desktop
