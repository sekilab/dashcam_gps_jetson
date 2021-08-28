sudo apt install -y  cmake libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev gstreamer1.0-tools libgtk2.0-dev gstreamer1.0-omx=1.0.0.1-0+rpi12+jessiepmg gstreamer1.0-plugins-bad gstreamer1.0-plugins-good

sudo apt install -y g++ cmake make wget unzip

mkdir OpenCV && cd OpenCV

wget -O opencv.zip https://github.com/opencv/opencv/archive/master.zip
unzip opencv.zip

mv opencv-master opencv
mkdir -p build && cd build
cmake -D CMAKE_BUILD_TYPE=RELEASE -D CMAKE_INSTALL_PREFIX=/usr/local -DINSTALL_PYTHON_EXAMPLES=ON -D INSTALL_C_EXAMPLES=ON -D　PYTHON_EXECUTABLE=/usr/bin/python3 -D BUILD_EXAMPLES=ON -D WITH_GTK=ON -D WITH_GSTREAMER=ON -D WITH_FFMPEG=OFF -D WITH_QT=OFF ../opencv
make -j4

sudo make install
