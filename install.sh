#!/bin/bash

if [[ `id -u` -ne 0 ]]; then
  # rootユーザーにしか実行させない
  echo "Please run as root"
  exit 1
fi

if type "python3.9" > /dev/null 2>&1; then
    :
else
    apt install python3.9 python3.9-venv -y
fi

mkdir /usr/UVC-Capture/
cd `dirname $0`
cp -r ./ /usr/UVC-Capture/

cd /usr/UVC-Capture/
python3.9 -m venv .venv

source ./.venv/bin/activate
pip install numpy==1.23.5 opencv-python==4.6.0.66
deactivate

cp UVC-Capture.service /etc/systemd/system
systemctl daemon-reload
systemctl enable UVC-Capture
systemctl start UVC-Capture

echo "Finish!!"