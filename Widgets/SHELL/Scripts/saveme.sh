#!/bin/bash
chromium-browser --kiosk --anonymous --app=htto://localhost:3245 &
while true
do
bash /home/dashboard2/NorsePi/SHELL/main.sh 2>&1 | tee /home/dashboard2/log_`date "+%Y-%m-%d_%T"`.txt
sleep 900
done
